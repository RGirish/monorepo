# Tool-Augmented LLM

A minimal chatbot that uses local LLM with tool calling capabilities.

## Setup

```bash
pip install huggingface_hub
```

Start local LLM server on `localhost:1234` (tested with `mistralai/mistral-7b-instruct-v0.3` on LM Studio)

## Usage

```bash
python main.py
```

Ask about weather and the bot will call the appropriate tool.

## Structure

- `main.py` - Main chat loop
- `tools.py` - Tool definitions
- `config.py` - System prompt