from flask import Flask, request, jsonify, render_template

# CREATE FLASK APP
# Developer 2 / Developer 1 Integration
app = Flask(__name__, template_folder='frontend', static_folder='frontend')

# REGISTER ROUTES
# To be implemented by Developer 2 in backend/routes.py
from backend.routes import register_routes
register_routes(app)

# RUN SERVER
if __name__ == '__main__':
    print("Starting Context-Aware Personal Executive Agent...")
    app.run(debug=True, port=5000)
