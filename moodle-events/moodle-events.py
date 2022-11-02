# Get the calendar information from moodle
# This is a python script that will get the calendar information from moodle and put it into a csv file
import os
import requests
import config
from ics import Calendar
import datetime
from datetime import date
import pickle


# TODO: Check for other control characters
def get_calendar_info():
    r = requests.get(config.calendar_url)
    formatted = r.text.replace("\u0308", "**")
    return formatted


def save_calendar_info(calendar):
    with open('calendar.ics', 'w') as file:
        file.writelines(calendar.serialize_iter())


def check_for_upcoming_events():
    events = pickle.load(open('events.data', 'rb'))
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=config.delta)
    with open('calendar.ics', 'r') as file:
        c = Calendar(file.read())
        for event in c.events:
            if (date.fromisoformat(str(event.begin.date())) - now.date() < delta) and event.name not in events:
                data = {"embeds": [{"title": event.name,
                                    "description": f"{event.description}\n**Fällig bis zum {date.fromisoformat(str(event.begin.date())).strftime('%d.%m.%Y')} **",
                                    }
                                   ]}
                r = requests.post(config.webhook, json=data)
                events.append(event.name)
                pickle.dump(events, open('events.data', 'wb'))
                print(event.name)
                print(event.begin)


def at_start():
    events = []
    if not os.path.exists('events.data'):
        pickle.dump(events, open('events.data', 'wb'))


if __name__ == '__main__':
    at_start()
    calendar = Calendar(get_calendar_info())
    save_calendar_info(calendar)
    check_for_upcoming_events()
