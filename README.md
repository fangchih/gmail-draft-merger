# gmail-draft-merger

A email merger tool by using the Gmail `draft` message as the template.



## Setup procedures

#### 1. Create a GCP project (or reuse an existing one) from [Google Cloud Console](https://console.cloud.google.com)

#### 2. Enabling API, `Gmail API` and `Google Sheet API`

Ref doc: https://cloud.google.com/endpoints/docs/openapi/enable-api#console

#### 3. Setting up the OAuth consent screen with the necessary API scopes.

Ref doc: https://support.google.com/cloud/answer/6158849

<kbd>
  <img width="600" alt="Screenshot 2023-08-30 at 14 13 57" src="https://github.com/fangchih/gmail-draft-merger/assets/1895216/24ccdd14-8a00-46f4-98d4-5d9c09165fee">
</kbd>

#### 4. Creating a OAuth Client ID with the `Desktop app` type.

Ref doc: https://support.google.com/cloud/answer/6158849

<kbd>
  <img width="600" src="https://github.com/fangchih/gmail-draft-merger/assets/1895216/54476373-5378-4464-b48d-8a8738bbf603">
</kbd>

<p>

<kbd>
  <img width="600" src="https://github.com/fangchih/gmail-draft-merger/assets/1895216/795b371b-d44b-4e1a-a5c8-f82c9f44447e">
</kbd>

#### 5. Download the client secret json file for later use.
<kbd>
  <img width="600" src="https://github.com/fangchih/gmail-draft-merger/assets/1895216/e635723d-b9b7-4e77-bca5-4ded5f19a604">
</kbd>


#### 6. Create a spreadshet as the user list with necessary `variables` that merger needs, ensure you then set the `SPREADSHEETS_ID` variable to its file ID.

Here is [one example Sheet](https://docs.google.com/spreadsheets/d/1lU3GChMP5DAh3MjeFuiLbkNc8PwO2OIYRIYcuE6racA/edit#gid=0) you can model yours with.

<kbd>
  <img width="600" src="https://github.com/fangchih/gmail-draft-merger/assets/1895216/410aa707-b122-4265-832c-69eb51ef9e51">
</kbd>


#### 7. Create a draft message in your Gmail account as the template and put necessary `variables` inside

<kbd>
  <img width="600" src="./gmail-draft.png">
</kbd>


#### 8. Install Python3 in your OS


## Installation


#### 1. Download the source and necessary python packages

```shell
git clone https://github.com/fangchih/gmail-draft-merger.git
cd gmail-draft-merger
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

#### 2. Update the `.env` file, replace the value to yours

```
SPREADSHEETS_ID=YOUR_SPREADSHEET_ID
SHEET_NAME=YOUR_SHEET_NAME
GMAIL_DRAFT_SUBJECT=YOUR_GMAIL_DRAFT_SUBJECT
CLIENT_SECRET_FILE=YOUR_CLENT_SECRET_FILE
``` 
#### 3. Execute the main.py, merged mails will be sent, your can do few tests first.

```shell
python src/main.py
```


## Cleanup and exit the python virtual env

```shell
deactivate
```

