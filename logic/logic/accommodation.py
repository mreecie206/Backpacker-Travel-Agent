ACCOMMODATION_DB = {
    "vietnam": [
        {
            "name": "The Like Hostel",
            "city": "Ho Chi Minh City",
            "type": "hostel",
            "price_per_night": 8,
            "amenities": ["WiFi", "Air Conditioning", "Free Breakfast"],
            "safety_notes": ["Located in District 1, safe for tourists."]
        },
        {
            "name": "Hanoi Buffalo Hostel",
            "city": "Hanoi",
            "type": "hostel",
            "price_per_night": 10,
            "amenities": ["Pool", "Bar", "Tours"],
            "safety_notes": ["Old Quarter is busy but safe."]
        }
    ],
    "cambodia": [
        {
            "name": "Onederz Hostel",
            "city": "Siem Reap",
            "type": "hostel",
            "price_per_night": 7,
            "amenities": ["Pool", "Rooftop", "Tours"],
            "safety_notes": ["Tourist-friendly area near Pub Street."]
        }
    ],
    "thailand": [
        {
            "name": "Lub D Hostel",
            "city": "Bangkok",
            "type": "hostel",
            "price_per_night": 12,
            "amenities": ["Coworking", "Bar", "Events"],
            "safety_notes": ["Safe area near Siam Square."]
        }
    ]
}

def get_accommodations(destination: str):
    key = destination.lower().replace(" ", "_")
    return ACCOMMODATION_DB.get(key, [])
