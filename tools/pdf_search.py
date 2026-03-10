# DEVELOPER 4: Data Tools & Resources
# Tool to parse and search through PDF files.

import os

_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "event_plan.pdf")


def search_pdf(query: str) -> str:
    """
    Extracts text from event_plan.pdf using pypdf and returns lines that
    contain any keyword from the query (case-insensitive).

    Returns matching lines, or a 'not found' message.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        return "[pdf_search] pypdf is not installed. Run: pip install pypdf"

    try:
        reader = PdfReader(_DATA_FILE)
    except FileNotFoundError:
        return f"[pdf_search] PDF file not found at: {_DATA_FILE}"
    except Exception as exc:
        return f"[pdf_search] Could not open PDF: {exc}"

    # Extract all text from every page.
    full_text = "\n".join(
        page.extract_text() or "" for page in reader.pages
    )

    keywords = [w.lower() for w in query.split() if len(w) > 2]
    matching_lines = [
        line.strip()
        for line in full_text.splitlines()
        if line.strip() and any(kw in line.lower() for kw in keywords)
    ]

    if not matching_lines:
        return "No relevant content found in the event plan PDF."

    return "\n".join(matching_lines)
