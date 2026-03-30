# AI Client Desktop

A simple desktop client for AI interactions using Python and Tkinter.
Connects to the OpenAI API so you can send prompts and view responses directly
from your desktop.

## Requirements

- Python 3.8+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your API key
cp .env.example .env
# Edit .env and replace the placeholder with your real OPENAI_API_KEY

# 3. Run the application
python main.py
```

## Usage

1. Type your prompt in the **Prompt** text box.
2. Click **Enviar** (or press **Ctrl+Enter**) to send the prompt to the AI.
3. The response will appear in the **Respuesta** area above.
4. Click **Limpiar** to clear both areas and start fresh.

## Error handling

The application handles the following situations gracefully:
- Empty prompt: shows a warning dialog.
- Missing or invalid API key: shows a descriptive error dialog.
- Network / API errors (rate limits, timeouts, etc.): shows an error dialog.

## Environment variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI secret key (required) |

Set these in a `.env` file in the project root (see `.env.example`).
