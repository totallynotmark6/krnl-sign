from functools import cache
import requests
import arrow

@cache
def fetch_calendar():
    r = requests.get("https://github.com/totallynotmark6/cornell-college-block-schedule/raw/main/calendar.json")
    data =  r.json() # type: dict[str, dict]
    for key in data.keys():
        for block in data[key]['blocks']:
            block['start'] = arrow.get(block['start'])
            block['end'] = arrow.get(block['end'])
        for event in data[key]['events']:
            event['start'] = arrow.get(event['start'])
            event['end'] = arrow.get(event['end'])
    return data

def calendar_data(for_date: arrow.Arrow):
    calendar = fetch_calendar()
    school_year = None
    for key in calendar.keys():
        year_data = calendar[key]
        if year_data['blocks'][0]['start'] <= for_date <= year_data['blocks'][-1]['end']:
            school_year = key
            break
    if school_year is None:
        raise ValueError("Calendar data not found for date!")
    year_data = calendar[school_year]
    block = None
    for block_data in year_data['blocks']:
        if block_data['start'] <= for_date <= block_data['end']:
            block = block_data
            break
    event = None
    for event_data in year_data['events']:
        if event_data['start'] <= for_date <= event_data['end']:
            event = event_data
            break
    
    if block is None and event is not None:
        return {
            "block": None,
            "day": None,
            "week": None,
            "event": event,
            "school_year": school_year
        }
    elif block is None and event is None:
        # so if we're not in a block, and we're not in an offically defined break, we're in block break!
        # block break starts on the last day of the last block we were in, and ends on the first day of the next block
        # to get the last block we were in, we need to find the most recent block that ended before the date we're checking
        last_block = None
        for block_data in year_data['blocks']:
            if block_data['end'] < for_date:
                last_block = block_data

def is_summer():
    return False