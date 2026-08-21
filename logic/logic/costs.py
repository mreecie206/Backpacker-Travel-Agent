COST_TABLES = {
    "vietnam": {
        "hostel_per_night": 8,
        "hotel_per_night": 18,
        "food_per_day": 10,
        "local_transport_per_day": 4,
        "bus_city_to_city": 12,
        "train_city_to_city": 18,
        "avg_flight_domestic": 45,
        "avg_flight_international": 120
    },

    "cambodia": {
        "hostel_per_night": 7,
        "hotel_per_night": 15,
        "food_per_day": 9,
        "local_transport_per_day": 4,
        "bus_city_to_city": 10,
        "train_city_to_city": None,
        "avg_flight_domestic": 55,
        "avg_flight_international": 140
    },

    "thailand": {
        "hostel_per_night": 10,
        "hotel_per_night": 22,
        "food_per_day": 12,
        "local_transport_per_day": 5,
        "bus_city_to_city": 14,
        "train_city_to_city": 20,
        "avg_flight_domestic": 40,
        "avg_flight_international": 130
    },

    "south_africa": {
        "hostel_per_night": 14,
        "hotel_per_night": 28,
        "food_per_day": 15,
        "local_transport_per_day": 6,
        "bus_city_to_city": 20,
        "train_city_to_city": None,
        "avg_flight_domestic": 60,
        "avg_flight_international": 250
    },

    "cape_verde": {
        "hostel_per_night": 18,
        "hotel_per_night": 35,
        "food_per_day": 16,
        "local_transport_per_day": 7,
        "bus_city_to_city": None,
        "train_city_to_city": None,
        "avg_flight_domestic": None,
        "avg_flight_international": 300
    },

    "brazil": {
        "hostel_per_night": 12,
        "hotel_per_night": 25,
        "food_per_day": 13,
        "local_transport_per_day": 6,
        "bus_city_to_city": 18,
        "train_city_to_city": None,
        "avg_flight_domestic": 55,
        "avg_flight_international": 220
    },

    "colombia": {
        "hostel_per_night": 10,
        "hotel_per_night": 22,
        "food_per_day": 11,
        "local_transport_per_day": 5,
        "bus_city_to_city": 15,
        "train_city_to_city": None,
        "avg_flight_domestic": 45,
        "avg_flight_international": 180
    },

    "portugal": {
        "hostel_per_night": 22,
        "hotel_per_night": 45,
        "food_per_day": 20,
        "local_transport_per_day": 8,
        "bus_city_to_city": 25,
        "train_city_to_city": 30,
        "avg_flight_domestic": 70,
        "avg_flight_international": 180
    }
}

def get_costs(country: str):
    if not isinstance(country, str):
        return None
    key = "_".join(country.strip().lower().split())
    return COST_TABLES.get(key, None)
