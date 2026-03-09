# DEVELOPER 2: Backend API
from flask import request, jsonify, render_template
# Integration point with Agent (Developer 3)
from agent.agent import process_question

def register_routes(app):
    
    # Serve Frontend UI
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/ask', methods=['POST'])
    def ask():
        # Responsibilities:
        # - process incoming requests
        # - call agent
        # - return response
        
        data = request.json
        question = data.get('question', '')

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # TODO: Call actual agent logic implemented by Developer 3
        # answer = process_question(question)
        
        # MOCK RESPONSE for now
        mock_answer = f"This is a placeholder answer for: '{question}'"
        
        return jsonify({"answer": mock_answer})
    
    # Catch-all to serve static files from frontend folder if needed
    @app.route('/<path:path>')
    def serve_static(path):
        from flask import send_from_directory
        import os
        return send_from_directory(os.path.join(app.root_path, 'frontend'), path)
