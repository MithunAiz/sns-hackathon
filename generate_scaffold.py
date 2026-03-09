import os

base_dir = r"c:\Users\Mithun R\.gemini\antigravity\scratch\sns-hackathon-2"

def write_file(rel_path, content):
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    # ROOT
    "app.py": """
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
    """,

    "requirements.txt": """
Flask
pandas
pypdf
python-dotenv
# google-generativeai  # LLM dependency commented out for now
    """,

    "README.md": """
# Context-Aware Personal Executive Agent

## Project Purpose
An AI assistant designed to answer user questions by searching across multiple simulated data sources (emails, meeting notes, CSV spreadsheets, and PDFs).

## Architecture Overview
User -> Frontend -> Backend -> Agent -> Tools -> Data

## Team Division
- **Developer 1 (Frontend):** Chat UI, sending messages to the backend, displaying responses.
- **Developer 2 (Backend API):** Flask routes, processing requests, calling the agent.
- **Developer 3 (AI Agent Logic):** Interpreting queries, selecting tools, generating answers.
- **Developer 4 (Data Tools & Sources):** Reading and searching simulated datasets.

## Instructions
Each developer should work within their respective module folder. Coordinate integration points (e.g., app.py and backend/routes.py) to ensure seamless communication. Look for the README in your specific folder for more details.
    """,

    # FRONTEND
    "frontend/index.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Executive Agent Chat</title>
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <!-- DEVELOPER 1: Build chat UI here -->
    <div id="chat-container">
        <h1>Context-Aware Executive Agent</h1>
        <div id="chat-history">
            <!-- Chat history will appear here -->
        </div>
        <div id="chat-input-area">
            <input type="text" id="user-input" placeholder="Ask a question (e.g., 'What did we decide about event logistics?')">
            <button id="send-btn" onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script src="/script.js"></script>
</body>
</html>
    """,

    "frontend/styles.css": """
/* DEVELOPER 1: Styling for the chat interface */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f4f4f9;
}

#chat-container {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

#chat-history {
    height: 400px;
    overflow-y: auto;
    border: 1px solid #ddd;
    margin-bottom: 20px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

#chat-input-area {
    display: flex;
    gap: 10px;
}

#user-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

#send-btn {
    padding: 10px 20px;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
}

.msg {
    padding: 8px 12px;
    border-radius: 8px;
    max-width: 80%;
}

.user-msg {
    background-color: #e3f2fd;
    align-self: flex-end;
}

.agent-msg {
    background-color: #f1f8e9;
    align-self: flex-start;
}
    """,

    "frontend/script.js": """
// DEVELOPER 1: Frontend Logic
// Responsibilities:
// - send user messages to backend
// - display assistant responses
// - maintain chat history

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (!message) return;

    // Display user message in chat history
    appendMessage('You', message, 'user-msg');
    userInput.value = '';

    // Placeholder POST request to /ask
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: message })
        });
        const data = await response.json();
        
        // Display AI response
        appendMessage('Agent', data.answer, 'agent-msg');
    } catch (error) {
        console.error('Error fetching response:', error);
        appendMessage('System', 'Error communicating with server.', 'agent-msg');
    }
}

