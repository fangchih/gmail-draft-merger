# gmail-draft-merger

A email merger tool by using the gmail draft message as the template.



## Google Cloud Platform

1. Create a GCP project (or reuse an existing one) from [your developer console](https://console.developers.google.com)
2. Enabling `Gmail API` and `Google Sheet API` [via the web console](https://cloud.google.com/endpoints/docs/openapi/enable-api#console)

3. 
4. Setting up the OAuth consent screen, add necessary API scopes. [doc](https://support.google.com/cloud/answer/6158849)

<kbd>
<img width="550" alt="Screenshot 2023-08-30 at 14 13 57" src="https://github.com/fangchih/gmail-draft-merger/assets/1895216/f810beb1-ce7d-4666-a187-8afc234cdc98">
</kbd>

5. We also need to create a OAuth Client ID with `Desktop app` type. [doc](https://support.google.com/cloud/answer/6158849)
<kbd>
<img width="600" src="https://github.com/fangchih/gmail-draft-merger/assets/1895216/795b371b-d44b-4e1a-a5c8-f82c9f44447e">
</kbd>


4. 
5. 


## Prerequisites 

1. Define `fields` that merger needs and organize that in the Google Spreadsheet. Here is [one example Sheet](https://docs.google.com/spreadsheets/d/1lU3GChMP5DAh3MjeFuiLbkNc8PwO2OIYRIYcuE6racA/edit#gid=0) you can model yours with. Ensure you then set the `SPREADSHEETS_ID` variable to its file ID.
2. Create a draft message as the template in Gmail and put necessary `fields` inside, you can refer the sample here: [gmail draft screenshot](gmail-draft.png).
3. Install Python3 in the OS
4. This app requires you to create a `draft` in your Gmail account to serve as the mail template.  Here's a [sample mail template](https://docs.google.com/document/d/1NHszIebuBSvgePFNH9m7BlMu3B2GUS4dQ4njwXwe6vw/edit) for reference.


## Install

```shell

git clone https://github.com/fangchih/gmail-draft-merger.git
cd gmail-draft-merger
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Run
- create the `.env` file, sample as below
```
SPREADSHEETS_ID=1lU3GChMP5DAh3MjeFuiLbkNc8PwO2OIYRIYcuE6racA
SHEET_NAME=sheet1
GMAIL_DRAFT_SUBJECT=2022 Merger template via gmail draft

CLIENT_SECRET_FILE=${HOME}/devkey/merger_client_secret.json
``` 
- Put environment variable values into the `.env` file.
- Execute the main.py:


```shell
python src/main.py
```


## Cleanup

```shell
deactivate
```

