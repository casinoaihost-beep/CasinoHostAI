guests = {
    "G0001": {
        "guest_id": "G0001",
        "first_name": "Marco",
        "last_name": "Rossi",
        "tier": "Gold",
        "language": "Italian",
        "country": "Italy",
        "points": 1850,
        "last_visit": "2026-10-05",
        "email": "marco.rossi@example.com",
        "phone": "+393331111111",
        "preferred_game": "Roulette",
        "hotel": True,
        "dinner": True,
        "human_host": "Luca"
    },

    "G0002": {
        "guest_id": "G0002",
        "first_name": "Anna",
        "last_name": "Bianchi",
        "tier": "Silver",
        "language": "Italian",
        "country": "Italy",
        "points": 620,
        "last_visit": "2026-09-28",
        "email": "anna.bianchi@example.com",
        "phone": "+393332222222",
        "preferred_game": "Slots",
        "hotel": False,
        "dinner": True,
        "human_host": None
    },

    "G0003": {
        "guest_id": "G0003",
        "first_name": "Johann",
        "last_name": "Muller",
        "tier": "Bronze",
        "language": "German",
        "country": "Germany",
        "points": 180,
        "last_visit": "2026-08-14",
        "email": "johann.muller@example.com",
        "phone": "+491703333333",
        "preferred_game": "Blackjack",
        "hotel": False,
        "dinner": False,
        "human_host": None
    },

    "G0004": {
        "guest_id": "G0004",
        "first_name": "Ivan",
        "last_name": "Horvat",
        "tier": "VIP Exclusive",
        "language": "Croatian",
        "country": "Croatia",
        "points": 4200,
        "last_visit": "2026-10-10",
        "email": "ivan.horvat@example.com",
        "phone": "+385914444444",
        "preferred_game": "Roulette",
        "hotel": True,
        "dinner": True,
        "human_host": "Vedran"
    },

    "G0005": {
        "guest_id": "G0005",
        "first_name": "Alexander",
        "last_name": "Petrov",
        "tier": "Chairman",
        "language": "Russian",
        "country": "Switzerland",
        "points": 12500,
        "last_visit": "2026-10-12",
        "email": "alexander.petrov@example.com",
        "phone": "+41795555555",
        "preferred_game": "Baccarat",
        "hotel": True,
        "dinner": True,
        "human_host": "VIP Director"
    },

    # NAMJERNO DVA GOSTA ISTOG IMENA
    "G0006": {
        "guest_id": "G0006",
        "first_name": "Marco",
        "last_name": "Rossi",
        "tier": "Silver",
        "language": "Italian",
        "country": "Switzerland",
        "points": 740,
        "last_visit": "2026-09-20",
        "email": "marco.rossi2@example.com",
        "phone": "+41796667777",
        "preferred_game": "Slots",
        "hotel": False,
        "dinner": True,
        "human_host": None
    }
}


def full_name(guest):
    return f"{guest['first_name']} {guest['last_name']}"