import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from core.CalendarFetcher import CalendarFetcher
from core.Event import Event

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


class GCalendarFetcher(CalendarFetcher):

    def __init__(self, credentials_path, token_path):

        store = file.Storage(token_path)
        self.creds = store.get()

        if not self.creds or self.creds.invalid:
            flow = client.flow_from_clientsecrets(credentials_path, SCOPES)
            self.creds = tools.run_flow(flow, store)

    def fetch(self, max_events):
        service = build('calendar', 'v3', http=self.creds.authorize(Http()))

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=max_events, singleEvents=True,
            orderBy='startTime').execute()

        items= events_result.get('items', [])

        import pdb; pdb.set_trace()

        events = [{"summary": e["summary"], "start": e["start"], "end": e["end"]} for e in items]

        return {"events": events}
