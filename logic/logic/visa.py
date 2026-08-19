import requests
import os

SHERPA_API_KEY = os.getenv("SHERPA_API_KEY")

def get_visa_requirements(origin_country, destination_country):
    """
    Scrapes visa requirements from Sherpa API.
    Returns structured visa info or None.
    """

    url = "https://api.joinsherpa.com/v2/requirements"

    headers = {
        "X-API-KEY": SHERPA_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "from": origin_country,
        "to": destination_country
    }

    try:
        r = requests.post(url, json=payload, headers=headers)
        data = r.json()

        # Sherpa returns a list of requirements
        if "requirements" not in data:
            return None

        reqs = data["requirements"]
        if not reqs:
            return None

        # Extract the most relevant visa requirement
        visa_items = [item for item in reqs if item.get("category") == "visa"]

        if not visa_items:
            return None

        visa = visa_items[0]

        return {
            "visa_required": visa.get("required", False),
            "description": visa.get("description", "No description available."),
            "documents": visa.get("documents", []),
            "duration": visa.get("duration", None)
        }

    except Exception:
        return None
