from tools.email_search import search_email
from tools.notes_search import search_notes
from tools.csv_search import search_csv
from tools.pdf_search import search_pdf
from tools.chat_search import search_chat_logs
from tools.task_search import search_tasks
from tools.gmail_tool import search_gmail

def get_tools():
    """
    Returns a list of callable functions that Gemini can use as tools.
    The docstrings inside each function will be used by Gemini
    to understand what they do.
    """
    return [
        search_email,
        search_notes,
        search_csv,
        search_pdf,
        search_chat_logs,
        search_tasks,
        search_gmail,
    ]
