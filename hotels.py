hotels = [
    {
        "name": "Grand Hotel Demo",
        "price": 140,
        "distance_km": 0.3,
        "available": True,
        "partner": True
    },

    {
        "name": "Adriatic Palace",
        "price": 110,
        "distance_km": 0.8,
        "available": True,
        "partner": True
    },

    {
        "name": "Sea View Hotel",
        "price": 85,
        "distance_km": 1.4,
        "available": True,
        "partner": False
    }
]


def show_hotels(guest, tier_rules):

    tier = guest["tier"]
    budget = tier_rules[tier]["hotel_budget"]

    print("\n=== HOTEL OPTIONS ===")

    if budget > 0:
        print("Casino budget:", budget, "EUR")
    else:
        print("Casino ne pokriva hotel za ovaj tier.")
        print("AI može pronaći hotel koji gost plaća sam.")

    available = [
        hotel
        for hotel in hotels
        if hotel["available"]
    ]

    available.sort(
        key=lambda hotel: hotel["price"]
    )

    for hotel in available:

        print()
        print(hotel["name"])
        print("Cijena:", hotel["price"], "EUR")
        print("Udaljenost:", hotel["distance_km"], "km")

        print(
            "Partner:",
            "DA" if hotel["partner"] else "NE"
        )

        if budget > 0 and hotel["price"] <= budget:
            print("Casino može pokriti ovaj hotel.")
        else:
            print("Gost plaća sam.")