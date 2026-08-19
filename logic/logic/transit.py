import requests
import os

TWELVEGO_API_KEY = os.getenv("TWELVEGO_API_KEY")

def get_bus_train_price(origin_city, destination_city, date):
    """
    Scrapes bus/train prices from 12Go Asia API.
    Returns the cheapest available option.
    """

    url = "https://api.12go.com/v2/booking/search"

    headers = {
        "X-API-KEY": TWELVEGO_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "from": origin_city,
        "to": destination_city,
        "date": date,
        "currency": "USD",
        "limit": 10
    }

    try:
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()

        if "routes" not in data:
            return None

        routes = data["routes"]

        if not routes:
            return None

        # Return the cheapest route
        cheapest = min(routes, key=lambda x: x["price"])
        return {
            "operator": cheapest["operator"],
            "price": cheapest["price"],
            "vehicle": cheapest["vehicle"],
            "duration": cheapest["duration"]
        }

    except Exception:
        return None
