# ── app.py ────────────────────────────────────────────────────────────────────
# Main entry point for the Context-Aware Personal Executive Agent server.
#
# Responsibilities:
#   - Import the pre-configured Flask app from backend.server_config
#   - Register the backend blueprint (routes) from backend
#   - Start the development server
#
# Usage:
#   python app.py
#
# Default URL: http://localhost:5000
# ──────────────────────────────────────────────────────────────────────────────

import logging

# Import the Flask app instance and server settings created in server_config.
from backend.server_config import app, HOST, PORT, DEBUG_MODE

# Import the blueprint that holds all API route definitions.
from backend import backend_bp

logger = logging.getLogger(__name__)

# ── Register Routes ────────────────────────────────────────────────────────────
# Attaches all endpoints defined in backend/routes.py to the Flask app.
app.register_blueprint(backend_bp)

# ── Run Server ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Starting Context-Aware Personal Executive Agent...")
    print(f"\n  Context-Aware Personal Executive Agent")
    print(f"  Server running at http://localhost:{PORT}")
    print(f"  Debug mode: {DEBUG_MODE}\n")
    app.run(host=HOST, port=PORT, debug=DEBUG_MODE)
