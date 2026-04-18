---
name: midi-music-producer
description: LLM-based music producer using MIDI-as-text. Transcribes MP3 files to note events, lets the LLM compose new music inspired by the patterns, then synthesizes back to MP3. Use when the user wants to generate new music using the MIDI approach.
compatibility: Requires python3.11, fluidsynth, ffmpeg, and basic-pitch/pretty_midi (pip install basic-pitch pretty_midi)
---

# MIDI Music Producer

**IMPORTANT: Do NOT write any new code files or scripts. All composition must happen directly in your context window — read the MIDI-as-text, reason about the musical patterns, and produce the output yourself.**

End-to-end pipeline: MP3 files → MIDI-as-text encoding → LLM composition → MIDI reconstruction → MP3 synthesis.

Unlike the Base95 approach, MIDI-as-text is semantically meaningful — the LLM can reason about pitch, rhythm, duration, and musical character, not just byte patterns.

## MIDI-as-text format

Each `.txt` file contains one note per line:

```
BPM 145.0
0.012 C6 72 0.089
0.134 E6 68 0.076
0.261 C6 85 0.100
```

Fields: `<time_seconds> <note_name> <velocity_1-127> <duration_seconds>`

Note names use scientific pitch notation — C4 is middle C (MIDI 60). Higher numbers = higher octave. `#` = sharp (e.g. `D#5`).

## Step 1 — Transcribe input MP3s to MIDI-as-text

The user will provide a directory of MP3 files. Run:

```bash
python3.11 skills/midi-music-producer/scripts/encode.py <input_mp3_dir> <midi_text_dir>
```

This writes one `.txt` file per MP3. Transcription may take 10–30 seconds per file.

## Step 2 — Study the musical patterns

Read up to 3 of the `.txt` files. Study:

- **Register**: what octave range do the notes sit in? (birds tend to be C5–C7)
- **Duration**: are notes short and staccato (< 0.1s) or longer?
- **Velocity**: loud and punchy or soft?
- **Timing**: are notes evenly spaced, or clustered in bursts?
- **Pitch intervals**: do notes step by semitones, jump by thirds/fifths, or repeat the same pitch?
- **Tempo (BPM)**: fast chirping or slower phrases?

## Step 3 — Compose a new piece

**Do this entirely in your context window. Do not write a script.**

Compose a new musical sequence of **30–60 notes** spanning approximately **2 seconds** that captures the musical character you observed. Use the same BPM as the primary input file.

Guidelines:
- Stay in the same register as the input (don't suddenly drop to C2)
- Match the rhythmic character — if inputs are rapid staccato, keep it rapid
- Vary pitches to create musical interest — small motifs, repetition with variation
- Velocity should reflect the energy of the source material

## Step 4 — Write output.txt

Write the composed sequence to a file named `output.txt` in the current working directory. Use the same format:

```
BPM <tempo from primary input>
<time> <note> <velocity> <duration>
...
```

Ensure times are monotonically increasing and no note starts before 0.0.

## Step 5 — Synthesize to MP3

```bash
python3.11 skills/midi-music-producer/scripts/decode.py output.txt output.mp3
```

## Step 6 — Play the result

```bash
open output.mp3
```

Report what the output sounds like — does it resemble the input character? Note the instrument used (Acoustic Grand Piano by default from the VintageDreamsWaves soundfont).
