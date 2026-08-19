SAFETY_FLAGS = {
    "vietnam": {
        "risk_level": "low",
        "notes": [
            "Petty theft can occur in crowded tourist areas.",
            "Motorbike traffic is dense — use caution when crossing streets.",
            "Avoid unlicensed taxis; use Grab for safer transport."
        ]
    },
    "cambodia": {
        "risk_level": "medium",
        "notes": [
            "Pickpocketing is common in Phnom Penh and Siem Reap.",
            "Avoid walking alone late at night in poorly lit areas.",
            "Be cautious of bag‑snatching from passing motorbikes."
        ]
    },
    "thailand": {
        "risk_level": "low",
        "notes": [
            "Tourist scams are common around tuk‑tuks and gem shops.",
            "Pickpocketing can occur in nightlife districts.",
            "Use metered taxis or Grab to avoid fare scams."
        ]
    },
    "south_africa": {
        "risk_level": "high",
        "notes": [
            "High rates of violent crime in certain urban areas.",
            "Avoid walking alone, especially after dark.",
            "Use registered taxis or rideshare apps only."
        ]
    },
    "brazil": {
        "risk_level": "high",
        "notes": [
            "Armed robbery and pickpocketing are common in major cities.",
            "Avoid displaying valuables in public.",
            "Stick to well‑lit, populated areas and avoid favelas unless with a guide."
        ]
    }
}

def get_safety_flags(country: str):
    key = country.lower().replace(" ", "_")
    return SAFETY_FLAGS.get(key, {
        "risk_level": "unknown",
        "notes": ["No safety data available for this region."]
    })
