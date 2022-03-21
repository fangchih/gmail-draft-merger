# -*- coding: utf-8 -*-
from __future__ import print_function

import time, os, base64, email, datetime
from dotenv import load_dotenv
from email import policy

from apiclient import errors

from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# authorization constants
# HOME_PATH = str(Path.home())

load_dotenv()

# Read ENV VARs
SPREADSHEETS_ID = os.getenv('SPREADSHEETS_ID')
GMAIL_DRAFT_SUBJECT = os.getenv('GMAIL_DRAFT_SUBJECT')
CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')
SHEET_NAME = "Sheet1"

# Define Columns
RECIPIENT_COL  = "Recipient"
EMAIL_SENT_COL = "Sent Time"
EMAIL_SENT_COL_IDX = "H"

# application constants
COLUMNS = []

TOKEN_STORE_FILE = 'token.json'

SCOPES = (  # iterable or space-delimited string
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
)


def _get_http_client():
    """Uses project credentials in CLIENT_SECRET_FILE along with requested OAuth2
        scopes for authorization, and caches API tokens in TOKEN_STORE_FILE.
    """
    store = file.Storage(TOKEN_STORE_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    return creds.authorize(Http())


def _get_sheets_data(service, sheet_name):
    """(private) Returns data from Google Sheets source. It gets all rows of
        'Sheet1' (the default Sheet in a new spreadsheet), but drops the first
        (header) row. Use any desired data range (in standard A1 notation).
    """
    ssvalues = service.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=sheet_name).execute().get('values')
    global COLUMNS
    COLUMNS = ssvalues[0]
    return ssvalues[1:] # skip header row


def _set_sheets_cell(service, range_name, values):
    body = {'values': values}
    result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEETS_ID, range=range_name, valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))  
    return result  


def _gen_token():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_STORE_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_STORE_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        # with open(TOKEN_STORE_FILE, 'w') as token:
        #     token.write(creds.to_json())



def _get_gmail_template_from_draft(service, subject_line):
    # Get a Gmail draft message by matching the subject line.
    # @param {string} subject_line to search for draft message
    # @return {raw message string} containing the subject, plain and html message body and attachments

    try:
        results = service.users().drafts().list(userId='me', q=subject_line).execute()
        drafts = results.get('drafts', [])

        if not drafts:
            raise Exception("Oops - can't find Gmail draft by subject: " + subject_line)

        if len(drafts)>1:
            raise Exception("Oops - got multiple Gmail drafts by subject: " + subject_line)

        draft = drafts[0]
        gmail_msg = service.users().messages().get(userId='me', format='raw', id=draft['message']['id']).execute()
        raw_message = str(base64.urlsafe_b64decode(gmail_msg['raw']), 'utf-8')
        return raw_message

    except Exception as e:
        raise Exception(e);


def _gmail_send(service, email_message):
    new_msg = {'raw': str(base64.urlsafe_b64encode(email_message.as_bytes()), 'utf-8')}
    gmail_msg = (gmail.users().messages().send(userId='me', body=new_msg).execute())
    print ('\t Message Id: %s' % gmail_msg['id'])
    return gmail_msg
  


if __name__ == '__main__':

    # used to record sent emails
    out = []
    merge = {}

    _gen_token()

    apiHttpclient = _get_http_client()
    sheets = discovery.build('sheets', 'v4', http=apiHttpclient)
    gmail = discovery.build('gmail', 'v1', http=apiHttpclient)

    raw_message = _get_gmail_template_from_draft(gmail, GMAIL_DRAFT_SUBJECT)
    data = _get_sheets_data(sheets, SHEET_NAME) # get data from data source

    for i, row in enumerate(data):
        merge = {}
        merge.update(dict(zip(COLUMNS, row)))
        print(i, merge)
        if EMAIL_SENT_COL in merge and merge[EMAIL_SENT_COL]:
            print('\t Passed...')
            continue
        
        context = merge.iteritems() if hasattr({}, 'iteritems') else merge.items()
        draft_msg = email.message_from_string(raw_message, policy=policy.default)

        for part in draft_msg.walk():
            if (part.get_content_type() == 'text/plain'):
                c = part.get_content()
                for key, value in context:
                    c = c.replace('{{' + key + '}}', value)
                part.set_content(c)
            if (part.get_content_type() == 'text/html'):
                c = part.get_content()
                for key, value in context:
                    c = c.replace('{{' + key + '}}', value)
                part.set_content(c, subtype='html')


        draft_msg['To'] = merge[RECIPIENT_COL]
        gmail_msg = _gmail_send(gmail, draft_msg)
        _set_sheets_cell(sheets, SHEET_NAME + "!" + EMAIL_SENT_COL_IDX + str(i+2), [[str(datetime.datetime.now())]])


    
