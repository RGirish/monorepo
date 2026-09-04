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
            f.readline()
            boundaries.append(f.tell())
    boundaries.append(file_size)
    return boundaries


@ray.remote
class StatsActor:
    def __init__(self):
        self.total_count = 0
        self.total_length = 0

    def report_chunk(self, count, length_sum):
        self.total_count += count
        self.total_length += length_sum

    def get_average(self):
        if self.total_count == 0:
            return 0.0
        return self.total_length / self.total_count


@ray.remote
def process_chunk(input_path, start, end, output_path, stats_actor):
    with open(input_path, "rb") as f:
        f.seek(start)
        data = f.read(end - start)

    count = 0
    length_sum = 0
    with open(output_path, "w") as out:
        for line in data.decode("utf-8").splitlines():
            if not line:
                continue
            record = json.loads(line)
            word_length = len(record["word"])
            record["length"] = word_length
            out.write(json.dumps(record) + "\n")
            count += 1
            length_sum += word_length

    # Block until the actor has applied this chunk's contribution, so that once
    # this task's future resolves, its update is guaranteed to be reflected.
    ray.get(stats_actor.report_chunk.remote(count, length_sum))
    return count


def main():
    ray.init()
    num_chunks = os.cpu_count()
    boundaries = get_chunk_boundaries(INPUT_PATH, num_chunks)
    stats_actor = StatsActor.remote()

    start = time.perf_counter()
    futures = [
        process_chunk.remote(
            INPUT_PATH, boundaries[i], boundaries[i + 1], f"words_with_length_chunk_{i}.jsonl", stats_actor
        )
        for i in range(num_chunks)
    ]
    counts = ray.get(futures)
    elapsed = time.perf_counter() - start

    average_length = ray.get(stats_actor.get_average.remote())

    print(f"Parallel ({num_chunks} chunks/tasks): processed {sum(counts):,} lines in {elapsed:.2f}s")
    print(f"Average word length across file: {average_length:.4f}")
    ray.shutdown()


if __name__ == "__main__":
    main()
