import json
import os

import ray

DEMO_INPUT = "words_corrupted_demo.jsonl"
NUM_DEMO_LINES = 40
CORRUPT_LINE_INDEX = 20
NUM_CHUNKS = 4


def make_corrupted_demo_file():
    with open("words.jsonl") as src:
        lines = [next(src) for _ in range(NUM_DEMO_LINES)]
    # Valid JSON, but missing the "word" key -- will raise KeyError downstream.
    lines[CORRUPT_LINE_INDEX] = json.dumps({"not_word": "oops"}) + "\n"
    with open(DEMO_INPUT, "w") as f:
        f.writelines(lines)


def get_chunk_boundaries(path, num_chunks):
    file_size = os.path.getsize(path)
    boundaries = [0]
    with open(path, "rb") as f:
        for i in range(1, num_chunks):
            approx = file_size * i // num_chunks
            f.seek(approx)
            f.readline()
            boundaries.append(f.tell())
    boundaries.append(file_size)
    return boundaries


@ray.remote
class AttemptCounter:
    def __init__(self):
        self.attempts = 0

    def record_attempt(self):
        self.attempts += 1
        return self.attempts


@ray.remote
def process_chunk(input_path, start, end, chunk_id):
    with open(input_path, "rb") as f:
        f.seek(start)
        data = f.read(end - start)

    results = []
    for line in data.decode("utf-8").splitlines():
        if not line:
            continue
        record = json.loads(line)
        record["length"] = len(record["word"])  # KeyError if "word" is missing
        results.append(record)
    return chunk_id, results


@ray.remote
def process_chunk_flaky(input_path, start, end, chunk_id, attempt_counter):
    ray.get(attempt_counter.record_attempt.remote())
    return ray.get(process_chunk.remote(input_path, start, end, chunk_id))


@ray.remote
def process_chunk_resilient(input_path, start, end, chunk_id):
    with open(input_path, "rb") as f:
        f.seek(start)
        data = f.read(end - start)

    results = []
    skipped = 0
    for line in data.decode("utf-8").splitlines():
        if not line:
            continue
        try:
            record = json.loads(line)
            record["length"] = len(record["word"])
            results.append(record)
        except (json.JSONDecodeError, KeyError) as e:
            skipped += 1
            print(f"  [chunk {chunk_id}] skipping malformed line: {type(e).__name__}: {e}")
    return chunk_id, results, skipped


def run_naive():
    print("\n--- Naive: no error handling ---")
    boundaries = get_chunk_boundaries(DEMO_INPUT, NUM_CHUNKS)
    futures = [
        process_chunk.remote(DEMO_INPUT, boundaries[i], boundaries[i + 1], i) for i in range(NUM_CHUNKS)
    ]
    for i, future in enumerate(futures):
        try:
            chunk_id, results = ray.get(future)
            print(f"Chunk {chunk_id}: OK, {len(results)} lines processed")
        except Exception as e:
            print(f"Chunk {i}: FAILED - {type(e).__name__}: {e}")


def run_with_retries():
    print("\n--- With max_retries=2, retry_exceptions=True ---")
    attempt_counter = AttemptCounter.remote()
    boundaries = get_chunk_boundaries(DEMO_INPUT, NUM_CHUNKS)
    flaky_with_options = process_chunk_flaky.options(max_retries=2, retry_exceptions=True)
    futures = [
        flaky_with_options.remote(DEMO_INPUT, boundaries[i], boundaries[i + 1], i, attempt_counter)
        for i in range(NUM_CHUNKS)
    ]
    for i, future in enumerate(futures):
        try:
            chunk_id, results = ray.get(future)
            print(f"Chunk {chunk_id}: OK, {len(results)} lines processed")
        except Exception as e:
            print(f"Chunk {i}: FAILED even after retries - {type(e).__name__}: {e}")
    total_attempts = ray.get(attempt_counter.record_attempt.remote()) - 1
    print(f"Total task attempts across all chunks: {total_attempts} (expected {NUM_CHUNKS} + 2 retries on the bad chunk = {NUM_CHUNKS + 2})")


def run_resilient():
    print("\n--- Resilient: catch per-line errors, skip bad lines ---")
    boundaries = get_chunk_boundaries(DEMO_INPUT, NUM_CHUNKS)
    futures = [
        process_chunk_resilient.remote(DEMO_INPUT, boundaries[i], boundaries[i + 1], i)
        for i in range(NUM_CHUNKS)
    ]
    for future in futures:
        chunk_id, results, skipped = ray.get(future)
        print(f"Chunk {chunk_id}: OK, {len(results)} lines processed, {skipped} skipped")


def main():
    ray.init()
    make_corrupted_demo_file()
    run_naive()
    run_with_retries()
    run_resilient()
    ray.shutdown()


if __name__ == "__main__":
    main()
