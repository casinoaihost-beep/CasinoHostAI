# activity.py

from datetime import datetime, timedelta
from statistics import mean

from guests import guests


# =========================================================
# GAME TYPES
# =========================================================

GAME_TYPES = [
    "Slots",
    "Roulette",
    "Blackjack",
    "Baccarat",
    "Poker",
    "Electronic Roulette",
    "Mixed Play",
    "Other",
]


# =========================================================
# IN-MEMORY DEMO DATABASE
# =========================================================

VISITS = []


# =========================================================
# HELPERS
# =========================================================

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_datetime(value):

    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    try:
        return datetime.fromisoformat(
            str(value)
        )

    except ValueError:
        return None


def normalize_game_type(game_type):

    value = str(
        game_type or ""
    ).strip().lower()

    aliases = {
        "slot": "Slots",
        "slots": "Slots",
        "roulette": "Roulette",
        "rulet": "Roulette",
        "blackjack": "Blackjack",
        "black jack": "Blackjack",
        "baccarat": "Baccarat",
        "baccara": "Baccarat",
        "poker": "Poker",
        "electronic roulette": "Electronic Roulette",
        "electronic": "Electronic Roulette",
        "mixed": "Mixed Play",
        "mixed play": "Mixed Play",
    }

    return aliases.get(
        value,
        game_type or "Other"
    )


# =========================================================
# CREATE GAME SESSION
# =========================================================

def create_game_session(
    game_type,
    duration_hours,
    casino_win_loss=0.0,
    theoretical_value=0.0,
    average_bet=0.0,
    turnover=0.0,
    location="",
    table_or_machine="",
    notes="",
):

    return {
        "game_type": normalize_game_type(
            game_type
        ),

        "duration_hours": max(
            safe_float(
                duration_hours
            ),
            0.0
        ),

        # Positive = guest lost / casino won
        # Negative = guest won / casino lost
        "casino_win_loss": safe_float(
            casino_win_loss
        ),

        "theoretical_value": max(
            safe_float(
                theoretical_value
            ),
            0.0
        ),

        "average_bet": max(
            safe_float(
                average_bet
            ),
            0.0
        ),

        "turnover": max(
            safe_float(
                turnover
            ),
            0.0
        ),

        "location": str(
            location or ""
        ),

        "table_or_machine": str(
            table_or_machine or ""
        ),

        "notes": str(
            notes or ""
        ),
    }


# =========================================================
# CREATE VISIT
# =========================================================

def create_visit(
    guest_id,
    arrival,
    departure=None,
    host="",
    visit_type="Regular",
    hotel_name="",
    hotel_nights=0,
    hotel_total_cost=0.0,
    casino_hotel_coverage=0.0,
    reimbursement_ticket=0.0,
    promotion="",
    notes="",
):

    arrival_dt = parse_datetime(
        arrival
    )

    departure_dt = parse_datetime(
        departure
    )

    visit = {
        "visit_id":
            f"VISIT-{len(VISITS) + 1:05d}",

        "guest_id":
            str(guest_id),

        "arrival":
            arrival_dt,

        "departure":
            departure_dt,

        "host":
            str(
                host or ""
            ),

        "visit_type":
            str(
                visit_type or "Regular"
            ),

        "hotel": {
            "name":
                str(
                    hotel_name or ""
                ),

            "nights":
                max(
                    safe_int(
                        hotel_nights
                    ),
                    0
                ),

            "total_cost":
                max(
                    safe_float(
                        hotel_total_cost
                    ),
                    0.0
                ),

            "casino_coverage":
                max(
                    safe_float(
                        casino_hotel_coverage
                    ),
                    0.0
                ),

            "reimbursement_ticket":
                max(
                    safe_float(
                        reimbursement_ticket
                    ),
                    0.0
                ),
        },

        "promotion":
            str(
                promotion or ""
            ),

        "notes":
            str(
                notes or ""
            ),

        "games": [],
    }

    VISITS.append(
        visit
    )

    return visit


# =========================================================
# ADD GAME
# =========================================================

