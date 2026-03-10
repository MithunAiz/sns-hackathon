"""
backend/routes.py
Flask API route definitions for the Executive Agent.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Blueprint, request, jsonify
from agent import run_agent
from backend.server_config import ACTIVE_CONFIG

# Blueprint for all agent routes
agent_bp = Blueprint("agent", __name__)

# In-memory session store  { session_id: [conversation_history] }
sessions = {}


@agent_bp.route("/ask", methods=["POST"])
def ask():
    """
    Main query endpoint.

    Request body:
        { "query": "What did we decide about catering?",
          "session_id": "user_123" }

    Response:
        { "answer": "...", "sources": [...], "session_id": "..." }
    """
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Missing required field: query"}), 400

    query      = data["query"].strip()
    session_id = data.get("session_id", ACTIVE_CONFIG.DEFAULT_SESSION_ID)

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Get or create conversation history for this session
    if session_id not in sessions:
        sessions[session_id] = []

    # Trim history if too long
    if len(sessions[session_id]) > ACTIVE_CONFIG.MAX_HISTORY_LENGTH:
        sessions[session_id] = sessions[session_id][-ACTIVE_CONFIG.MAX_HISTORY_LENGTH:]

    try:
        result = run_agent(query, sessions[session_id])
        sessions[session_id] = result["history"]

        return jsonify({
            "answer":     result["answer"],
            "sources":    result["sources"],
            "session_id": session_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@agent_bp.route("/reset", methods=["POST"])
def reset():
    """
    Reset conversation history for a session.

    Request body:
        { "session_id": "user_123" }
    """
    data       = request.get_json() or {}
    session_id = data.get("session_id", ACTIVE_CONFIG.DEFAULT_SESSION_ID)
    sessions[session_id] = []
    return jsonify({"message": "Session reset", "session_id": session_id})


@agent_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status":  "healthy",
        "version": ACTIVE_CONFIG.API_VERSION,
        "title":   ACTIVE_CONFIG.API_TITLE
    })


@agent_bp.route("/sessions", methods=["GET"])
def list_sessions():
    """List all active sessions (for debugging)."""
    return jsonify({
        "active_sessions": list(sessions.keys()),
        "count": len(sessions)
    })

def register_routes(app):
    """Register all blueprints with the Flask app."""
    from flask_cors import CORS
    CORS(app)
    app.register_blueprint(agent_bp)