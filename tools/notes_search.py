# DEVELOPER 4: Data Tools & Resources
# Tool to do full text search over meeting notes.

import os

_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "meeting_notes.txt")


def search_notes(query: str) -> str:
    """
    Reads meeting_notes.txt and returns lines that contain any keyword from
    the query (case-insensitive).

    If no lines match, returns the full file content so the agent always has
    context to work with.
    """
    try:
        with open(_DATA_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f"[notes_search] Notes file not found at: {_DATA_FILE}"
    except Exception as exc:
        return f"[notes_search] Could not read notes: {exc}"

    keywords = [w.lower() for w in query.split() if len(w) > 2]
    matching_lines = [
        line.strip()
        for line in lines
        if line.strip() and any(kw in line.lower() for kw in keywords)
    ]

    if not matching_lines:
        # Return full notes so the agent still has context.
        return "".join(lines).strip()

    return "\n".join(matching_lines)
