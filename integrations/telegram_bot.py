"""
Telegram Bot integration for the Context-Aware Personal Executive Agent.
Handles incoming webhook messages and sends responses back via Telegram Bot API.
"""
import requests
import os


TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}"


def get_api_url(token: str) -> str:
    """Returns the base Telegram API URL for the given bot token."""
    return TELEGRAM_API_BASE.format(token=token)


def parse_telegram_update(data: dict) -> tuple:
    """
    Parses a Telegram webhook update and extracts chat_id and message text.
    Returns (chat_id, text) or (None, None) if the update is not a text message.
    """
    try:
        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "").strip()
        
        if chat_id and text:
            return chat_id, text
        return None, None
    except Exception:
        return None, None


def send_telegram_message(token: str, chat_id: int, text: str) -> bool:
    """
    Sends a text message to a Telegram chat using the Bot API.
    Returns True if successful, False otherwise.
    """
    url = f"{get_api_url(token)}/sendMessage"
    
    # Telegram has a 4096 character limit per message
    MAX_LENGTH = 4000
    if len(text) > MAX_LENGTH:
        text = text[:MAX_LENGTH] + "\n\n... (message truncated)"
    
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            # Retry without markdown in case of formatting errors
            payload["parse_mode"] = ""
            response = requests.post(url, json=payload, timeout=10)
            print(f"[Telegram] Send message status: {response.status_code}")
            return response.status_code == 200
    except requests.RequestException as e:
        print(f"[Telegram] Error sending message: {e}")
        return False


def handle_telegram_message(data: dict, token: str, agent, fallback_fn) -> dict:
    """
    Full handler for a Telegram webhook update.
    
    1. Parses the incoming message
    2. Sends it to the AI agent (or fallback)
    3. Sends the response back to Telegram
    
    Returns a status dict.
    """
    chat_id, text = parse_telegram_update(data)
    
    if not chat_id or not text:
        return {"status": "ignored", "reason": "No valid text message found"}
    
    # Handle /start command
    if text == "/start":
        welcome = (
            "👋 Hello! I'm your *Executive Assistant Bot*.\n\n"
            "I can search across emails, meeting notes, guest lists, "
            "chat logs, task trackers, and event plans.\n\n"
            "Just ask me anything! For example:\n"
            "• _Who is the keynote speaker?_\n"
            "• _What tasks are pending?_\n"
            "• _What did the team chat about logistics?_\n"
            "• _What is the event schedule?_"
        )
        send_telegram_message(token, chat_id, welcome)
        return {"status": "ok", "action": "welcome_sent"}
    
    # Use Telegram chat_id as session_id for context persistence
    session_id = f"telegram_{chat_id}"
    
    # Try AI agent first
    answer = None
    if agent:
        answer = agent.ask(session_id, text)
        
        # Check if the AI returned an error
        is_error = any(phrase in answer.lower() for phrase in [
            "all 4 models are currently unavailable",
            "an error occurred after",
            "quota exceeded",
            "rate limit"
        ])
        
        if is_error:
            answer = None  # Fall back to keyword search
    
    # Fallback to keyword search if AI failed
    if not answer:
        answer = fallback_fn(text)
    
    # Clean markdown for Telegram (** → * for bold)
    telegram_text = answer.replace("**", "*")
    
    send_telegram_message(token, chat_id, telegram_text)
    
    return {"status": "ok", "chat_id": chat_id}
