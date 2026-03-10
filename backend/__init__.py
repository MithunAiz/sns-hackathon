from flask import Blueprint

backend_bp = Blueprint("backend", __name__)

from backend import routes