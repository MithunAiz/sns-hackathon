"""
backend/app.py
Flask API for the Personal Executive Agent.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
from flask_cors import CORS
from agent.agent import run_agent

app = Flask(__name__)
CORS(app)

# Store conversation history per session
sessions = {}


@app.route("/")
def home():
    return jsonify({"status": "Agent API running", "version": "1.0"})


@app.route("/ask", methods=["POST"])
def ask():
    """Main endpoint — accepts a query and returns agent answer."""
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Missing query field"}), 400

    query = data["query"]
    session_id = data.get("session_id", "default")

    # Get or create conversation history for this session
    if session_id not in sessions:
        sessions[session_id] = []

    try:
        result = run_agent(query, sessions[session_id])
        sessions[session_id] = result["history"]

        return jsonify({
            "answer": result["answer"],
            "sources": result["sources"],
            "session_id": session_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/reset", methods=["POST"])
def reset():
    """Reset conversation history for a session."""
    data = request.get_json()
    session_id = data.get("session_id", "default")
    sessions[session_id] = []
    return jsonify({"message": "Session reset successfully"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)