#!/usr/bin/env python3
# Script to import a timetable from the app ClassTime into a google calendar.
# Calendar ID is found in the calendar's settings, DB file can be exported through the share button in the app.
# Only works with A/B timetables, which are exported separately.

import json, datetime, pickle, os.path, sys, argparse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

parser = argparse.ArgumentParser()
parser.add_argument("timetable", help="filename of .timetable db.")
parser.add_argument("-tz", "--timezone", help="Timezone in TZ database format. Defaults to Europe/London.")
parser.add_argument("-c", "--calendar", help="ID of the calendar you are adding to. Found under the settings on calendar.google.com.")
try:
    args = parser.parse_args()
    calendar_id = args.calendar
    dbfile = args.timetable
    if not args.timezone:
        timeZone = "Europe/London"
    else:
        timeZone = args.timezone
except FileNotFoundError:
    print("No filename supplied.")
    sys.exit()

print("This script only works for A/B week timetables, each being loaded seperately.")
choice = input("Is this timetable made for this week? [y/n]: ").lower()
if choice == "y":
    today = datetime.datetime.today()
elif choice == "n":
    today = datetime.datetime.today() + datetime.timedelta(days=7)
else:
    sys.exit()

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class Lesson:
    def __init__(self, name, startDelta, endDelta, teacher, room, day):
        self.summary = name
        if teacher != "":
            self.description = "Teacher: {}".format(teacher)
        self.location = "Room: {}".format(room)
        currentDay = days.index(today.strftime("%A"))
        lessonDay = days.index(day)
        dayDelta = lessonDay - currentDay
        applyDate = (today + datetime.timedelta(days=dayDelta)).day
        # the .timetable file stores lesson start & end times as minutes from 00:00, so they are converted here
        self.start = {
            "dateTime": datetime.datetime(today.year, today.month, applyDate, int(startDelta/60), int(startDelta%60)).isoformat(),
            "timeZone": timeZone
        }
        self.end = {
            "dateTime": datetime.datetime(today.year, today.month, applyDate, int(endDelta/60), int(endDelta%60)).isoformat(),
            "timeZone": timeZone
        }
        # Change this if you have the same timetable each week
        self.recurrence = ["RRULE:FREQ=WEEKLY;INTERVAL=2"]



lessons = []
try:
    with open(dbfile, "r") as raw:
        db = json.load(raw)
    for d in range(1,6):
        try:
            for l in range(1,6):
                name = db["LESSON_{}_{}".format(d,l)]
                startDelta = db["LESSON_START_TIME_{}_{}".format(d,l)]
                endDelta = db["LESSON_END_TIME_{}_{}".format(d,l)]
                teacher = db["TEACHER_{}_{}".format(d,l)]
                room = db["ROOM_{}_{}".format(d,l)]
                day = days[d-1]
                if name != "":
                    lessons.append(Lesson(name, startDelta, endDelta, teacher, room, day))
        except:
            pass
except FileNotFoundError:
    print("File not found.")
    sys.exit()

print("Lessons imported. Do these look right?")
for l in lessons:
    try:
        d = l.description+", "
    except:
        d = ""
    print("{}: {}, {}{}".format(l.start["dateTime"], l.summary, d, l.location))
if input(":) ? [y/n]: ").lower() != "y":
    sys.exit()

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# borrowed from https://github.com/gsuitedevs/python-samples/blob/master/drive/quickstart/quickstart.py
# Removed unnecessary libraries, comments, and changed scope.
SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

for l in lessons:
    event = json.loads(json.dumps(l.__dict__))
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
print("Events Added. Refresh your calendar to see classes.")
