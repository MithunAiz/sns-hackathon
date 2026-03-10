# DEVELOPER 4: Data Tools & Resources
# Tool to search through simulated email datasets.

import json
import os

# Absolute path to the data file, resolved relative to this file's location.
_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "emails.json")


def search_email(query: str) -> str:
    """
    Searches emails.json for emails whose subject or body contains any word
    from the query (case-insensitive).

    Returns a readable summary of matching emails, or a 'not found' message.
    """
    try:
        with open(_DATA_FILE, "r", encoding="utf-8") as f:
            emails = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return f"[email_search] Could not load emails data: {exc}"

    keywords = [w.lower() for w in query.split() if len(w) > 2]
    matches = []

    for email in emails:
        text = f"{email.get('subject', '')} {email.get('body', '')}".lower()
        if any(kw in text for kw in keywords):
            matches.append(
                f"From: {email.get('sender')} | Date: {email.get('date')}\n"
                f"Subject: {email.get('subject')}\n"
                f"Body: {email.get('body')}"
            )

    if not matches:
        return "No matching emails found."

    return "\n\n".join(matches)
