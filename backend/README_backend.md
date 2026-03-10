# Backend Module

## Overview
The backend handles communication between the frontend chat interface and the AI agent.

It receives user questions, processes them, and returns responses using REST APIs.

## Folder Structure

backend/
│
├── __init__.py          # Initializes backend module
├── routes.py            # Defines API endpoints
├── server_config.py     # Backend configuration settings
├── README_backend.md    # Backend documentation


## API Endpoints

GET /
- Checks if backend server is running.

POST /ask
- Accepts a question from the user.

Example Request:

{
 "question": "What did we decide about catering?"
}

Example Response:

{
 "question": "What did we decide about catering?",
 "answer": "Agent response will appear here."
}

## Technologies Used

- Python
- Flask
- REST API