def add_game_to_visit(
    visit,
    game_type,
    duration_hours,
    casino_win_loss=0.0,
    theoretical_value=0.0,
    average_bet=0.0,
    turnover=0.0,
    location="",
    table_or_machine="",
    notes="",
):

    game = create_game_session(
        game_type=game_type,
        duration_hours=duration_hours,
        casino_win_loss=casino_win_loss,
        theoretical_value=theoretical_value,
        average_bet=average_bet,
        turnover=turnover,
        location=location,
        table_or_machine=table_or_machine,
        notes=notes,
    )

    visit["games"].append(
        game
    )

    return game


# =========================================================
# VISIT DURATION
# =========================================================

def visit_duration_hours(
    visit
):

    arrival = visit.get(
        "arrival"
    )

    departure = visit.get(
        "departure"
    )

    if not arrival or not departure:
        return 0.0

    seconds = (
        departure
        - arrival
    ).total_seconds()

    if seconds < 0:
        return 0.0

    return seconds / 3600


# =========================================================
# VISIT GAMING SUMMARY
# =========================================================

def visit_gaming_summary(
    visit
):

    games = visit.get(
        "games",
        []
    )

    total_hours = sum(
        safe_float(
            game.get(
                "duration_hours"
            )
        )
        for game in games
    )

    casino_win_loss = sum(
        safe_float(
            game.get(
                "casino_win_loss"
            )
        )
        for game in games
    )

    theoretical = sum(
        safe_float(
            game.get(
                "theoretical_value"
            )
        )
        for game in games
    )

    turnover = sum(
        safe_float(
            game.get(
                "turnover"
            )
        )
        for game in games
    )

    bets = [
        safe_float(
            game.get(
                "average_bet"
            )
        )
        for game in games
        if safe_float(
            game.get(
                "average_bet"
            )
        ) > 0
    ]

    average_bet = (
        mean(bets)
        if bets
        else 0.0
    )

    return {
        "game_sessions":
            len(games),

        "gaming_hours":
            total_hours,

        "casino_win_loss":
            casino_win_loss,

        "theoretical_value":
            theoretical,

        "turnover":
            turnover,

        "average_bet":
            average_bet,
    }


# =========================================================
# GUEST VISITS
# =========================================================

def guest_visits(
    guest_id
):

    guest_id = str(
        guest_id
    )

    results = [
        visit
        for visit in VISITS
        if str(
            visit.get(
                "guest_id"
            )
        ) == guest_id
    ]

    results.sort(
        key=lambda visit:
            visit.get("arrival")
            or datetime.min,
        reverse=True
    )

    return results


# =========================================================
# LAST VISIT
# =========================================================

def guest_last_visit(
    guest_id
):

    visits = guest_visits(
        guest_id
    )

    if not visits:
        return None

    return visits[0]


# =========================================================
# GAME SESSIONS
# =========================================================

def guest_game_sessions(
    guest_id
):

    sessions = []

    for visit in guest_visits(
        guest_id
    ):

        for game in visit.get(
            "games",
            []
        ):

            session = dict(
                game
            )

            session["visit_id"] = (
                visit.get(
                    "visit_id"
                )
            )

            session["visit_date"] = (
                visit.get(
                    "arrival"
                )
            )

            sessions.append(
                session
            )

    return sessions


# =========================================================
# GUEST STATISTICS
# =========================================================

