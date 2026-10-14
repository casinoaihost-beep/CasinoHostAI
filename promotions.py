promotions = [
    {
        "name": "Golden Weekend",
        "tiers": [
            "Gold",
            "VIP Exclusive",
            "Chairman"
        ]
    },

    {
        "name": "Dinner Night",
        "tiers": [
            "Silver",
            "Gold",
            "VIP Exclusive",
            "Chairman"
        ]
    },

    {
        "name": "VIP Luxury Weekend",
        "tiers": [
            "VIP Exclusive",
            "Chairman"
        ]
    }
]


def show_promotions(guest):

    print("\n=== PROMOCIJE ===")

    found = False

    for promotion in promotions:

        if guest["tier"] in promotion["tiers"]:

            print("-", promotion["name"])
            found = True

    if not found:
        print("Trenutno nema posebnih promocija.")