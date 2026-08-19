from logic.costs import get_costs

def build_route(cities, countries=None):
    """
    Multi-country routing with cost tables per country.
    """

    if not cities or len(cities) < 2:
        return {
            "route": [],
            "total_legs": 0
        }

    route = []

    for i in range(len(cities) - 1):
        origin_city = cities[i]
        dest_city = cities[i + 1]

        origin_country = countries[i] if countries and i < len(countries) else None
        dest_country = countries[i + 1] if countries and i + 1 < len(countries) else None

        cross_border = (
            origin_country is not None and
            dest_country is not None and
            origin_country != dest_country
        )

        # ⭐ Load cost tables for each country
        origin_costs = get_costs(origin_country) if origin_country else None
        dest_costs = get_costs(dest_country) if dest_country else None

        route.append({
            "origin_city": origin_city,
            "origin_country": origin_country,
            "origin_costs": origin_costs,

            "destination_city": dest_city,
            "destination_country": dest_country,
            "destination_costs": dest_costs,

            "cross_border": cross_border
        })

    return {
        "route": route,
        "total_legs": len(route)
    }
