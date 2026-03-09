import os
from pypdf import PdfReader

def search_pdf(query: str) -> str:
    """
    Use pypdf to read event_plan.pdf and search the extracted text for the query.
    Returns the relevant extracted text.
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'event_plan.pdf')
    try:
        reader = PdfReader(file_path)
    except FileNotFoundError:
        return "Error: event_plan.pdf not found."
        
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text() + "\n"
        
    if query.lower() in extracted_text.lower():
        # Keep it simple, return the extracted text block containing info
        return f"Found relevant information in event plan (PDF):\n\n{extracted_text}"
        
    return f"No matching information found in the event plan (PDF) for query: '{query}'"
