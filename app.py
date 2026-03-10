import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='frontend')

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('frontend', path)

# Register backend routes
from backend.routes import register_routes
register_routes(app)

if __name__ == '__main__':
    print("Starting Context-Aware Personal Executive Agent...")
    app.run(debug=True, port=5000)