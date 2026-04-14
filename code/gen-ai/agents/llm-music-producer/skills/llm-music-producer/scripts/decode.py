#!/usr/bin/env python3
"""Reconstruct an MP3 from LLM-generated frame payloads.

Reads a JSON file in the same format produced by encode.py:
  - template_header_hex:  4-byte frame header (hex) to prepend to every payload
  - payload_size_bytes:   expected byte length per decoded payload
  - payloads_b95:         list of Base95-encoded payloads

Prepends the template header to each decoded payload and concatenates
all frames into a valid MP3 file.

Usage:
    python decode.py <payloads.json> <output.mp3> [--play]
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ALPHABET = "".join(chr(i) for i in range(32, 127))


def decode_bytes(s: str, expected_size: int) -> bytes:
    """Decode a Base95 string back to bytes, trimmed to expected_size."""
    result = []
    for i in range(0, len(s), 5):
        group = s[i: i + 5]
        if len(group) < 5:
            break
        n = 0
        for c in group:
            idx = ALPHABET.find(c)
            if idx == -1:
                raise ValueError(f"Character {repr(c)} (code {ord(c)}) not in Base95 alphabet")
            n = n * 95 + idx
        result.append(n.to_bytes(4, "big"))
    return b"".join(result)[:expected_size]


def main():
    parser = argparse.ArgumentParser(description="Reconstruct MP3 from Base95 frame payloads JSON.")
    parser.add_argument("input_json", help="JSON file with payloads_b95, template_header_hex, payload_size_bytes")
    parser.add_argument("output_mp3", help="Output .mp3 file path")
    parser.add_argument("--play", action="store_true", help="Open output in system audio player after writing")
    args = parser.parse_args()

    input_path = Path(args.input_json)
    output_path = Path(args.output_mp3)

    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    meta = json.loads(input_path.read_text())
    header = bytes.fromhex(meta["template_header_hex"])
    payload_size = meta["payload_size_bytes"]
    payloads_b95 = meta["payloads_b95"]

    frames = []
    errors = 0
    for i, b95 in enumerate(payloads_b95):
        try:
            payload = decode_bytes(b95, payload_size)
            frames.append(header + payload)
        except ValueError as e:
            print(f"  Frame {i}: decode error — {e}", file=sys.stderr)
            errors += 1

    if not frames:
        print("Error: no frames decoded", file=sys.stderr)
        sys.exit(1)

    mp3_data = b"".join(frames)
    output_path.write_bytes(mp3_data)

    duration_s = len(frames) * 1152 / 44100
    print(f"  {len(frames)} frames → {output_path.name}  "
          f"({len(mp3_data):,} bytes, ~{duration_s:.1f}s){' — ' + str(errors) + ' frame errors' if errors else ''}")

    if args.play:
        print(f"  Opening {output_path} ...")
        subprocess.run(["open", str(output_path)])


if __name__ == "__main__":
    main()
