# Ollama

**Link:** [ollama.com](https://ollama.com/)
**Covered in:** [Week 3](../weeks/week-03-2026-01-19.md)

---

## What It Is

Ollama is a tool for downloading and running large language models locally on your own hardware. It provides a simple CLI and a local HTTP API that mimics the OpenAI API format, making it easy to swap between local and remote models in agent frameworks. Supported models include Llama, Mistral, Gemma, Phi, and many others.

## Why Use It

- **Privacy** — all inference happens locally; no data leaves the machine
- **Cost** — no per-token API costs for development and experimentation
- **Offline** — works without an internet connection
- **Drop-in compatibility** — the API is compatible with OpenAI SDK conventions

## Usage with Strands Agents

Used in [week 3](../weeks/week-03-2026-01-19.md) to provide local model inference for the [Jarvis chatbot](../builds/jarvis-chatbot.md). Strands Agents can point at Ollama's local endpoint instead of a remote API, providing a fully local, zero-cost development environment for agent experimentation.

## Related Concepts

- [Strands Agents](strands-agents.md) — the agent framework used alongside Ollama
- [Jarvis Chatbot](../builds/jarvis-chatbot.md) — the first build using Strands + Ollama
