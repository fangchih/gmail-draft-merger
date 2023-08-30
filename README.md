# gmail-draft-merger

A email merger tool by using the gmail draft message as the template.



## Google Cloud Platform

1. Create a GCP project (or reuse an existing one) from [your developer console](https://console.developers.google.com)

2. Enabling `Gmail API` and `Google Sheet API ` [via the web console](https://cloud.google.com/endpoints/docs/openapi/enable-api#console)





## Prerequisites 

1. Define `fields` that merger needs and organize that in the Google Spreadsheet: [merger template](https://docs.google.com/spreadsheets/d/1lU3GChMP5DAh3MjeFuiLbkNc8PwO2OIYRIYcuE6racA/edit#gid=0).
2. Create a draft message as the template in Gmail and put necessary `fields` inside, you can refer the sample here: [gmail draft screenshot](gmail-draft.png).
3. Install Python3 in the OS
4. This sample app requires you to create a `Gmail draft mail` to serve as the letter template with variable placeholders.  Here's a [sample letter template](https://docs.google.com/document/d/1NHszIebuBSvgePFNH9m7BlMu3B2GUS4dQ4njwXwe6vw/edit) for reference.
5. Here is [one example Sheet](https://docs.google.com/spreadsheets/d/1lU3GChMP5DAh3MjeFuiLbkNc8PwO2OIYRIYcuE6racA/edit#gid=0) you can model yours with. Ensure you then set the `SPREADSHEETS_ID` variable to its file ID.

## Install


```shell

git clone https://github.com/fangchih/gmail-draft-merger.git
cd gmail-draft-merger
python -m venv ./venvdir
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
- Execute the main.py: `python main.py`.




## Application code

If you run the sample app as written (with all real variables and data documents) and accept the OAuth2 permissions.
You'll see one line of output per letter merged.
