import json
import os
from datetime import datetime, timedelta

def search_email(query: str) -> str:
    """
    Search emails.json for matches in subject, body, date, or sender based on the query.
    Returns the matching email content as a single string.
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'emails.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            emails = json.load(f)
    except FileNotFoundError:
        return "Error: emails.json not found."

    results = []
    query_lower = query.lower()

    # Handle relative dates for fallback
    today_str = datetime.now().strftime('%Y-%m-%d')
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    search_terms = []
    if 'yesterday' in query_lower:
        search_terms.append(yesterday_str)
    if 'today' in query_lower:
        search_terms.append(today_str)
        
    # Extract potential keywords by removing common filler words
    words = [w for w in query_lower.split() if len(w) > 3 and w not in ['show', 'find', 'from', 'email', 'emails', 'mail', 'message', 'yesterday', 'today']]
    search_terms.extend(words)

    for email in emails:
        matched = False
        
        # If there are no specific terms, check if the full query is somehow in there
        if not search_terms:
            if query_lower in email.get('subject', '').lower() or query_lower in email.get('body', '').lower():
                matched = True
        else:
            for term in search_terms:
                if (term in email.get('subject', '').lower() or 
                    term in email.get('body', '').lower() or 
                    term in email.get('date', '').lower() or
                    term in email.get('sender', '').lower()):
                    matched = True
                    break

        if matched:
            results.append(f"Date: {email.get('date')}\nSubject: {email.get('subject')}\nSender: {email.get('sender')}\nBody: {email.get('body')}")

    if not results:
        return f"No email results found for query: '{query}'"
    
    return "\n\n---\n\n".join(results)
