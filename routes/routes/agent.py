from flask import Blueprint, jsonify, request

from logic.accommodation import get_accommodations
from logic.costs import COST_TABLES, get_costs
from logic.flights import get_live_flight_price
from logic.optimizer import find_cheapest_route
from logic.prompt import SYSTEM_PROMPT
from logic.routing import build_route
from logic.safety import get_safety_flags
from logic.transit import get_bus_train_price
from logic.visa import get_visa_requirements


print("AGENT BLUEPRINT LOADED")
agent_bp = Blueprint("agent", __name__)


@agent_bp.get("/countries")
def countries():
    """Return the countries supported by the travel-planning cost model."""
    return jsonify({
        "countries": [
            country.replace("_", " ").title()
            for country in sorted(COST_TABLES)
        ],
        "count": len(COST_TABLES),
    })


@agent_bp.get("/countries/<string:country>")
def country_data(country):
    """Return cost data for one supported country."""
    costs = get_costs(country)
    if costs is None:
        return jsonify({
            "error": f"No cost data is available for {country}.",
            "available_countries": [
                name.replace("_", " ").title()
                for name in sorted(COST_TABLES)
            ],
        }), 404

    return jsonify({
        "country": country.replace("_", " ").title(),
        "costs": costs,
    })


@agent_bp.route("/plan_trip", methods=["POST"])
def plan_trip():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    origin = data.get("origin")
    destination = data.get("destination")
    if not isinstance(origin, str) or not origin.strip():
        return jsonify({"error": "origin is required."}), 400
    if not isinstance(destination, str) or not destination.strip():
        return jsonify({"error": "destination is required."}), 400

    cost_table = get_costs(destination)
    if cost_table is None:
        return jsonify({"error": f"No cost data is available for {destination}."}), 400

    cities = data.get("cities") or []
    countries = data.get("countries") or []
    durations = data.get("durations") or {}
    user_budget = data.get("budget")
    weekly_budget = data.get("weekly_budget")

    if not isinstance(cities, list) or not all(isinstance(city, str) for city in cities):
        return jsonify({"error": "cities must be a list of strings."}), 400
    if not isinstance(countries, list) or not all(isinstance(country, str) for country in countries):
        return jsonify({"error": "countries must be a list of strings."}), 400
    if not isinstance(durations, dict):
        return jsonify({"error": "durations must be an object."}), 400

    try:
        live_price = get_live_flight_price(origin, destination, "2026-09-01")
    except Exception:
        live_price = None
    live_price = live_price if live_price is not None else cost_table["avg_flight_international"]

    visa_results = []
    for origin_country, destination_country in zip(countries, countries[1:]):
        visa_info = get_visa_requirements(origin_country, destination_country)
        visa_results.append({
            "origin_country": origin_country,
            "destination_country": destination_country,
            "visa": visa_info or {
                "visa_required": None,
                "description": "Visa information unavailable.",
                "documents": [],
                "duration": None,
            },
        })

    transit_results = []
    for origin_city, destination_city in zip(cities, cities[1:]):
        try:
            transit_price = get_bus_train_price(origin_city, destination_city, "2026-09-01")
        except Exception:
            transit_price = None
        transit_price = transit_price or {
            "operator": "N/A",
            "price": cost_table["bus_city_to_city"] or 0,
            "vehicle": "bus",
            "duration": "N/A",
        }
        transit_results.append({
            "origin": origin_city,
            "destination": destination_city,
            "details": transit_price,
        })

    route_info = build_route(cities, countries) if cities else None
    estimated_cost = {
        "accommodation_week": cost_table["hostel_per_night"] * 7,
        "food_week": cost_table["food_per_day"] * 7,
        "local_transport_week": cost_table["local_transport_per_day"] * 7,
        "city_to_city_bus": cost_table["bus_city_to_city"],
        "domestic_flight": cost_table["avg_flight_domestic"],
        "international_flight": cost_table["avg_flight_international"],
        "live_flight_price": live_price,
    }
    total_weekly = sum(estimated_cost[key] for key in (
        "accommodation_week", "food_week", "local_transport_week"
    ))

    multi_country_budget = []
    total_multi_country_cost = live_price
    for leg in (route_info or {}).get("route", []):
        origin_costs = leg.get("origin_costs")
        destination_costs = leg.get("destination_costs")
        origin_days = max(1, int(durations.get(leg["origin_country"], 7))) if origin_costs else 0
        destination_days = max(1, int(durations.get(leg["destination_country"], 7))) if destination_costs else 0

        def country_budget(country, costs, days):
            if not costs:
                return None
            return {
                "country": country,
                "days": days,
                "hostel_total": costs["hostel_per_night"] * days,
                "food_total": costs["food_per_day"] * days,
                "transport_total": costs["local_transport_per_day"] * days,
                "city_to_city_bus": costs["bus_city_to_city"] or 0,
            }

        origin_budget = country_budget(leg["origin_country"], origin_costs, origin_days)
        destination_budget = country_budget(leg["destination_country"], destination_costs, destination_days)
        for budget in (origin_budget, destination_budget):
            if budget:
                total_multi_country_cost += sum(budget[key] for key in (
                    "hostel_total", "food_total", "transport_total", "city_to_city_bus"
                ))
        multi_country_budget.append({
            "origin_city": leg["origin_city"],
            "destination_city": leg["destination_city"],
            "origin_budget": origin_budget,
            "destination_budget": destination_budget,
            "cross_border": leg["cross_border"],
        })

    for transit in transit_results:
        total_multi_country_cost += transit["details"].get("price", 0)

    budget_warnings = []
    if isinstance(user_budget, (int, float)):
        if total_multi_country_cost > user_budget:
            budget_warnings.append({"type": "total_budget_exceeded", "over_by": total_multi_country_cost - user_budget})
        else:
            budget_warnings.append({"type": "total_budget_ok", "remaining": user_budget - total_multi_country_cost})

    cheapest_route_data = None
    if len(cities) > 1:
        cheapest_route_data = find_cheapest_route(cities, countries or None, origin, destination)

    return jsonify({
        "system_prompt_used": SYSTEM_PROMPT,
        "input": {"origin": origin, "destination": destination, "cities": cities, "countries": countries,
                   "durations": durations, "budget": user_budget, "weekly_budget": weekly_budget},
            "stay_length_recommendations": [],
            "optimized_durations": durations,
            "optimized_total_cost": total_multi_country_cost,
            "full_itinerary": [],
        "route_plan": route_info,
        "multi_country_budget": multi_country_budget,
        "total_multi_country_trip_cost": total_multi_country_cost,
        "visa_requirements": visa_results,
        "transit": transit_results,
        "breakdown": estimated_cost,
        "total_weekly_cost": total_weekly,
        "budget_friendly": total_weekly <= 350,
        "cheapest_route": cheapest_route_data["cheapest"] if cheapest_route_data else None,
        "all_route_rankings": cheapest_route_data["ranked_routes"] if cheapest_route_data else None,
        "budget_warnings": budget_warnings,
        "safety_flags": get_safety_flags(destination),
        "accommodations": get_accommodations(destination),
    })
