# SNS Hackathon Executive Assistant

Context-aware assistant with two interfaces:
- Web app (`Flask` + vanilla frontend)
- Telegram bot (long-polling)

Data and response strategy:
- Real-time Gmail API search is used first for email-style queries.
- If AI/model path fails or is rate-limited, deterministic keyword fallback logic answers from local project data.
- If Gmail returns nothing or auth fails, offline `data/emails.json` fallback is used.

## Features

- Real-time Gmail search with advanced query parsing (`after:`, `before:`, `from:`, `has:attachment`, `filename:pdf`)
- Telegram bot integration for chat access
- Web chat interface for browser usage
- Tool-based retrieval from:
  - Emails (`data/emails.json`)
  - Meeting notes (`data/meeting_notes.txt`)
  - Guest list (`data/guests.csv`)
  - Event/task/chat files
- Rule-based fallback coverage for event questions (speaker, budget, venue, transport, schedule, tasks, RSVP, etc.)

## Project Structure

- `app.py`: Flask app, `/ask` endpoint, Gmail query parser, fallback engine
- `telegram_bot_runner.py`: Telegram polling runner
- `agent/`: AI agent + tool registry
- `tools/`: Source-specific retrieval tools
- `integrations/`: Gmail and Telegram integrations
- `frontend/`: Web UI assets
- `data/`: Offline fallback data

## Prerequisites

- Python 3.10+
- Gmail OAuth credentials (`config/credentials.json`) for real-time Gmail search
- Telegram bot token (for Telegram interface)

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create your local environment file:
```bash
copy .env.example .env
```

4. Fill `.env` values:
```env
GEMINI_API_KEY=...
TELEGRAM_BOT_TOKEN=...
GROK_API_KEY=...
```

5. Ensure Gmail OAuth files are present (not committed to git):
- `config/credentials.json`
- `config/token.json` (generated after auth)

## Run

Web app:
```bash
python app.py
```
Open `http://localhost:5000`

Telegram bot:
```bash
python telegram_bot_runner.py
```

Run both (separate terminals) for full experience.

## Fallback Behavior

- AI path attempted first (when available)
- If AI response indicates quota/rate-limit/model failure, fallback engine runs
- Email queries stay Gmail-first
- If Gmail result is empty/auth error, offline email fallback searches `data/emails.json`
- Temporal parsing supports phrases like `yesterday` and maps them to a precise Gmail date window

## Security and Git Hygiene

Ignored by `.gitignore`:
- `.env` and `.env.*` (except `.env.example`)
- OAuth secrets and tokens in `config/`
- virtual env folders, caches, logs, editor folders

Do not commit:
- `.env`
- `config/credentials.json`
- `config/token.json`

## Quick Test Queries

- `show me emails from yesterday`
- `show me emails from hr@company.com yesterday`
- `what tasks are pending`
- `who is the keynote speaker`
- `what is the budget`
