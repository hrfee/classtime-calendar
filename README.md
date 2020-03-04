# classtime-calendar

Script to import a timetable from [ClassTime](https://play.google.com/store/apps/details?id=eu.nohus.classtime) into Google Calendar.
## Usage

```
typeprint.py [-tz|--timezone] <timezone> [-c|--calendar] <calendar id> <timetable>
```
* `--timezone`: Timezone in TZ database. Defaults to `Europe/London`.
* `--calendar`: ID of calendar to apply to. To find: [calendar settings](https://calendar.google.com/calendar/r/settings) > click your calendar under "Settings for my calendar", "Calendar ID" under Integration at bottom of page.
* `<timetable>`: .timetable file can be exported through the share menu in the ClassTime app.

On the first run, a browser window will open where you can login. Credentials are saved to `token.pickle`/`credentials.json`.
## Known problems
* Currently only works with A/B week timetables. Each should be imported separately, at which time the script will ask whether it is for the current week. If you have a single timetable, either import twice as different weeks or change `self.recurrence`'s interval.
* The delete from calendar script was too rough to include, so there's no way to quickly remove classes from the calendar.

## Licenses
Check LICENSE.txt. Code taken from quickstart.py in import.py includes Copyright notice
