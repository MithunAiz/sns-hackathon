"""
Telegram Bot Runner — Polling Mode
Runs alongside the Flask server and polls Telegram for new messages.
No ngrok or public URL required!

Usage:
    python telegram_bot_runner.py
"""
import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from agent.agent import ExecutiveAgent
from integrations.telegram_bot import parse_telegram_update, send_telegram_message

# ===== Import the fallback engine from app.py =====
# We replicate the import chain so the bot has access to the same Q&A engine
from app import keyword_search_fallback

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def get_bot_info():
    """Verify the bot token works and get bot username."""
    r = requests.get(f"{TELEGRAM_API}/getMe", timeout=10)
    if r.status_code == 200 and r.json().get("ok"):
        bot = r.json()["result"]
        return bot.get("username"), bot.get("first_name")
    return None, None


def get_updates(offset=None):
    """Long-poll Telegram for new updates."""
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(f"{TELEGRAM_API}/getUpdates", params=params, timeout=35)
        if r.status_code == 200:
            return r.json().get("result", [])
    except requests.RequestException as e:
        print(f"[Poll] Error: {e}")
        time.sleep(5)
    return []


def process_message(update, agent):
    """Process a single Telegram update."""
    chat_id, text = parse_telegram_update(update)
    if not chat_id or not text:
        return
    
    print(f"[Bot] Message from {chat_id}: {text}")
    
    # Handle /start
    if text.strip() == "/start":
        welcome = (
            "👋 Hello! I'm your *Executive Assistant Bot*.\n\n"
            "I can search across emails, meeting notes, guest lists, "
            "chat logs, task trackers, and event plans.\n\n"
            "Just ask me anything! For example:\n"
            "• _Who is the keynote speaker?_\n"
            "• _What tasks are pending?_\n"
            "• _What did the team chat about logistics?_\n"
            "• _What is the event schedule?_\n"
            "• _What is the budget?_"
        )
        send_telegram_message(TELEGRAM_BOT_TOKEN, chat_id, welcome)
        return
    
    # Try AI agent
    session_id = f"telegram_{chat_id}"
    answer = None
    
    if agent:
        answer = agent.ask(session_id, text)
        is_error = any(phrase in answer.lower() for phrase in [
            "all 4 models are currently unavailable",
            "an error occurred after",
            "quota exceeded",
            "rate limit"
        ])
        if is_error:
            answer = None
    
    # Fallback to keyword search
    if not answer:
        answer = keyword_search_fallback(text)
    
    # Convert markdown for Telegram (** → *)
    telegram_text = answer.replace("**", "*")
    
    send_telegram_message(TELEGRAM_BOT_TOKEN, chat_id, telegram_text)
    print(f"[Bot] Replied to {chat_id}")


def main():
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set in .env file!")
        sys.exit(1)
    
    # Verify bot
    username, name = get_bot_info()
    if not username:
        print("ERROR: Invalid bot token! Could not connect to Telegram.")
        sys.exit(1)
    
    print(f"{'='*50}")
    print(f"  Telegram Bot Active!")
    print(f"  Bot: @{username} ({name})")
    print(f"  Mode: Long Polling")
    print(f"  Open Telegram and message @{username}")
    print(f"{'='*50}")
    
    # Initialize AI agent
    try:
        agent = ExecutiveAgent()
        print("[Bot] AI Agent initialized successfully.")
    except Exception as e:
        print(f"[Bot] AI Agent failed to init: {e}")
        print("[Bot] Running in keyword-only fallback mode.")
        agent = None
    
    # Polling loop
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                offset = update["update_id"] + 1
                process_message(update, agent)
        except KeyboardInterrupt:
            print("\n[Bot] Shutting down...")
            break
        except Exception as e:
            print(f"[Bot] Unexpected error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
