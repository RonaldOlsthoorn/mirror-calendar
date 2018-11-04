import os, json
from gcal import GCalendarFetcher
from core.CalendarFetcher import CalendarFetcher
from flask import jsonify


class CompositeCalendarFetcher(CalendarFetcher):

    def __init__(self, calendars):
        self.calendars = calendars

    def fetch(self, max_events=50):
        events = self._fetch_events(max_events)
        return jsonify({"events": _sort_by_date(events)})

    def _fetch_events(self, max_events):
        events = []

        for calendar in self.calendars:
            events.append(calendar.fetch(max_events))

        return events


def _sort_by_date(event_lists):

    events = []

    for eventlist in event_lists:
        events.extend(eventlist["events"])

    return events


def from_json(path):

    with open(path, 'r') as f:
        config = json.load(f)

    calendars = []

    for cal_config in config["calendars"]:
        if cal_config["type"] == "gcal":
            credentials_path = os.path.normpath(
                os.path.join(os.path.dirname(path),
                             cal_config["credentials_path"]))

            token_path = os.path.normpath(
                os.path.join(os.path.dirname(path),
                             cal_config["token_path"]))

            calendars.append(GCalendarFetcher.GCalendarFetcher(credentials_path, token_path))
        else:
            raise "unknown calendar type: {}".format(cal_config["type"])

    return CompositeCalendarFetcher(calendars)
