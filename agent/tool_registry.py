# DEVELOPER 3: AI Agent Tool Registry
# Contains logic for registering tools and calling them dynamically.

# Integration with Tools (Developer 4)
from tools.email_search import search_email
from tools.pdf_search import search_pdf
from tools.csv_search import search_csv
from tools.notes_search import search_notes

def select_tool(question: str) -> str:
    """
    Uses keyword matching to decide which tool is best suited for the question.
    Checks against expanded keyword sets for each data source.
    """
    q_lower = question.lower()

    # Email data source — emails, messages, senders, inbox keywords
    EMAIL_KEYWORDS = {'email', 'mail', 'inbox', 'message', 'sender', 'received', 'caterer', 'logistics'}
    if any(kw in q_lower for kw in EMAIL_KEYWORDS):
        return 'email_search'

    # PDF data source — event plan, venue, schedule, budget, logistics document
    PDF_KEYWORDS = {'pdf', 'plan', 'venue', 'schedule', 'budget', 'conference', 'keynote', 'parking'}
    if any(kw in q_lower for kw in PDF_KEYWORDS):
        return 'pdf_search'

    # CSV data source — guest list, attendees, RSVP, confirmed, VIP
    CSV_KEYWORDS = {'csv', 'guest', 'attending', 'attendee', 'rsvp', 'confirmed', 'vip', 'invited', 'who is'}
    if any(kw in q_lower for kw in CSV_KEYWORDS):
        return 'csv_search'

    # Default: meeting notes
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
