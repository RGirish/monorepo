#!/usr/bin/env python3
"""Parse MP3 files into frames and encode the audio payloads as Base95.

MP3 frame structure:
  [4-byte header][side info][audio payload (Huffman-coded spectral data)]

This script strips the 4-byte header from each frame and encodes only the
payload. The header is deterministic for a fixed bitrate/samplerate and is
stored as metadata so decode.py can reconstruct it without LLM involvement.

Output format (per file): JSON with fields:
  - source:               original filename
  - template_header_hex:  most common frame header (hex) — used for reconstruction
  - payload_size_bytes:   byte length of each decoded payload
  - payloads_b95:         list of Base95-encoded payloads, one per frame

Usage:
    python encode.py <input_dir> <output_dir> [--max-frames N]
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ALPHABET = "".join(chr(i) for i in range(32, 127))

# MPEG1 Layer3 bitrate table (index → kbps)
_BITRATES = {
    0x1: 32, 0x2: 40, 0x3: 48, 0x4: 56, 0x5: 64,
    0x6: 80, 0x7: 96, 0x8: 112, 0x9: 128, 0xA: 160,
    0xB: 192, 0xC: 224, 0xD: 256, 0xE: 320,
}
# MPEG1 sample rate table (index → Hz)
_SAMPLERATES = {0x0: 44100, 0x1: 48000, 0x2: 32000}


def frame_size(header: bytes) -> int | None:
    """Return total frame size in bytes for an MPEG1 Layer3 header, or None if invalid."""
    if len(header) < 4:
        return None
    b1, b2 = header[1], header[2]
    # Sync:     header[0] == 0xFF, top 3 bits of b1 == 0xE0
    # MPEG1:    bits 4-3 of b1 == 0x18
    # Layer3:   bits 2-1 of b1 == 0x02
    if (b1 & 0xE0) != 0xE0 or (b1 & 0x18) != 0x18 or (b1 & 0x06) != 0x02:
        return None
    bitrate = _BITRATES.get((b2 >> 4) & 0x0F)
    samplerate = _SAMPLERATES.get((b2 >> 2) & 0x03)
    if not bitrate or not samplerate:
        return None
    padding = (b2 >> 1) & 0x01
    return (144 * bitrate * 1000 // samplerate) + padding


def parse_frames(data: bytes) -> list[tuple[bytes, bytes]]:
    """Return list of (header, payload) for every valid MPEG1 Layer3 frame."""
    frames = []
    i = 0
    while i < len(data) - 4:
        if data[i] == 0xFF:
            header = data[i: i + 4]
            size = frame_size(header)
            if size and size > 4 and i + size <= len(data):
                frames.append((header, data[i + 4: i + size]))
                i += size
                continue
        i += 1
    return frames


def encode_bytes(data: bytes) -> str:
    """Encode arbitrary bytes to Base95 (4 bytes → 5 chars, no length prefix)."""
    pad = (4 - len(data) % 4) % 4
    padded = data + b"\x00" * pad
    result = []
    for i in range(0, len(padded), 4):
        n = int.from_bytes(padded[i: i + 4], "big")
        group = []
        for _ in range(5):
            group.append(ALPHABET[n % 95])
            n //= 95
        result.append("".join(reversed(group)))
    return "".join(result)


def main():
    parser = argparse.ArgumentParser(description="Encode MP3 frame payloads to Base95 JSON.")
    parser.add_argument("input_dir", help="Directory containing .mp3 files")
    parser.add_argument("output_dir", help="Directory to write per-file .json output")
    parser.add_argument("--max-frames", type=int, default=115,
                        help="Max frames per file (default 115 ≈ 3 s at 32 kbps/44100 Hz)")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.is_dir():
        print(f"Error: {input_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(input_dir.glob("*.mp3"))
    if not files:
        print(f"No .mp3 files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    for mp3_path in files:
        data = mp3_path.read_bytes()
        frames = parse_frames(data)[: args.max_frames]

        if not frames:
            print(f"  {mp3_path.name}: no valid MPEG1 Layer3 frames found — skipping", file=sys.stderr)
            continue

        # Use the most common header as the reconstruction template
        template_hex = Counter(h.hex() for h, _ in frames).most_common(1)[0][0]
        payload_size = len(frames[0][1])
        encoded_payloads = [encode_bytes(p) for _, p in frames]

        out = {
            "source": mp3_path.name,
            "template_header_hex": template_hex,
            "payload_size_bytes": payload_size,
            "payloads_b95": encoded_payloads,
        }
        out_path = output_dir / (mp3_path.stem + ".json")
        out_path.write_text(json.dumps(out, indent=2))

        chars = len(encoded_payloads[0]) if encoded_payloads else 0
        print(f"  {mp3_path.name} → {out_path.name}  "
              f"({len(frames)} frames × {payload_size} B payload → {chars} chars each)")


if __name__ == "__main__":
    main()
