import json
import time

INPUT_PATH = "words.jsonl"
OUTPUT_PATH = "words_with_length_sequential.jsonl"


def main():
    start = time.perf_counter()

    with open(INPUT_PATH, "r") as infile, open(OUTPUT_PATH, "w") as outfile:
        for line in infile:
            record = json.loads(line)
            record["length"] = len(record["word"])
            outfile.write(json.dumps(record) + "\n")

    elapsed = time.perf_counter() - start
    print(f"Sequential: processed in {elapsed:.2f}s")


if __name__ == "__main__":
    main()
