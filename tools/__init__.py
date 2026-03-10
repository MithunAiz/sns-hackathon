"""
tools/__init__.py
-----------------
Public interface for the Context-Aware Personal Executive Agent tool layer.

Exports all four search functions so the agent module can import them
from a single location:

    from tools import search_email, search_notes, search_csv, search_pdf

Each function accepts a natural language query string and returns results
from the corresponding simulated data source.
"""

from tools.email_search import search_email
from tools.notes_search import search_notes
from tools.csv_search import search_csv
from tools.pdf_search import search_pdf

__all__ = [
    "search_email",
    "search_notes",
    "search_csv",
    "search_pdf",
]
