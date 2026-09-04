import json
import os
import time

import ray

INPUT_PATH = "words.jsonl"


def get_chunk_boundaries(path, num_chunks):
    file_size = os.path.getsize(path)
    boundaries = [0]
    with open(path, "rb") as f:
        for i in range(1, num_chunks):
            approx = file_size * i // num_chunks
            f.seek(approx)
            f.readline()  # discard partial line, so each chunk starts on a line boundary
            boundaries.append(f.tell())
    boundaries.append(file_size)
    return boundaries


@ray.remote
def process_chunk(input_path, start, end, output_path):
    with open(input_path, "rb") as f:
        f.seek(start)
        data = f.read(end - start)

    with open(output_path, "w") as out:
        count = 0
        for line in data.decode("utf-8").splitlines():
            if not line:
                continue
            record = json.loads(line)
            record["length"] = len(record["word"])
            out.write(json.dumps(record) + "\n")
            count += 1
    return count


def main():
    ray.init()
    num_chunks = os.cpu_count()
    boundaries = get_chunk_boundaries(INPUT_PATH, num_chunks)

    start = time.perf_counter()
    futures = [
        process_chunk.remote(
            INPUT_PATH, boundaries[i], boundaries[i + 1], f"words_with_length_chunk_{i}.jsonl"
        )
        for i in range(num_chunks)
    ]
    counts = ray.get(futures)
    elapsed = time.perf_counter() - start

    print(f"Parallel ({num_chunks} chunks/tasks): processed {sum(counts):,} lines in {elapsed:.2f}s")
    ray.shutdown()


if __name__ == "__main__":
    main()
