# rules.py

from urllib.parse import quote


# =========================================================
# GENERAL
# =========================================================

HOST_WHATSAPP_NUMBER = "385955783464"


def normalize_tier(tier):
    value = str(tier or "").strip().lower()

    aliases = {
        "gold": "gold",
        "silver": "silver",
        "vip": "vip",
        "chairman": "chairman",
        "new": "new",
        "new guest": "new",
        "novi": "new",
        "nov gost": "new",
    }

    return aliases.get(value, value)


# =========================================================
# HOTEL POLICY
# =========================================================

HOTEL_POLICIES = {

    "gold": {
        "type": "fixed_cap",
        "night_cap": 150.0,
        "included_nights": 2,
        "maximum_total": 300.0,
    },

    "vip": {
        "type": "fixed_cap",
        "night_cap": 200.0,
        "included_nights": 3,
        "maximum_total": 600.0,
    },

    "silver": {
        "type": "not_included",
    },

    "chairman": {
        "type": "manual_approval",
    },

    "new": {
        "type": "post_play_review",
    },
}


def get_hotel_policy(tier):
    tier = normalize_tier(tier)

    return HOTEL_POLICIES.get(
        tier,
        {
            "type": "manual_approval",
        }
    )


def calculate_hotel_coverage(
    tier,
    requested_nights,
    nightly_room_price,
):

    tier = normalize_tier(tier)
    policy = get_hotel_policy(tier)

    requested_nights = max(
        int(requested_nights),
        0
    )

    nightly_room_price = max(
        float(nightly_room_price),
        0.0
    )

    total_room_cost = (
        requested_nights
        * nightly_room_price
    )

    result = {
        "tier": tier,
        "policy_type": policy["type"],
        "requested_nights": requested_nights,
        "nightly_room_price": nightly_room_price,
        "total_room_cost": total_room_cost,
        "casino_covered": 0.0,
        "guest_room_difference": total_room_cost,
        "included_nights": 0,
        "night_cap": 0.0,
        "maximum_total": 0.0,
        "extras_covered": False,
    }

    if policy["type"] == "fixed_cap":

        included_nights = min(
            requested_nights,
            policy["included_nights"]
        )

        covered_per_night = min(
            nightly_room_price,
            policy["night_cap"]
        )

        casino_covered = (
            included_nights
            * covered_per_night
        )

        casino_covered = min(
            casino_covered,
            policy["maximum_total"]
        )

        guest_difference = max(
            total_room_cost
            - casino_covered,
            0.0
        )

        result.update({
            "casino_covered": casino_covered,
            "guest_room_difference": guest_difference,
            "included_nights": policy["included_nights"],
            "night_cap": policy["night_cap"],
            "maximum_total": policy["maximum_total"],
        })

    return result


# =========================================================
# NEW GUEST HOTEL REIMBURSEMENT
# =========================================================

def build_new_guest_review_ticket(
    guest_name,
    guest_id,
    hotel_cost,
    gaming_loss,
    play_hours,
    game_type,
    notes="",
):

    return {
        "status": "HOST_REVIEW_REQUIRED",
        "guest_name": guest_name,
        "guest_id": guest_id,
        "hotel_cost": float(hotel_cost),
        "gaming_loss": float(gaming_loss),
        "play_hours": float(play_hours),
        "game_type": game_type,
        "notes": notes,
        "automatic_decision": False,
    }


def format_new_guest_ticket(ticket):

    return (
        "GCP HOTEL REIMBURSEMENT REVIEW\n\n"
        f"Guest: {ticket['guest_name']}\n"
        f"Guest ID: {ticket['guest_id']}\n"
        f"Hotel paid by guest: €{ticket['hotel_cost']:.2f}\n"
        f"Gaming loss: €{ticket['gaming_loss']:.2f}\n"
        f"Play duration: {ticket['play_hours']:.1f} h\n"
        f"Game type: {ticket['game_type']}\n"
        f"Notes: {ticket['notes'] or '-'}\n\n"
        "Status: HOST REVIEW REQUIRED\n"
        "No automatic reimbursement decision."
    )


# =========================================================
# RESTAURANT
# Python weekday:
# Monday 0 ... Sunday 6
# =========================================================

DINNER_DAYS = {3, 4, 5, 6}       # Thu-Sun
LUNCH_DAYS = {4, 5, 6}           # Fri-Sun

SILVER_DAYS = {3, 6}             # Thu + Sun


RESTAURANT_SERVICES = {

    "dinner": {
        "days": DINNER_DAYS,
        "from": "19:00",
        "to": "22:00",
        "last_arrival": "21:15",
    },

    "lunch": {
        "days": LUNCH_DAYS,
        "from": "13:00",
        "to": "15:00",
        "last_arrival": "14:15",
    },
}


def restaurant_eligibility(
    tier,
    service,
    weekday,
):

    tier = normalize_tier(tier)

    service_data = RESTAURANT_SERVICES[service]

    service_open = (
        weekday in service_data["days"]
    )

    if tier == "silver":

        tier_allowed = (
            weekday in SILVER_DAYS
        )

    elif tier in {
        "gold",
        "vip",
        "chairman",
    }:

        # Dostupno svaki dan kada restoran radi
        tier_allowed = service_open

    else:

        tier_allowed = False

    return {
        "service_open": service_open,
        "tier_allowed": tier_allowed,
        "eligible": (
            service_open
            and tier_allowed
        ),
        "from": service_data["from"],
        "to": service_data["to"],
        "last_arrival": service_data["last_arrival"],
    }


# =========================================================
# LINKS
# =========================================================

def whatsapp_url(
    message,
    phone=HOST_WHATSAPP_NUMBER
):

    phone = "".join(
        ch for ch in str(phone)
        if ch.isdigit()
    )

    return (
        f"https://wa.me/{phone}"
        f"?text={quote(message)}"
    )


def mailto_url(
    email,
    subject="Grand Casino Portorož",
    body=""
):

    if not email or email == "-":
        return None

    return (
        f"mailto:{email}"
        f"?subject={quote(subject)}"
        f"&body={quote(body)}"
    )


def tel_url(phone):

    if not phone or phone == "-":
        return None

    clean = "".join(
        ch for ch in str(phone)
        if ch.isdigit() or ch == "+"
    )

    return f"tel:{clean}"