function appendMessage(sender, text, className) {
    const chatHistory = document.getElementById('chat-history');
    const msgElement = document.createElement('div');
    msgElement.className = `msg ${className}`;
    msgElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatHistory.appendChild(msgElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}
    """,

    "frontend/README_frontend.md": """
# Frontend Module (Developer 1)
Responsibilities: build chat UI, send user messages to backend, display assistant responses, maintain chat history.
    """,

    # BACKEND
    "backend/routes.py": """
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
    """,

    "backend/server_config.py": """
# DEVELOPER 2: Server Configuration
# Contains constants, API configurations, or environment variable loadings.

import os

DEBUG_MODE = True
PORT = 5000

# Load .env variables (if needed later)
# from dotenv import load_dotenv
# load_dotenv()
    """,

    "backend/README_backend.md": """
# Backend Module (Developer 2)
Responsibilities: create Flask routes, process incoming requests, call agent, return response.
    """,

    # AGENT
    "agent/agent.py": """
# DEVELOPER 3: AI Agent Logic
# Responsibilities:
# - interpret user queries
# - select appropriate tool
# - call tool functions
# - generate final answer using LLM

from agent.tool_registry import select_tool, call_tool

def process_question(question: str) -> str:
    \"\"\"
    Main entry point for evaluating a user question.
    Expected workflow:
    1. Understand query
    2. Select Tool
    3. Query Data Source
    4. Compile Final Answer
    \"\"\"
    
    # STUB IMPLEMENTATION
    tool_name = select_tool(question)
    tool_result = call_tool(tool_name, question)
    
    # TODO: Pass the result to an LLM to generate natural language answer
    final_answer = f"[Agent processed via {tool_name}] Found data: {tool_result}"
    return final_answer
    """,

    "agent/tool_registry.py": """
# DEVELOPER 3: AI Agent Tool Registry
# Contains logic for registering tools and calling them dynamically.

# Integration with Tools (Developer 4)
from tools.email_search import search_email
from tools.pdf_search import search_pdf
from tools.csv_search import search_csv
from tools.notes_search import search_notes

def select_tool(question: str) -> str:
    \"\"\"
    Uses logic (or an LLM) to decide which tool is best suited for the question.
    \"\"\"
    # STUB: Simplistic keyword matching for mock purposes
    q_lower = question.lower()
    if 'email' in q_lower:
        return 'email_search'
    elif 'pdf' in q_lower or 'plan' in q_lower:
        return 'pdf_search'
    elif 'csv' in q_lower or 'guest' in q_lower:
        return 'csv_search'
    else:
        return 'notes_search'

def call_tool(tool_name: str, query: str) -> str:
    \"\"\"
    Executes the specified tool with the query.
    \"\"\"
    # STUB implementation
    if tool_name == 'email_search':
        return search_email(query)
    elif tool_name == 'pdf_search':
        return search_pdf(query)
    elif tool_name == 'csv_search':
        return search_csv(query)
    elif tool_name == 'notes_search':
        return search_notes(query)
    
    return "No matching tool found."
    """,

    "agent/README_agent.md": """
# Agent Module (Developer 3)
Responsibilities: interpret user queries, select appropriate tool, call tool functions, generate final answer using LLM.
    """,

    # TOOLS
    "tools/email_search.py": """
# DEVELOPER 4: Data Tools & Resources
# Tool to search through simulated email datasets.

import json
import os

def search_email(query: str) -> str:
    \"\"\"
    Searches the emails.json data source.
    \"\"\"
    # STUB implementation
    return "Mock email search result for query: " + query
    """,

    "tools/pdf_search.py": """
# DEVELOPER 4: Data Tools & Resources
# Tool to parse and search through PDF files.

def search_pdf(query: str) -> str:
    \"\"\"
    Searches the event_plan.pdf data source.
    \"\"\"
    # STUB implementation
    return "Mock PDF search result for query: " + query
    """,

    "tools/csv_search.py": """
# DEVELOPER 4: Data Tools & Resources
# Tool to search and filter CSV structures.

import pandas as pd

def search_csv(query: str) -> str:
    \"\"\"
    Searches the guests.csv data source.
    \"\"\"
    # STUB implementation
    return "Mock CSV search result for query: " + query
    """,

    "tools/notes_search.py": """
# DEVELOPER 4: Data Tools & Resources
# Tool to do full text search over meeting notes.

def search_notes(query: str) -> str:
    \"\"\"
    Searches the meeting_notes.txt data source.
    \"\"\"
    # STUB implementation
    return "Mock meeting notes search result for query: " + query
    """,

    "tools/README_tools.md": """
# Tools Module (Developer 4)
Responsibilities: execute searches over various document types (email, pdf, csv, text), retrieve relevant segments.
    """,

    # DATA
    "data/emails.json": """
[
    {
        "id": 1,
        "sender": "boss@example.com",
        "subject": "Event logistics",
        "body": "Let's make sure the caterer brings vegetarian options.",
        "date": "2023-10-01"
    }
]
    """,

    "data/meeting_notes.txt": """
Meeting Date: 2023-10-02
Attendees: Alice, Bob, Charlie
Notes:
- The Q3 review will be held next Tuesday.
- We need to confirm the venue booking by Friday.
- Budget constraints mean we can't afford the live band requested.
    """,

    "data/guests.csv": """
Name,Email,VIP,Status
Alice Smith,alice@example.com,Yes,Confirmed
Bob Jones,bob@example.com,No,Pending
Charlie Brown,charlie@example.com,Yes,Declined
    """,

    "data/event_plan.pdf": """
%PDF-1.4
%This is a stub placeholder for a real PDF.
%In reality pypdf would be parsing binary pdf data here.
(Event Plan 2024: The main theme is Technology and Innovation.)
    """,

    "data/README_data.md": """
# Data Module
Contains simulated/mock data files for the system to search over.
    """,
    
    # EXTRA init files to avoid import errors
    "backend/__init__.py": "",
    "agent/__init__.py": "",
    "tools/__init__.py": "",
}

for rel, path_content in files.items():
    write_file(rel, path_content)

print("Scaffold successfully generated!")
