# ── server_config.py ──────────────────────────────────────────────────────────
# Initialises the Flask application, enables CORS, configures structured
# logging, and exposes server settings loaded from environment variables.
# Imported by app.py which registers routes and starts the server.
# ──────────────────────────────────────────────────────────────────────────────

import os
import logging

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load variables from a .env file (if present) into the environment.
load_dotenv()

# ── Structured Logging ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Server Settings ────────────────────────────────────────────────────────────
DEBUG_MODE = os.getenv("DEBUG", "true").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))

# Optional LLM API keys — read from environment / .env file.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ── Flask App ──────────────────────────────────────────────────────────────────
# template_folder / static_folder point to the shared frontend directory.
app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend",
)
app.config["DEBUG"] = DEBUG_MODE

# ── CORS ───────────────────────────────────────────────────────────────────────
# Allow all origins so the frontend (served on any port) can reach the API.
CORS(app, resources={r"/*": {"origins": "*"}})

logger.info("Flask app initialised — CORS enabled, server will run on %s:%s", HOST, PORT)
