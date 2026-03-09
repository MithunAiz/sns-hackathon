"""
Centralized configuration for the Context-Aware Personal Executive Agent.
Loads settings from environment variables (.env file).
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Paths
DATA_PATH = os.path.join(os.path.dirname(__file__), "data")

# Telegram API
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
