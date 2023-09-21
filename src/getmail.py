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
from google.oauth2 import service_account


from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email

load_dotenv()

TOKEN_STORE_FILE = 'token.json'

SA_KEY = os.getenv('SA_KEY')




# def _gen_token():
#     creds = None
#     if os.path.exists(TOKEN_STORE_FILE):
#         creds = Credentials.from_authorized_user_file(TOKEN_STORE_FILE, SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
#             creds = flow.run_local_server(port=0)



def _get_credential():
    """Uses project credentials in CLIENT_SECRET_FILE along with requested OAuth2
        scopes for authorization, and caches API tokens in TOKEN_STORE_FILE.
    """
    creds = service_account.Credentials.from_service_account_file(SA_KEY, scopes=['https://www.googleapis.com/auth/gmail.readonly'])
    
    return creds.with_subject("justin@andersenplay.com")


  
def getEmails():

    # _gen_token()
  
    # Connect to the Gmail API
    service = discovery.build('gmail', 'v1', credentials=_get_credential())
  
    # request a list of all the messages
    result = service.users().messages().list(userId='me').execute()
  
    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')
  
    # messages is a list of dictionaries where each dictionary contains a message id.
  
    # iterate through all the messages
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
  
        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']
  
            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
  
            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)
  
            print("Message: ", decoded_data)
            print('\n')

            break
        except:
            pass
  
  
getEmails()