def guest_statistics(
    guest_id
):

    visits = guest_visits(
        guest_id
    )

    games = guest_game_sessions(
        guest_id
    )

    total_gaming_hours = sum(
        safe_float(
            game.get(
                "duration_hours"
            )
        )
        for game in games
    )

    total_win_loss = sum(
        safe_float(
            game.get(
                "casino_win_loss"
            )
        )
        for game in games
    )

    total_theoretical = sum(
        safe_float(
            game.get(
                "theoretical_value"
            )
        )
        for game in games
    )

    total_turnover = sum(
        safe_float(
            game.get(
                "turnover"
            )
        )
        for game in games
    )

    positive_losses = sum(
        max(
            safe_float(
                game.get(
                    "casino_win_loss"
                )
            ),
            0.0
        )
        for game in games
    )

    guest_winnings = sum(
        abs(
            min(
                safe_float(
                    game.get(
                        "casino_win_loss"
                    )
                ),
                0.0
            )
        )
        for game in games
    )

    game_hours = [
        safe_float(
            game.get(
                "duration_hours"
            )
        )
        for game in games
        if safe_float(
            game.get(
                "duration_hours"
            )
        ) > 0
    ]

    average_game_duration = (
        mean(game_hours)
        if game_hours
        else 0.0
    )

    bets = [
        safe_float(
            game.get(
                "average_bet"
            )
        )
        for game in games
        if safe_float(
            game.get(
                "average_bet"
            )
        ) > 0
    ]

    average_bet = (
        mean(bets)
        if bets
        else 0.0
    )

    hotel_cost = sum(
        safe_float(
            visit.get(
                "hotel",
                {}
            ).get(
                "total_cost"
            )
        )
        for visit in visits
    )

    hotel_coverage = sum(
        safe_float(
            visit.get(
                "hotel",
                {}
            ).get(
                "casino_coverage"
            )
        )
        for visit in visits
    )

    reimbursement = sum(
        safe_float(
            visit.get(
                "hotel",
                {}
            ).get(
                "reimbursement_ticket"
            )
        )
        for visit in visits
    )

    last_visit = (
        visits[0]
        if visits
        else None
    )

    return {
        "guest_id":
            str(guest_id),

        "visits":
            len(visits),

        "game_sessions":
            len(games),

        "total_gaming_hours":
            total_gaming_hours,

        "average_game_duration":
            average_game_duration,

        "casino_win_loss":
            total_win_loss,

        "guest_total_losses":
            positive_losses,

        "guest_total_winnings":
            guest_winnings,

        "theoretical_value":
            total_theoretical,

        "turnover":
            total_turnover,

        "average_bet":
            average_bet,

        "hotel_total_cost":
            hotel_cost,

        "casino_hotel_coverage":
            hotel_coverage,

        "hotel_reimbursements":
            reimbursement,

        "last_visit":
            (
                last_visit.get(
                    "arrival"
                )
                if last_visit
                else None
            ),
    }


# =========================================================
# GAME TYPE STATISTICS
# =========================================================

def guest_game_type_statistics(
    guest_id
):

    sessions = guest_game_sessions(
        guest_id
    )

    stats = {}

    for session in sessions:

        game_type = session.get(
            "game_type",
            "Other"
        )

        if game_type not in stats:

            stats[game_type] = {
                "sessions": 0,
                "hours": 0.0,
                "casino_win_loss": 0.0,
                "theoretical_value": 0.0,
                "turnover": 0.0,
            }

        stats[game_type]["sessions"] += 1

        stats[game_type]["hours"] += (
            safe_float(
                session.get(
                    "duration_hours"
                )
            )
        )

        stats[game_type]["casino_win_loss"] += (
            safe_float(
                session.get(
                    "casino_win_loss"
                )
            )
        )

        stats[game_type]["theoretical_value"] += (
            safe_float(
                session.get(
                    "theoretical_value"
                )
            )
        )

        stats[game_type]["turnover"] += (
            safe_float(
                session.get(
                    "turnover"
                )
            )
        )

    return stats


# =========================================================
# PRIMARY GAME
# =========================================================

def guest_primary_game(
    guest_id
):

    stats = guest_game_type_statistics(
        guest_id
    )

    if not stats:
        return None

    return max(
        stats,
        key=lambda game:
            stats[game]["hours"]
    )


# =========================================================
# VISIT FREQUENCY
# =========================================================

def average_days_between_visits(
    guest_id
):

    visits = guest_visits(
        guest_id
    )

    dates = [
        visit.get(
            "arrival"
        )
        for visit in visits
        if visit.get(
            "arrival"
        )
    ]

    if len(dates) < 2:
        return None

    dates = sorted(
        dates
    )

    differences = []

    for i in range(
        1,
        len(dates)
    ):

        difference = (
            dates[i]
            - dates[i - 1]
        ).total_seconds()

        differences.append(
            difference / 86400
        )

    return (
        mean(differences)
        if differences
        else None
    )


# =========================================================
# AI CONTEXT
# =========================================================

