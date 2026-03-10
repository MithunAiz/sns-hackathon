"""
backend/server_config.py
Central configuration for the Flask backend server.
"""

import os

class Config:
    """Base configuration."""

    # Flask settings
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "exec-agent-secret-key-2026")

    # CORS — allow frontend to call backend
    CORS_ORIGINS = ["*"]

    # Agent settings
    MAX_HISTORY_LENGTH = 20   # Max conversation turns to keep in memory
    DEFAULT_SESSION_ID  = "default"

    # API info
    API_VERSION = "1.0"
    API_TITLE   = "Context-Aware Personal Executive Agent API"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Active config — change to ProductionConfig for deployment
ACTIVE_CONFIG = DevelopmentConfig