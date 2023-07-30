from functools import cache
import requests
import arrow

@cache
def fetch_calendar():
    r = requests.get("https://github.com/totallynotmark6/cornell-college-block-schedule/raw/main/calendar.json")
    return r.json()

def calendar_data(for_date: arrow.Arrow):
    calendar = fetch_calendar()
    
