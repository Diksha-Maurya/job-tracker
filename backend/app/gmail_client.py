import os
import pickle
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service():
    creds = None
    token_path = 'token.json'
    creds_path = 'credentials.json'

    # Load saved credentials if available
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no (valid) credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def list_recent_emails(user_id='me', max_results=5):
    service = get_gmail_service()
    results = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId=user_id, id=msg['id']).execute()
        snippet = msg_data.get('snippet')
        internal_date = msg_data.get('internalDate')
        date = datetime.fromtimestamp(int(internal_date) / 1000)
        emails.append({
            'id': msg['id'],
            'snippet': snippet,
            'date': date.isoformat()
        })

    return emails
