"""
tools/notes_search.py
---------------------
Tool for searching the meeting notes text file (data/meeting_notes.txt).
Used by the AI agent to find decisions, action items, and discussion points
from planning meetings.
"""

import os
from typing import List


# Path to the meeting notes file (relative to project root)
NOTES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "meeting_notes.txt")


def _load_notes() -> List[str]:
    """
    Read the meeting notes file and return its contents as a list of lines.

    Returns:
        List of strings, one per line of the meeting notes file.

    Raises:
        FileNotFoundError: If meeting_notes.txt does not exist at the expected path.
    """
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return f.readlines()


def search_notes(query: str) -> List[str]:
    """
    Search meeting notes for lines containing the given query string.

    Reads meeting_notes.txt line by line and returns every line that
    contains the query term. The search is case-insensitive and strips
    leading/trailing whitespace from each matched line before returning.

    Args:
        query (str): The search term or phrase to look for in the notes.

    Returns:
        List[str]: A list of matching lines from the meeting notes.
        Returns an empty list if no lines match.

    Example:
        >>> results = search_notes("catering")
        >>> for line in results:
        ...     print(line)
        'DECISION: GreenLeaf Catering selected after reviewing three vendor proposals.'
        'Cost: $42 per guest for full buffet'
    """
    lines = _load_notes()
    query_lower = query.lower().strip()

    matches = []
    for line in lines:
        # Case-insensitive match; skip blank lines
        if query_lower in line.lower() and line.strip():
            matches.append(line.strip())

    return matches