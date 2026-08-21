import requests
import os

TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")

def get_live_flight_price(origin, destination, date):
    url = "https://api.tequila.kiwi.com/v2/search"
    headers = {"apikey": TEQUILA_API_KEY}

    params = {
        "fly_from": origin,
        "fly_to": destination,
        "date_from": date,
        "date_to": date,
        "curr": "USD",
        "limit": 1
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
    except (requests.RequestException, ValueError):
        return None

    if data.get("data"):
        return data["data"][0]["price"]

    return None
