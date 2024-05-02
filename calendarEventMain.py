from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

### Get Creds  ###
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

credFile = "credentials.json"
creds = None
emailCalendar = "mike.lian.teach@gmail.com"
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            credFile, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

### Generate date format ### Need to find more effective way
def genDateFormat(year, month, day):
    end_date = f'{year}{month:02d}{day:02d}T235959Z'
    return end_date

### Adding Event ###
def addEvent(eventName, eventDate, endReDate, startTime, endTime, colorId):
  event = {
    'summary': eventName,
    'description': '',
    'start': {
      'dateTime': f'{eventDate}T{startTime}',
      'timeZone': 'Asia/Kuching',
    },
    'end': {
      'dateTime': f'{eventDate}T{endTime}',
      'timeZone': 'Asia/Kuching',
    },
    'recurrence': [
      f'RRULE:FREQ=WEEKLY;UNTIL={endReDate}'
    ],
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'popup', 'minutes': 30},
        {'method': 'popup', 'minutes': 10},
        {'method': 'popup', 'minutes': 5},
      ],
    },
    'colorId': f'{colorId}',
  }
  try:
    service = build('calendar', 'v3', credentials=creds)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created:', event.get('htmlLink'))
  except HttpError as error:
      print('An error occurred: %s' % error)



moikeClass = [
    #Monday
    ["Y10_DT","2024-5-6","08:00:00", "09:00:00", "3"],
    ["Y7_DL","2024-5-6","09:00:00", "10:00:00", "11"], 
    ["Y9_DL","2024-5-6","11:30:00", "12:30:00", "7"], 
    ["Meeting","2024-5-6","15:00:00", "16:00:00", "5"], 
    #Tues
    ["NC","2024-5-7", "08:00:00", "09:00:00"],
    ["Y7_DL","2024-5-7","09:00:00", "10:00:00", "11"], 
    ["Y8_STEAM","2024-5-7","10:30:00", "11:30:00", "10"], 
    ["Y10_CS","2024-5-7","11:30:00", "13:00:00", "9"], 
    ["Y8_DL","2024-5-7","14:00:00", "15:00:00", "2"],
    #Wed
    ["Y8_DL","2024-5-8","09:00:00", "10:00:00", "2"],
    ["Y7_STEAM","2024-5-8","10:30:00", "11:30:00", "6"],
    ["Canteen Duty","2024-5-8","13:00:00", "13:20:00", "5"],
    ["Y10_CS","2024-5-8","13:30:00", "15:00:00", "9"],
    ["Maker's Club","2024-5-8","15:00:00", "16:00:00", "4"],
    #Thu
    ["Y10_DT","2024-5-9","09:00:00", "10:00:00", "3"],
    ["Y9_STEAM","2024-5-9","10:30:00", "11:30:00", "1"],
    ["Y8_STEAM","2024-5-9","12:30:00", "14:00:00", "10"],
    ["Y9_DL","2024-5-9","14:00:00", "15:00:00", "7"],
    ["Drone Club","2024-5-9","15:00:00", "16:00:00", "4"],
    #Fri
    ["Y10_DT","2024-5-10","10:30:00", "11:30:00", "3"],
    ["Y9_STEAM","2024-5-10","11:30:00", "12:30:00", "1"],
    ["Assembly","2024-5-10","12:30:00", "13:00:00", "5"],
    ["PSHE","2024-5-10","13:30:00", "14:10:00", "5"],
    ["Y7_STEAM","2024-5-10","14:10:00", "15:00:00", "6"],
]

endDate = genDateFormat(2024, 7, 19)
for subject in moikeClass:  # 0-Name, 1-StartDate, 2-StartTime, 3-EndTime, 4-ColourCode
    colourId = "1"
    if subject[0] != "NC":

        match subject[0]:
            case "Y7_DL":
                print("Tomato ", subject[0])
                colourId = "11"
            case "Y7_STEAM":
                print("Tangerine ", subject[0])
                colourId = "6"
            case "Y8_DL":
                print("Sage ", subject[0])
                colourId = "2"
            case "Y8_STEAM":
                print("Basil ", subject[0])
                colourId = "10"
            case "Y9_DL":
                print("Peacoke", subject[0])
                colourId = "7"
            case "Y9_STEAM":
                print("Lavender", subject[0])
                colourId = "1"
            case "Y10_DT":
                print("Grape", subject[0])
                colourId = "3"
            case "Y10_CS":
                print("Blueberry", subject[0])
                colourId = "9"
            case "Y11_ICT":
                print("Graphite", subject[0])
                colourId = "8"
            case _:
                print("Banana", subject[0])
                colourId = "5"
        print(colourId)
        
        addEvent(subject[0], subject[1], endDate, subject[2], subject[3], subject[4])

        
