"""
tools/email_search.py
---------------------
Tool for searching the simulated email inbox (data/emails.json).
Used by the AI agent to retrieve email records relevant to a query.
"""

import json
import os
from typing import List, Dict, Any


# Path to the emails data file (relative to project root)
EMAILS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "emails.json")


def _load_emails() -> List[Dict[str, Any]]:
    """
    Load and return all email records from the JSON data file.

    Returns:
        List of email dictionaries loaded from emails.json.

    Raises:
        FileNotFoundError: If emails.json does not exist at the expected path.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    with open(EMAILS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def search_email(query: str) -> List[Dict[str, Any]]:
    """
    Search the email inbox for records matching the given query string.

    Performs a case-insensitive keyword search across both the 'subject'
    and 'body' fields of each email. Returns all emails where at least
    one of those fields contains the query string.

    Args:
        query (str): The search term or phrase to look for in emails.

    Returns:
        List[Dict[str, Any]]: A list of matching email records. Each record
        contains keys: id, subject, sender, to, date, body.
        Returns an empty list if no matches are found.

    Example:
        >>> results = search_email("catering")
        >>> for r in results:
        ...     print(r["subject"])
        'Catering Vendor Finalized - GreenLeaf Confirmed'
    """
    emails = _load_emails()
    query_lower = query.lower().strip()

    matches = []
    for email in emails:
        # Search in subject and body fields (case-insensitive)
        subject_match = query_lower in email.get("subject", "").lower()
        body_match = query_lower in email.get("body", "").lower()

        if subject_match or body_match:
            matches.append(email)

    return matches