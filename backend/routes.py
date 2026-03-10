# ── routes.py ─────────────────────────────────────────────────────────────────
# Defines all Flask API routes for the backend.
# Responsibilities:
#   - Parse and validate incoming JSON requests
#   - Forward the user question to the agent module
#   - Return structured JSON responses with appropriate HTTP status codes
# ──────────────────────────────────────────────────────────────────────────────

import logging

from flask import request, jsonify
from backend import backend_bp

# process_question is the sole public interface exposed by the agent module.
# The agent handles all AI reasoning — we only call it here.
from agent.agent import process_question

logger = logging.getLogger(__name__)


# ── Health Check ───────────────────────────────────────────────────────────────
@backend_bp.route("/", methods=["GET"])
def home():
    """Health-check endpoint — confirms the backend is reachable."""
    logger.info("GET / — health check requested")
    return jsonify({
        "status": "ok",
        "message": "Context-Aware Personal Executive Agent backend is running.",
    }), 200


# ── Ask Endpoint ───────────────────────────────────────────────────────────────
@backend_bp.route("/ask", methods=["POST"])
def ask_agent():
    """
    Receive a user question, forward it to the agent, and return the answer.

    Request body (JSON):
        { "question": "What did we decide about the event logistics?" }

    Success response (200):
        { "question": "...", "answer": "..." }

    Error responses:
        400 — missing or invalid JSON / missing 'question' field
        500 — unexpected error from the agent
    """
    logger.info("POST /ask — incoming request")

    # ── 1. Parse JSON body ─────────────────────────────────────────────────────
    # silent=True prevents Flask from raising a 400 on malformed JSON;
    # we handle the error ourselves for a consistent response format.
    data = request.get_json(silent=True)

    if not data:
        logger.warning("POST /ask — request body is missing or not valid JSON")
        return jsonify({"error": "Request body must be valid JSON."}), 400

    # ── 2. Validate input ──────────────────────────────────────────────────────
    question = data.get("question", "").strip()

    if not question:
        logger.warning("POST /ask — 'question' field is missing or empty")
        return jsonify({"error": "'question' field is required and must not be empty."}), 400

    logger.info("POST /ask — question: %s", question)

    # ── 3. Call the agent ──────────────────────────────────────────────────────
    try:
        answer = process_question(question)
        logger.info("POST /ask — agent responded successfully")

        # ── 4. Return structured JSON response ─────────────────────────────────
        return jsonify({
            "question": question,
            "answer": answer,
        }), 200

    except Exception as exc:
        # Log the full traceback for debugging; return a safe message to the client.
        logger.error("POST /ask — agent raised an exception: %s", exc, exc_info=True)
        return jsonify({
            "error": "An internal error occurred while processing your question.",
            "detail": str(exc),
        }), 500
