# LLM Music Producer

**Status: in progress (week 12)**
**Code:** [code/gen-ai/agents/llm-music-producer/](../../code/gen-ai/agents/llm-music-producer/)
**Week:** [Week 12 — Mar 23](../weeks/week-12-2026-03-23.md)

---

## What it is

An experimental pipeline that treats an LLM as an audio composer. Real MP3 clips are encoded as Base95 text and fed to the LLM as examples; the LLM generates new audio payloads in Base95; the code reconstructs a valid MP3 and plays it.

The core hypothesis: if the LLM can identify statistical patterns in the Base95-encoded frame payloads, it may produce output that sounds similar to the inputs.

---

## How it works

### MP3 frame structure

Every MP3 file is a sequence of frames:

```
[4-byte header][audio payload]
```

- **Header** — sync word + bitrate + samplerate + channel flags. Fully deterministic for a fixed encoding — the code generates these, never the LLM.
- **Audio payload** — Huffman-coded spectral coefficients. This is what carries the actual sound, and what the LLM generates.

### Base95 encoding

Binary payload bytes are encoded as printable ASCII text using 95 characters (codes 32–126, space through `~`):

- Every 4 bytes → 5 characters (big-endian base-95)
- No length prefix — payload size is fixed per encoding configuration
- At 32 kbps / 44100 Hz mono: each frame payload is 83 bytes → 105 Base95 chars

### Pipeline

```
MP3 files
  → encode.py: parse frames, strip headers, encode payloads as Base95 JSON
  → LLM (via agentskills.io skill): read encoded payloads, synthesize new ones
  → decode.py: decode Base95 payloads, prepend deterministic headers, write MP3
  → open output.mp3
```

### Agent skill

The full pipeline is packaged as an [agentskills.io](https://agentskills.io) skill (`skills/llm-music-producer/SKILL.md`), compatible with Claude Code and other skill-aware agents. The skill instructs the agent to:

1. Run `encode.py` on the input MP3 directory
2. Read 3 JSON files, studying the first 10 frame payloads from each
3. Synthesize 77 new payloads (≈ 2 seconds) in context — no helper scripts
4. Write `output.json` and run `decode.py` to reconstruct the MP3
5. Play the result

---

## Design decisions

**Why strip the headers?** Asking the LLM to generate valid MP3 sync bytes (`0xFF 0xFB...`) is fragile — even one wrong byte breaks the frame. Generating them deterministically in code guarantees structural validity regardless of what the LLM produces.

**Why Base95 over Base64?** Base95 uses all 95 printable ASCII characters, offering better bit density (~6.57 bits/char vs 6 for Base64) and keeping the encoded data within a single text format the LLM handles naturally.

**Why not MIDI-as-text?** MIDI would be more semantically meaningful to the LLM, but requires a full audio-to-MIDI transcription step (e.g. Spotify's `basic-pitch`). The Base95 frame payload approach is a deliberate experiment: can the LLM learn patterns directly from compressed audio representations without any symbolic intermediate?

**Target encoding parameters:** 32 kbps, 44100 Hz, mono (MPEG1 Layer3). Stereo or non-standard sample rates increase frame size significantly, making LLM generation slower.

---

## Test audio

Bird recordings from Freesound, trimmed to 3-second clips at 32 kbps mono 44100 Hz:

- `resources/audio/birds/` — originals (immutable)
- `resources/audio/birds-3s-32kbps/` — 3s clips, stereo 24000 Hz (first attempt)
- `resources/audio/birds-3s-32kbps-mono/` — 3s clips, mono 44100 Hz (current, optimal for LLM generation)

---

## Status

Basic pipeline working end-to-end. Output MP3 plays for the full duration but sounds like noise — expected, as the LLM is pattern-matching on compressed spectral data without musical semantics. Continuing next session to evaluate quality and iterate.

→ See also: [LLM Wiki](../tools/llm-wiki.md) (same week AI learning)
