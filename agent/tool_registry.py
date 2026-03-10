"""
agent/tool_registry.py
Defines all tools available to the AI agent (Anthropic function calling format).
"""

TOOL_REGISTRY = [
    {
        "name": "search_email",
        "description": (
            "Search through emails for vendor confirmations, speaker details, "
            "transport arrangements, marketing decisions, or any event communication."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The keyword or phrase to search for in emails"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_notes",
        "description": (
            "Search meeting notes for decisions made, action items, budget figures, "
            "logistics plans, venue details, or catering choices."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The keyword or phrase to search for in meeting notes"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_csv",
        "description": (
            "Search the guest list for attendee names, roles, RSVP status, "
            "dietary preferences, or affiliated organizations."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The keyword or phrase to search for in the guest list"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_pdf",
        "description": (
            "Search the official event plan PDF for the event schedule, sponsors, "
            "emergency contacts, transport info, or formal event documentation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The keyword or phrase to search for in the event PDF"
                }
            },
            "required": ["query"]
        }
    }
]