def build_guest_ai_context(
    guest_id
):

    statistics = guest_statistics(
        guest_id
    )

    return {
        "guest_id":
            str(guest_id),

        "visit_count":
            statistics["visits"],

        "last_visit":
            statistics["last_visit"],

        "total_gaming_hours":
            statistics[
                "total_gaming_hours"
            ],

        "average_game_duration":
            statistics[
                "average_game_duration"
            ],

        "casino_win_loss":
            statistics[
                "casino_win_loss"
            ],

        "guest_total_losses":
            statistics[
                "guest_total_losses"
            ],

        "guest_total_winnings":
            statistics[
                "guest_total_winnings"
            ],

        "theoretical_value":
            statistics[
                "theoretical_value"
            ],

        "turnover":
            statistics[
                "turnover"
            ],

        "average_bet":
            statistics[
                "average_bet"
            ],

        "primary_game":
            guest_primary_game(
                guest_id
            ),

        "average_days_between_visits":
            average_days_between_visits(
                guest_id
            ),

        "hotel_total_cost":
            statistics[
                "hotel_total_cost"
            ],

        "casino_hotel_coverage":
            statistics[
                "casino_hotel_coverage"
            ],

        "hotel_reimbursements":
            statistics[
                "hotel_reimbursements"
            ],
    }


# =========================================================
# DEMO DATA GENERATOR
# =========================================================

