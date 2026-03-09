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
