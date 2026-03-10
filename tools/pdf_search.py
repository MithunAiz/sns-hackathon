"""
tools/pdf_search.py
-------------------
Tool for searching the event plan PDF document (data/event_plan.pdf).
Uses pypdf to extract text from each page and returns sections that
match the given query string.
"""

import os
from typing import List

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None  # Graceful fallback if pypdf is not installed


# Path to the event plan PDF (relative to project root)
PDF_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "event_plan.pdf")

# Minimum characters a text chunk must have to be returned as a result
MIN_CHUNK_LENGTH = 20


def _extract_pdf_text() -> List[str]:
    """
    Extract text from all pages of the event plan PDF.

    Returns:
        List[str]: A list of non-empty text strings, one per PDF page.

    Raises:
        ImportError: If the pypdf library is not installed.
        FileNotFoundError: If event_plan.pdf does not exist at the expected path.
    """
    if PdfReader is None:
        raise ImportError(
            "pypdf is required for PDF search. Install it with: pip install pypdf"
        )

    reader = PdfReader(PDF_FILE)
    pages_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            pages_text.append(text.strip())

    return pages_text


def _split_into_chunks(text: str) -> List[str]:
    """
    Split a page's text into smaller searchable chunks (by paragraph/line).

    Args:
        text (str): Raw text extracted from a single PDF page.

    Returns:
        List[str]: Individual non-empty lines or paragraphs from the text.
    """
    # Split on double newlines (paragraphs) first, then single newlines
    chunks = []
    for paragraph in text.split("\n\n"):
        for line in paragraph.split("\n"):
            line = line.strip()
            if len(line) >= MIN_CHUNK_LENGTH:
                chunks.append(line)
    return chunks


def search_pdf(query: str) -> List[str]:
    """
    Search the event plan PDF for text sections matching the given query.

    Extracts text from all pages of the PDF, splits each page into
    chunks (lines/paragraphs), and returns chunks that contain the
    query string. The search is case-insensitive.

    Args:
        query (str): The search term or phrase to look for in the PDF.

    Returns:
        List[str]: A list of matching text sections from the PDF.
        Returns an empty list if no matches are found.
        If the PDF file is not found, returns a list with a single
        informative message string instead of raising an error.

    Example:
        >>> results = search_pdf("keynote speaker")
        >>> for r in results:
        ...     print(r)
        'Keynote Speaker: Dr. Ananya Krishnan — Responsible AI'
    """
    # Gracefully handle missing PDF file
    if not os.path.exists(PDF_FILE):
        return [
            "event_plan.pdf not found. Please add the PDF to the data/ folder. "
            "Expected content: venue details, catering vendor, guest count, "
            "transport arrangements, and keynote speaker information."
        ]

    pages_text = _extract_pdf_text()
    query_lower = query.lower().strip()

    matches = []
    for page_text in pages_text:
        chunks = _split_into_chunks(page_text)
        for chunk in chunks:
            if query_lower in chunk.lower():
                matches.append(chunk)

    return matches