def load_demo_activity():

    if VISITS:
        return

    now = datetime.now()

    game_cycle = [
        "Slots",
        "Roulette",
        "Blackjack",
        "Baccarat",
        "Electronic Roulette",
        "Mixed Play",
    ]

    host_cycle = [
        "Vedran",
        "Anna",
        "Luca",
        "Maja",
    ]

    # -----------------------------------------------------
    # Create demo history for first 70 guests.
    # Remaining guests act as new / no-history guests.
    # -----------------------------------------------------

    guest_ids = list(
        guests.keys()
    )

    for index, guest_id in enumerate(
        guest_ids[:70],
        start=1
    ):

        guest = guests[
            guest_id
        ]

        tier = str(
            guest.get(
                "tier",
                "new"
            )
        ).lower()

        # ---------------------------------------------
        # Number of demo visits by tier
        # ---------------------------------------------

        if tier == "chairman":
            visit_count = 6

        elif tier == "vip":
            visit_count = 5

        elif tier == "gold":
            visit_count = 4

        elif tier == "silver":
            visit_count = 3

        else:
            visit_count = 1

        # ---------------------------------------------
        # Some guests deliberately have longer inactivity
        # for CRM 14 / 30 / 60-day tests.
        # ---------------------------------------------

        inactivity_pattern = [
            3,
            8,
            15,
            22,
            35,
            47,
            65,
            80,
        ]

        days_since_last = inactivity_pattern[
            (index - 1)
            % len(
                inactivity_pattern
            )
        ]

        for visit_number in range(
            visit_count
        ):

            days_back = (
                days_since_last
                + (
                    visit_number
                    * (
                        9
                        + (
                            index % 8
                        )
                    )
                )
            )

            hour = (
                18
                + (
                    index % 4
                )
            )

            arrival = (
                now
                - timedelta(
                    days=days_back
                )
            ).replace(
                hour=hour,
                minute=30,
                second=0,
                microsecond=0,
            )

            duration_visit = (
                5
                + (
                    index % 4
                )
            )

            departure = (
                arrival
                + timedelta(
                    hours=duration_visit
                )
            )

            host = host_cycle[
                (
                    index
                    + visit_number
                )
                % len(
                    host_cycle
                )
            ]

            # -----------------------------------------
            # HOTEL
            # -----------------------------------------

            hotel_name = ""
            hotel_nights = 0
            hotel_total_cost = 0.0
            hotel_coverage = 0.0

            if tier in {
                "gold",
                "vip",
                "chairman",
            } and visit_number == 0:

                hotel_name = (
                    "Partner Hotel Portorož"
                )

                if tier == "gold":

                    hotel_nights = 2

                    hotel_total_cost = (
                        240
                        + (
                            index % 4
                        )
                        * 20
                    )

                    hotel_coverage = min(
                        hotel_total_cost,
                        300
                    )

                elif tier == "vip":

                    hotel_nights = 3

                    hotel_total_cost = (
                        450
                        + (
                            index % 4
                        )
                        * 40
                    )

                    hotel_coverage = min(
                        hotel_total_cost,
                        600
                    )

                else:

                    hotel_nights = 3

                    hotel_total_cost = (
                        550
                        + (
                            index % 5
                        )
                        * 50
                    )

                    hotel_coverage = (
                        hotel_total_cost
                    )

            # -----------------------------------------
            # VISIT
            # -----------------------------------------

            visit = create_visit(
                guest_id=guest_id,
                arrival=arrival,
                departure=departure,
                host=host,
                visit_type=(
                    "VIP Weekend"
                    if visit_number == 0
                    and tier in {
                        "gold",
                        "vip",
                        "chairman",
                    }
                    else "Regular"
                ),
                hotel_name=hotel_name,
                hotel_nights=hotel_nights,
                hotel_total_cost=hotel_total_cost,
                casino_hotel_coverage=hotel_coverage,
                promotion=(
                    "Dinner Invitation"
                    if visit_number % 2 == 0
                    else ""
                ),
                notes="Demo activity",
            )

            # -----------------------------------------
            # GAME SESSION 1
            # -----------------------------------------

            primary_game = game_cycle[
                index
                % len(
                    game_cycle
                )
            ]

            duration_1 = (
                1.5
                + (
                    index % 6
                )
                * 0.5
            )

            bet_base = {
                "chairman": 150,
                "vip": 80,
                "gold": 35,
                "silver": 15,
                "new": 8,
            }.get(
                tier,
                10
            )

            average_bet_1 = (
                bet_base
                + (
                    visit_number
                    * 5
                )
            )

            turnover_1 = (
                average_bet_1
                * duration_1
                * 150
            )

            theoretical_1 = (
                turnover_1
                * (
                    0.025
                    + (
                        index % 3
                    )
                    * 0.005
                )
            )

            # Positive/negative mixed demo results
            if (
                index
                + visit_number
            ) % 5 == 0:

                win_loss_1 = (
                    -(
                        250
                        + index
                        * 15
                    )
                )

            else:

                win_loss_1 = (
                    300
                    + index
                    * 25
                    + visit_number
                    * 100
                )

            add_game_to_visit(
                visit,
                game_type=primary_game,
                duration_hours=duration_1,
                casino_win_loss=win_loss_1,
                theoretical_value=theoretical_1,
                average_bet=average_bet_1,
                turnover=turnover_1,
                location=(
                    "Slots Area"
                    if primary_game
                    in {
                        "Slots",
                        "Electronic Roulette"
                    }
                    else "Live Tables"
                ),
                notes="Demo session",
            )

            # -----------------------------------------
            # SECOND SESSION FOR PREMIUM GUESTS
            # -----------------------------------------

            if tier in {
                "chairman",
                "vip",
                "gold",
            }:

                second_game = game_cycle[
                    (
                        index
                        + 2
                    )
                    % len(
                        game_cycle
                    )
                ]

                duration_2 = (
                    1.0
                    + (
                        index % 4
                    )
                    * 0.5
                )

                average_bet_2 = max(
                    average_bet_1
                    * 0.75,
                    5
                )

                turnover_2 = (
                    average_bet_2
                    * duration_2
                    * 120
                )

                theoretical_2 = (
                    turnover_2
                    * 0.03
                )

                if index % 7 == 0:

                    win_loss_2 = (
                        -500
                        - index * 10
                    )

                else:

                    win_loss_2 = (
                        180
                        + index * 20
                    )

                add_game_to_visit(
                    visit,
                    game_type=second_game,
                    duration_hours=duration_2,
                    casino_win_loss=win_loss_2,
                    theoretical_value=theoretical_2,
                    average_bet=average_bet_2,
                    turnover=turnover_2,
                    location="Live Tables",
                    notes="Secondary demo session",
                )


# =========================================================
# LOAD DEMO DATA
# =========================================================

load_demo_activity()