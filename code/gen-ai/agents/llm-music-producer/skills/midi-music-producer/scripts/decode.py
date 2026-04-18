#!/usr/bin/env python3
"""Convert MIDI-as-text to MP3.

Pipeline:
  MIDI-as-text → pretty_midi (build MIDI) → fluidsynth (render WAV) → ffmpeg (MP3)

Usage:
    python3.11 decode.py <input.txt> <output.mp3> [--soundfont path.sf2] [--play]
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import pretty_midi

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Soundfont search paths (ordered by preference)
SOUNDFONT_CANDIDATES = [
    Path("/opt/homebrew/Cellar/fluid-synth/2.5.3/share/fluid-synth/sf2/VintageDreamsWaves-v2.sf2"),
    Path("/usr/local/share/soundfonts/FluidR3_GM.sf2"),
    Path("/usr/share/sounds/sf2/FluidR3_GM.sf2"),
    Path.home() / "soundfonts/FluidR3_GM.sf2",
]


def note_name_to_midi(name: str) -> int:
    """Convert note name (e.g. 'C5', 'D#4') to MIDI number."""
    if len(name) >= 3 and name[1] == '#':
        note, octave = name[:2], int(name[2:])
    else:
        note, octave = name[0], int(name[1:])
    return NOTE_NAMES.index(note) + (octave + 1) * 12


def parse_midi_text(text: str) -> pretty_midi.PrettyMIDI:
    """Parse MIDI-as-text into a PrettyMIDI object."""
    bpm = 120.0
    notes = []

    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('BPM'):
            try:
                bpm = float(line.split()[1])
            except (IndexError, ValueError):
                pass
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        try:
            start = float(parts[0])
            pitch = note_name_to_midi(parts[1])
            velocity = max(1, min(127, int(parts[2])))
            duration = max(0.03, float(parts[3]))
            notes.append((start, pitch, velocity, duration))
        except (ValueError, IndexError, KeyError):
            continue  # skip malformed lines gracefully

    midi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
    for start, pitch, velocity, duration in notes:
        instrument.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch,
            start=start, end=start + duration,
        ))
    midi.instruments.append(instrument)
    return midi


def find_soundfont() -> Path | None:
    # Search homebrew cellar, preferring clean ASCII filenames
    cellar = Path("/opt/homebrew/Cellar/fluid-synth")
    if cellar.exists():
        candidates = sorted(cellar.rglob("*.sf2"))
        for sf2 in candidates:
            if sf2.name.isascii():
                return sf2
        if candidates:
            return candidates[0]

    for p in SOUNDFONT_CANDIDATES:
        if p.exists():
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="Convert MIDI-as-text to MP3.")
    parser.add_argument("input_txt", help="MIDI-as-text file")
    parser.add_argument("output_mp3", help="Output .mp3 file")
    parser.add_argument("--soundfont", help="Path to .sf2 soundfont (auto-detected if omitted)")
    parser.add_argument("--play", action="store_true", help="Open in system audio player after writing")
    args = parser.parse_args()

    input_path = Path(args.input_txt)
    output_path = Path(args.output_mp3)

    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    soundfont = Path(args.soundfont) if args.soundfont else find_soundfont()
    if not soundfont or not soundfont.exists():
        print("Error: no soundfont found.", file=sys.stderr)
        print("  Download FluidR3_GM.sf2 and pass --soundfont <path>", file=sys.stderr)
        sys.exit(1)

    text = input_path.read_text()
    midi = parse_midi_text(text)
    note_count = sum(len(i.notes) for i in midi.instruments)
    print(f"  Parsed {note_count} notes  (soundfont: {soundfont.name})")

    with tempfile.TemporaryDirectory() as tmpdir:
        mid_path = Path(tmpdir) / "output.mid"
        wav_path = Path(tmpdir) / "output.wav"

        midi.write(str(mid_path))

        r = subprocess.run(
            ["fluidsynth", "-ni", "-F", str(wav_path), "-r", "44100", str(soundfont), str(mid_path)],
            capture_output=True, text=True,
        )
        if not wav_path.exists():
            print(f"Error: fluidsynth failed\n{r.stderr}", file=sys.stderr)
            sys.exit(1)

        r = subprocess.run(
            ["ffmpeg", "-i", str(wav_path), "-b:a", "32k", "-ar", "44100", "-ac", "1",
             str(output_path), "-y"],
            capture_output=True, text=True,
        )
        if not output_path.exists():
            print(f"Error: ffmpeg failed\n{r.stderr}", file=sys.stderr)
            sys.exit(1)

    print(f"  → {output_path}  ({output_path.stat().st_size:,} bytes)")

    if args.play:
        subprocess.run(["open", str(output_path)])


if __name__ == "__main__":
    main()
