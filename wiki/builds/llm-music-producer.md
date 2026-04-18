# LLM Music Producer

**Status: complete (week 12)**
**Code:** [code/gen-ai/agents/llm-music-producer/](../../code/gen-ai/agents/llm-music-producer/)
**Week:** [Week 12 — Mar 23](../weeks/week-12-2026-03-23.md)

---

## What it is

Two experimental pipelines that use an LLM as an audio composer. Both are packaged as [agentskills.io](https://agentskills.io) skills — the full encode → compose → decode pipeline runs inside an agent's context window with no external model calls.

The project explores two fundamentally different representations of audio for LLM consumption: raw compressed bytes (Base95) and symbolic note events (MIDI-as-text).

---

## Approach 1: Base95 frame payloads

### How it works

Every MP3 file is a sequence of frames with the structure `[4-byte header][audio payload]`. Headers are fully deterministic for a fixed encoding configuration (bitrate, sample rate, channel mode) — so the code generates them, never the LLM. The LLM only generates the audio payload bytes (Huffman-coded spectral coefficients).

Binary payloads are encoded as printable ASCII using 95 characters (codes 32–126):

- Every 4 bytes → 5 characters (big-endian base-95)
- At 32 kbps / 44100 Hz mono: each frame payload is 83 bytes → 105 Base95 chars
- 77 frames ≈ 2 seconds of audio

Pipeline:
```
MP3 files
  → encode.py: parse frames, strip headers, encode payloads as Base95 JSON
  → LLM skill: read 3 input files (10 payloads each), synthesize 77 new payloads
  → decode.py: decode Base95, zero main_data_begin field, prepend headers, write MP3
```

### Key fix: bit reservoir

MP3's bit reservoir lets a frame borrow bits from the next frame's payload buffer. The `main_data_begin` field (first 9 bits of side info) points back into that buffer. When generating frames independently, this field must be zeroed — otherwise the decoder tries to read audio data from a non-existent prior frame, causing silence or truncation after frame 1.

```python
def zero_main_data_begin(payload: bytes) -> bytes:
    p = bytearray(payload)
    if len(p) >= 2:
        p[0] = 0x00
        p[1] = p[1] & 0x7F
    return bytes(p)
```

### Result

Output MP3 plays for the full duration and is structurally valid. Audio sounds like noise — expected, since the LLM is pattern-matching on compressed spectral data with no musical semantics.

---

## Approach 2: MIDI-as-text

### How it works

MP3 files are transcribed to symbolic note events using Spotify's `basic-pitch` library (audio-to-MIDI). Notes are written as human-readable text, one per line:

```
BPM 145.0
0.012 C6 72 0.089
0.134 E6 68 0.076
0.261 C6 85 0.100
```

The LLM reads up to 3 transcribed files, studies pitch register, velocity, duration, and timing patterns, then composes 30–60 new notes for ~2 seconds entirely in context. The output is synthesized back to audio via `pretty_midi` → fluidsynth → ffmpeg.

### Key details

- `basic-pitch` thresholds must be lowered for non-musical audio (e.g. bird recordings): `onset_threshold=0.3`, `frame_threshold=0.2`, `minimum_note_length=30`
- Soundfont auto-detected from homebrew cellar, preferring clean ASCII filenames
- Python 3.11 (homebrew) required for ML dependencies; `setuptools==69.5.1` needed for `pkg_resources` compatibility

### Result

Output is musically coherent — the LLM can recognize pitch registers, apply rhythmic patterns, and generate notes that stylistically resemble the inputs. A genuine compositional result rather than noise.

---

## Skill packaging

Both pipelines are packaged as agentskills.io skills under `skills/`:

```
skills/
├── base95-music-producer/
│   ├── SKILL.md
│   └── scripts/
│       ├── encode.py
│       └── decode.py
└── midi-music-producer/
    ├── SKILL.md
    └── scripts/
        ├── encode.py
        └── decode.py
```

Both are symlinked into `.claude/skills/` so Claude Code discovers them automatically when launched from the project directory. The user selects which approach by describing it naturally.

---

## Design decisions

**Why strip MP3 headers?** One wrong byte in the sync word (`0xFF 0xFB...`) breaks the entire frame. Generating headers deterministically in code guarantees structural validity regardless of what the LLM produces.

**Why Base95 over Base64?** Better bit density (~6.57 bits/char vs 6 for Base64) and all characters are printable ASCII within a single tokenization-friendly range.

**Why mono 44100 Hz at 32 kbps?** Stereo or non-standard sample rates increase frame size, making LLM generation slower. Mono 44100 Hz at 32 kbps gives 105 chars/payload — fast enough for a 2-second generation in a single context window.

**Why MIDI-as-text beats Base95 for quality?** MIDI is semantically meaningful — pitch names, durations, and velocities are concepts the LLM was trained on. Base95-encoded spectral coefficients are not. The LLM can compose in MIDI space; it can only memorize statistics in Base95 space.

---

## Test audio

Bird recordings from Freesound, trimmed to 3-second clips:

- `resources/audio/birds/` — originals (immutable)
- `resources/audio/birds-3s-32kbps-mono/` — 3s clips, mono 44100 Hz, 32 kbps (used for Base95)
- `midi/encoded/` — MIDI-as-text transcriptions (2s max-duration)
- `midi/encoded-hq/` — MIDI-as-text transcriptions (5s max-duration, more notes)

→ See also: [LLM Wiki](../tools/llm-wiki.md) (same week AI learning)
