import datetime
import os.path
from dateutil.relativedelta import relativedelta
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]      

def get_films_agenda():

  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("credentials/token.json"):
    creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("credentials/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    
    date = datetime.strptime(str(now), '%Y-%m-%dT%H:%M:%S.%fZ')
    one_month_before = date - relativedelta(months=1)
    one_month_after = date + relativedelta(months=1)
    one_month_before = one_month_before.isoformat() + 'Z'
    one_month_after = one_month_after.isoformat() + 'Z'

    # On récupère l'ensemble des events dans le dernier mois
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=one_month_before,
            timeMax=one_month_after,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    films = []
    for event in events:
        if "UGC" in event["location"]:
            films.append(event["summary"].replace(' ','_').replace("'",'_').replace(":",'').replace("-",'_').lower())
    return films
  except HttpError as error:
    print(f"An error occurred: {error}")