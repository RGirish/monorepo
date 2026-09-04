import json
import random
import string
import sys

DEFAULT_NUM_LINES = 2_000_000
OUTPUT_PATH = "words.jsonl"


def random_word(min_len=1, max_len=15):
    length = random.randint(min_len, max_len)
    return "".join(random.choices(string.ascii_lowercase, k=length))


def main():
    num_lines = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_NUM_LINES
    with open(OUTPUT_PATH, "w") as f:
        for _ in range(num_lines):
            f.write(json.dumps({"word": random_word()}) + "\n")
    print(f"Wrote {num_lines:,} lines to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
