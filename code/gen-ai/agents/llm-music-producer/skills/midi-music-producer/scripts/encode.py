#!/usr/bin/env python3
"""Transcribe MP3 files to MIDI-as-text using basic-pitch.

Pipeline:
  MP3 → basic-pitch (audio-to-MIDI transcription) → pretty_midi (parse) → MIDI-as-text

MIDI-as-text format (one event per line):
  BPM <tempo>
  <time_s> <note_name> <velocity> <duration_s>

Example:
  BPM 145.0
  0.012 C6 72 0.089
  0.134 E6 68 0.076
  0.261 C6 85 0.100

Note names use scientific pitch notation: C4 = middle C (MIDI 60).
Velocity is 1–127. Duration is in seconds.

Usage:
    python3.11 encode.py <input_dir> <output_dir> [--max-duration 2.0]
"""

import argparse
import sys
from pathlib import Path

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def midi_num_to_name(n: int) -> str:
    return f"{NOTE_NAMES[n % 12]}{(n // 12) - 1}"


def transcribe(mp3_path: Path, max_duration: float) -> str:
    from basic_pitch.inference import predict
    from basic_pitch import ICASSP_2022_MODEL_PATH

    _, midi_data, _ = predict(
        str(mp3_path),
        ICASSP_2022_MODEL_PATH,
        onset_threshold=0.3,
        frame_threshold=0.2,
        minimum_note_length=30,
    )

    try:
        tempo = midi_data.estimate_tempo()
        if not (40 <= tempo <= 300):
            tempo = 120.0
    except Exception:
        tempo = 120.0

    notes = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            if note.start >= max_duration:
                continue
            end = min(note.end, max_duration)
            notes.append((note.start, note.pitch, note.velocity, end - note.start))

    notes.sort(key=lambda n: n[0])

    lines = [f"BPM {tempo:.1f}"]
    for start, pitch, velocity, duration in notes:
        lines.append(f"{start:.3f} {midi_num_to_name(pitch)} {velocity} {duration:.3f}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Transcribe MP3 files to MIDI-as-text.")
    parser.add_argument("input_dir", help="Directory containing .mp3 files")
    parser.add_argument("output_dir", help="Directory to write .txt files")
    parser.add_argument("--max-duration", type=float, default=2.0,
                        help="Max duration to transcribe in seconds (default: 2.0)")
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
        try:
            print(f"  Transcribing {mp3_path.name}...", end=" ", flush=True)
            midi_text = transcribe(mp3_path, args.max_duration)
            note_count = sum(1 for line in midi_text.splitlines() if line and not line.startswith("BPM"))
            out_path = output_dir / (mp3_path.stem + ".txt")
            out_path.write_text(midi_text)
            print(f"→ {out_path.name}  ({note_count} notes)")
        except Exception as e:
            print(f"error — {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
