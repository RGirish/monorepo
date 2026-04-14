---
name: llm-music-producer
description: Full pipeline for LLM-based audio generation from MP3 frame payloads. Encodes MP3 files to per-frame Base95 payloads, uses the LLM to synthesize new payloads inspired by the input patterns, reconstructs a valid MP3, and plays it. Use when the user wants to generate new audio inspired by a set of input MP3 files.
compatibility: Requires Python 3.10+ and ffmpeg
---

# LLM Music Producer

**IMPORTANT: Do NOT write any new code files, scripts, or helpers at any point. All synthesis must be done directly in your context window — read the encoded data, reason about the patterns, and produce the output JSON yourself.**

End-to-end pipeline: MP3 files → frame payload encoding → LLM synthesis → MP3 reconstruction → playback.

The key idea: MP3 frame headers are deterministic for a fixed bitrate/samplerate, so the code generates them. The LLM only handles the audio payload bytes — the Huffman-coded spectral data that actually carries the sound. By studying payload patterns across real clips, the LLM may reproduce similar-sounding content.

## MP3 frame structure (for reference)

```
[4-byte header] [side info] [audio payload ← this is what you generate]
```

- **Header**: sync word + bitrate + samplerate + channel flags — deterministic, code handles it
- **Side info**: scale factor pointers — included in the payload bytes you receive and generate
- **Audio payload**: Huffman-coded spectral coefficients — carries the actual sound character

## Step 1 — Encode input audio files

The user will provide a directory of MP3 files. Run:

```bash
python skills/llm-music-producer/scripts/encode.py <input_mp3_dir> <encoded_dir> --max-frames 77
```

This writes one `.json` file per MP3 into `<encoded_dir>`. Each JSON contains:
- `template_header_hex`: the 4-byte frame header (hex) to use for reconstruction
- `payload_size_bytes`: byte length of each payload
- `payloads_b95`: list of Base95-encoded frame payloads, one per frame

## Step 2 — Study the encoded payloads

Read only **3 of the JSON files** in `<encoded_dir>` — pick the 3 with the most frames. **Pick the file with the most frames (closest to 77) as your primary reference** — use its `template_header_hex` and `payload_size_bytes` for reconstruction.

From each JSON file, **only read and study the first 10 payloads** — do not load the full list. Those 10 frames are enough to understand the texture and character of each clip.

Each payload is one frame's audio data encoded in Base95:
- **Alphabet**: 95 printable ASCII chars in order — space (32) through `~` (126)
- **Chunk**: every 4 bytes → 5 chars, big-endian base-95; every 5 chars → 4 bytes
- **No length prefix** — all payloads decode to exactly `payload_size_bytes` bytes

Study the patterns across those 30 sample frames (10 per clip):
- What characters appear most frequently overall?
- Are there recurring 5-char groups (= recurring 4-byte patterns)?
- How do payloads shift across frames within a clip?
- How do the 3 clips differ from each other in character distribution?

## Step 3 — Synthesize new payloads

**Do this entirely in your context window. Do not write a script to do this for you.**

Generate exactly **77 new frame payloads** (≈ 2 seconds at 32 kbps / 44100 Hz) inspired by the patterns you observed. Use the primary reference file's `payload_size_bytes` to determine payload length. Each payload must:
- Be exactly `ceil(payload_size_bytes / 4) * 5` characters long
- Contain only printable ASCII characters (codes 32–126, space through `~`)
- Reflect the character distributions and recurring patterns you observed

Do not copy payloads verbatim — blend and vary them across the 77 frames.

## Step 4 — Write the output JSON

Write a file named `output.json` in the current working directory:

```json
{
  "source": "llm-generated",
  "template_header_hex": "<copy from primary reference JSON>",
  "payload_size_bytes": <copy from primary reference JSON>,
  "payloads_b95": [
    "<payload 1>",
    "<payload 2>",
    ...77 total...
  ]
}
```

## Step 5 — Reconstruct the MP3

```bash
python skills/llm-music-producer/scripts/decode.py output.json output.mp3
```

## Step 6 — Play the result

```bash
open output.mp3
```

Report how long the audio plays and whether it sounds like anything recognizable. If the player reports an error or the file is silent, note that too — this is an experimental synthesis.
