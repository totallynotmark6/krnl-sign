import requests
from krnl_sign.util import ttl_cache

@ttl_cache(30)
def fetch_status():
    r = requests.get("https://public.radio.co/stations/s209f09ff1/status")
    return r.json()

def get_live_data():
    status = fetch_status()
    return status["source"] # name is under collaborator!

def get_current_track():
    status = fetch_status()
    return status["current_track"]

def is_live():
    live_data = get_live_data()
    if live_data["collaborator"] is None:
        return False
    return True