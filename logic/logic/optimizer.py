from itertools import permutations
from logic.routing import build_route
from logic.costs import get_costs
from logic.transit import get_bus_train_price
from logic.flights import get_live_flight_price

def compute_total_cost(cities, countries, origin, destination):
    """
    Computes total cost for a given route permutation.
    Uses your existing cost logic.
    """

    route_info = build_route(cities, countries)

    # Load destination cost table for fallback
    cost_table = get_costs(destination)

    # Live flight price
    live_price = get_live_flight_price(origin, destination, "2026-09-01")
    if live_price is None:
        live_price = cost_table["avg_flight_international"]

    # Bus/train scraping
    transit_cost = 0
    for i in range(len(cities) - 1):
        origin_city = cities[i]
        dest_city = cities[i + 1]

        transit_price = get_bus_train_price(origin_city, dest_city, "2026-09-01")
        if transit_price is None:
            transit_price = {"price": cost_table["bus_city_to_city"]}

        transit_cost += transit_price["price"]

    # Multi-country cost tables
    total = 0
    for leg in route_info["route"]:
        origin_costs = leg.get("origin_costs")
        dest_costs = leg.get("destination_costs")

        if origin_costs:
            total += (
                origin_costs["hostel_per_night"] * 7 +
                origin_costs["food_per_day"] * 7 +
                origin_costs["local_transport_per_day"] * 7 +
                origin_costs["bus_city_to_city"]
            )

        if dest_costs:
            total += (
                dest_costs["hostel_per_night"] * 7 +
                dest_costs["food_per_day"] * 7 +
                dest_costs["local_transport_per_day"] * 7 +
                dest_costs["bus_city_to_city"]
            )

    # Add transit + flight
    total += transit_cost
    total += live_price

    return total, route_info

def find_cheapest_route(cities, countries, origin, destination):
    """
    Generates all permutations of cities and finds the cheapest route.
    """

    results = []

    for perm in permutations(cities):
        perm_countries = None
        if countries:
            # reorder countries to match perm
            perm_countries = [countries[cities.index(city)] for city in perm]

        total_cost, route_info = compute_total_cost(
            list(perm),
            perm_countries,
            origin,
            destination
        )

        results.append({
            "route": list(perm),
            "countries": perm_countries,
            "total_cost": total_cost,
            "route_info": route_info
        })

    # Sort by cost
    results.sort(key=lambda x: x["total_cost"])

    return {
        "cheapest": results[0],
        "ranked_routes": results
    }
