"""
tools/gmail_search.py
Real Gmail integration using Google API.
Falls back to simulated data if credentials not available.
"""

import os
import base64
from email import message_from_bytes

# Fallback to simulated if no credentials
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDS_FILE = "credentials.json"
TOKEN_FILE  = "token.json"


def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def search_real_gmail(query: str) -> list:
    """
    Search real Gmail inbox for messages matching query.
    Falls back to simulated email search if Gmail not configured.
    """
    if not GMAIL_AVAILABLE or not os.path.exists(CREDS_FILE):
        # Fallback to simulated data
        from tools.email_search import search_email
        return search_email(query)

    try:
        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me', q=query, maxResults=5
        ).execute()

        messages = []
        for msg in results.get('messages', []):
            detail = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()

            headers = detail['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender  = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date    = next((h['value'] for h in headers if h['name'] == 'Date'), '')

            # Extract body
            body = ""
            if 'parts' in detail['payload']:
                for part in detail['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
            else:
                data = detail['payload']['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')

            messages.append({
                "id": msg['id'],
                "subject": subject,
                "sender": sender,
                "date": date,
                "body": body[:500]
            })

        return messages

    except Exception as e:
        # Fallback to simulated
        from tools.email_search import search_email
        return search_email(query)