# DEVELOPER 3: AI Agent Tool Registry
# Contains logic for registering tools and calling them dynamically.

# Integration with Tools (Developer 4)
from tools.email_search import search_email
from tools.pdf_search import search_pdf
from tools.csv_search import search_csv
from tools.notes_search import search_notes

def select_tool(question: str) -> str:
    """
    Uses logic (or an LLM) to decide which tool is best suited for the question.
    """
    # STUB: Simplistic keyword matching for mock purposes
    q_lower = question.lower()
    if 'email' in q_lower:
        return 'email_search'
    elif 'pdf' in q_lower or 'plan' in q_lower:
        return 'pdf_search'
    elif 'csv' in q_lower or 'guest' in q_lower:
        return 'csv_search'
    else:
        return 'notes_search'

def call_tool(tool_name: str, query: str) -> str:
    """
    Executes the specified tool with the query.
    """
    # STUB implementation
    if tool_name == 'email_search':
        return search_email(query)
    elif tool_name == 'pdf_search':
        return search_pdf(query)
    elif tool_name == 'csv_search':
        return search_csv(query)
    elif tool_name == 'notes_search':
        return search_notes(query)
    
    return "No matching tool found."
