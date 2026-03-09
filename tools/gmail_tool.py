import base64
from email.message import Message
import googleapiclient.errors
from integrations.gmail_auth import get_gmail_service

def search_gmail(query: str) -> str:
    """
    Searches the user's Gmail inbox using the Gmail API.
    Returns the top 5 relevant emails formatted as a string.
    """
    try:
        service = get_gmail_service()
    except FileNotFoundError as e:
        return f"Authentication Error: {str(e)}\nPlease place the 'credentials.json' file in the 'config/' directory to enable real-time Gmail search."
    except Exception as e:
        return f"Authentication Error: Could not connect to Gmail API. {str(e)}"

    if not service:
        return "Error: Could not establish Gmail service."

    try:
        # Call the Gmail API to search for messages
        results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            return f"No relevant emails were found in your inbox for query: '{query}'"

        email_summaries = []
        for msg in messages:
            # Fetch the full message details
            msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            
            headers = msg_detail.get('payload', {}).get('headers', [])
            subject = "No Subject"
            sender = "Unknown Sender"
            date = "Unknown Date"
            
            for header in headers:
                name = header.get('name', '').lower()
                if name == 'subject':
                    subject = header.get('value')
                elif name == 'from':
                    sender = header.get('value')
                elif name == 'date':
                    date = header.get('value')
            
            snippet = msg_detail.get('snippet', '')
            
            email_summaries.append({
                "sender": sender,
                "subject": subject,
                "date": date,
                "snippet": snippet
            })

        # Format output for the agent
        formatted_results = f"🔍 **Gmail Search Results for '{query}'**:\n\n"
        for i, email in enumerate(email_summaries, 1):
            formatted_results += (
                f"**Email {i}**\n"
                f"• **From:** {email['sender']}\n"
                f"• **Date:** {email['date']}\n"
                f"• **Subject:** {email['subject']}\n"
                f"• **Snippet:** {email['snippet']}\n"
                f"{'-'*40}\n"
            )
        
        return formatted_results

    except googleapiclient.errors.HttpError as error:
        return f"Gmail API Error: {error}"
    except Exception as e:
        return f"Unexpected error while searching Gmail: {str(e)}"
