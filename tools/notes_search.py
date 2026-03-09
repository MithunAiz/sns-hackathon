import os

def search_notes(query: str) -> str:
    """
    Search meeting_notes.txt for relevant lines based on the query.
    Returns the matched context or an indication if no match was found.
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'meeting_notes.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "Error: meeting_notes.txt not found."

    results = []
    query_lower = query.lower()
    
    # Simple search: return the whole document if query is broad, or specific lines.
    # Since notes are short, we return matches with some surrounding context, or just the whole note if it matches.
    
    document = "".join(lines)
    if query_lower in document.lower():
         return f"Found relevant information in meeting notes:\n\n{document}"
        
    return f"No notes found matching query: '{query}'"
