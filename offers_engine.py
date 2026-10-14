# offers_engine.py

from datetime import datetime

from activity import (
    guest_statistics,
    guest_primary_game,
    average_days_between_visits,
    guest_last_visit,
    guest_game_type_statistics,
)

from rules import (
    normalize_tier,
    get_hotel_policy,
)


# =========================================================
# SAFETY / CONTACT RULES
# =========================================================
#
# Ovaj engine NE SMIJE preporučiti marketinški kontakt ako
# gost ima zabranu kontakta, self-exclusion ili blokadu.
#
# Kasnije će se ti podaci čitati iz prave baze.
# =========================================================


def contact_allowed(
    marketing_allowed=True,
    self_excluded=False,
    blocked=False,
    do_not_contact=False,
):

    if self_excluded:
        return False

    if blocked:
        return False

    if do_not_contact:
        return False

    if not marketing_allowed:
        return False

    return True


# =========================================================
# DAYS SINCE LAST VISIT
# =========================================================

def days_since_last_visit(
    guest_id,
    now=None,
):

    if now is None:
        now = datetime.now()

    last_visit = guest_last_visit(
        guest_id
    )

    if not last_visit:
        return None

    arrival = last_visit.get(
        "arrival"
    )

    if not arrival:
        return None

    difference = now - arrival

    return max(
        difference.days,
        0
    )


# =========================================================
# INACTIVITY STATUS
# =========================================================
#
# Ovo nisu financijska/promotivna pravila.
# Ovo su samo CRM statusi za hosta.
#
# Kasnije ih možemo promijeniti bez diranja web aplikacije.
# =========================================================

INACTIVITY_LEVELS = [

    {
        "min_days": 60,
        "level": "REACTIVATION",
        "priority": "HIGH",
    },

    {
        "min_days": 30,
        "level": "INACTIVE",
        "priority": "MEDIUM",
    },

    {
        "min_days": 14,
        "level": "FOLLOW_UP",
        "priority": "NORMAL",
    },

    {
        "min_days": 0,
        "level": "ACTIVE",
        "priority": "LOW",
    },
]


def inactivity_status(
    guest_id,
):

    days = days_since_last_visit(
        guest_id
    )

    if days is None:

        return {
            "days_since_last_visit": None,
            "level": "NEW_OR_UNKNOWN",
            "priority": "NORMAL",
        }

    for rule in INACTIVITY_LEVELS:

        if days >= rule["min_days"]:

            return {
                "days_since_last_visit": days,
                "level": rule["level"],
                "priority": rule["priority"],
            }

    return {
        "days_since_last_visit": days,
        "level": "ACTIVE",
        "priority": "LOW",
    }


# =========================================================
# HOTEL RECOMMENDATION
# =========================================================

def hotel_recommendation(
    tier,
):

    normalized = normalize_tier(
        tier
    )

    policy = get_hotel_policy(
        normalized
    )

    policy_type = policy.get(
        "type"
    )

    if policy_type == "fixed_cap":

        return {
            "eligible": True,
            "approval": "RULE_BASED",
            "type": "HOTEL_BENEFIT",
            "included_nights":
                policy.get(
                    "included_nights",
                    0
                ),
            "night_cap":
                policy.get(
                    "night_cap",
                    0.0
                ),
            "maximum_total":
                policy.get(
                    "maximum_total",
                    0.0
                ),
            "message":
                "Hotel benefit available under current tier rules.",
        }

    if policy_type == "post_play_review":

        return {
            "eligible": False,
            "approval": "HOST_REVIEW",
            "type": "HOTEL_REIMBURSEMENT_REVIEW",
            "message":
                "Guest initially pays hotel. Reimbursement requires post-play host review.",
        }

    if policy_type == "manual_approval":

        return {
            "eligible": None,
            "approval": "MANUAL",
            "type": "HOTEL_MANUAL_APPROVAL",
            "message":
                "Hotel benefit requires host or management approval.",
        }

    return {
        "eligible": False,
        "approval": "NONE",
        "type": "NO_AUTOMATIC_HOTEL",
        "message":
            "No automatic hotel benefit under current rules.",
    }


# =========================================================
# GAMING PROFILE
# =========================================================

def build_gaming_profile(
    guest_id,
):

    stats = guest_statistics(
        guest_id
    )

    primary_game = guest_primary_game(
        guest_id
    )

    game_stats = (
        guest_game_type_statistics(
            guest_id
        )
    )

    return {
        "visit_count":
            stats.get(
                "visits",
                0
            ),

        "game_sessions":
            stats.get(
                "game_sessions",
                0
            ),

        "total_gaming_hours":
            stats.get(
                "total_gaming_hours",
                0.0
            ),

        "average_game_duration":
            stats.get(
                "average_game_duration",
                0.0
            ),

        "casino_win_loss":
            stats.get(
                "casino_win_loss",
                0.0
            ),

        "guest_total_losses":
            stats.get(
                "guest_total_losses",
                0.0
            ),

        "guest_total_winnings":
            stats.get(
                "guest_total_winnings",
                0.0
            ),

        "theoretical_value":
            stats.get(
                "theoretical_value",
                0.0
            ),

        "turnover":
            stats.get(
                "turnover",
                0.0
            ),

        "average_bet":
            stats.get(
                "average_bet",
                0.0
            ),

        "primary_game":
            primary_game,

        "game_breakdown":
            game_stats,

        "average_days_between_visits":
            average_days_between_visits(
                guest_id
            ),
    }


# =========================================================
# HOST ACTIONS
# =========================================================

def build_host_actions(
    guest_id,
    tier,
    marketing_allowed=True,
    self_excluded=False,
    blocked=False,
    do_not_contact=False,
):

    actions = []

    normalized_tier = normalize_tier(
        tier
    )

    inactivity = inactivity_status(
        guest_id
    )

    can_contact = contact_allowed(
        marketing_allowed=
            marketing_allowed,

        self_excluded=
            self_excluded,

        blocked=
            blocked,

        do_not_contact=
            do_not_contact,
    )

    days = inactivity.get(
        "days_since_last_visit"
    )

    level = inactivity.get(
        "level"
    )

    # -----------------------------------------------------
    # CONTACT PROHIBITED
    # -----------------------------------------------------

    if not can_contact:

        actions.append({
            "action": "NO_MARKETING_CONTACT",
            "priority": "CRITICAL",
            "automatic": True,
            "message":
                "Marketing contact is not permitted for this guest.",
        })

        return actions


    # -----------------------------------------------------
    # NEW / UNKNOWN
    # -----------------------------------------------------

    if level == "NEW_OR_UNKNOWN":

        actions.append({
            "action": "HOST_REVIEW",
            "priority": "NORMAL",
            "automatic": False,
            "message":
                "No previous visit history found. Host review recommended.",
        })


    # -----------------------------------------------------
    # 14+ DAYS
    # -----------------------------------------------------

    elif level == "FOLLOW_UP":

        actions.append({
            "action": "HOST_FOLLOW_UP",
            "priority": "NORMAL",
            "automatic": False,
            "message":
                f"Guest has not visited for {days} days. Consider personal host follow-up.",
        })


    # -----------------------------------------------------
    # 30+ DAYS
    # -----------------------------------------------------

    elif level == "INACTIVE":

        actions.append({
            "action": "INACTIVE_GUEST_REVIEW",
            "priority": "MEDIUM",
            "automatic": False,
            "message":
                f"Guest has not visited for {days} days. Add to inactive guest review list.",
        })


    # -----------------------------------------------------
    # 60+ DAYS
    # -----------------------------------------------------

    elif level == "REACTIVATION":

        actions.append({
            "action": "REACTIVATION_REVIEW",
            "priority": "HIGH",
            "automatic": False,
            "message":
                f"Guest has not visited for {days} days. Host may prepare a reactivation contact if permitted.",
        })


    # -----------------------------------------------------
    # ACTIVE
    # -----------------------------------------------------

    else:

        actions.append({
            "action": "ACTIVE_GUEST",
            "priority": "LOW",
            "automatic": True,
            "message":
                "Guest is currently within the active visit window.",
        })


    # -----------------------------------------------------
    # TIER-SPECIFIC HOST NOTES
    # -----------------------------------------------------

    if normalized_tier == "gold":

        actions.append({
            "action": "CHECK_GOLD_BENEFITS",
            "priority": "NORMAL",
            "automatic": True,
            "message":
                "Check Gold hotel and dining eligibility for next visit.",
        })

    elif normalized_tier == "vip":

        actions.append({
            "action": "CHECK_VIP_BENEFITS",
            "priority": "NORMAL",
            "automatic": True,
            "message":
                "Check VIP hotel, dining and host services for next visit.",
        })

    elif normalized_tier == "chairman":

        actions.append({
            "action": "CHAIRMAN_REVIEW",
            "priority": "HIGH",
            "automatic": False,
            "message":
                "Chairman guest: review benefits with host or management.",
        })


    return actions


# =========================================================
# OFFER / SERVICE RECOMMENDATIONS
# =========================================================

def build_service_recommendations(
    guest_id,
    tier,
):

    profile = build_gaming_profile(
        guest_id
    )

    recommendations = []

    hotel = hotel_recommendation(
        tier
    )

    recommendations.append({
        "category": "HOTEL",
        "recommendation": hotel,
    })


    # -----------------------------------------------------
    # PREFERRED GAME
    # -----------------------------------------------------

    primary_game = profile.get(
        "primary_game"
    )

    if primary_game:

        recommendations.append({
            "category": "GAMING_PREFERENCE",
            "recommendation": {
                "type": "PRIMARY_GAME",
                "value": primary_game,
                "approval": "INFORMATIONAL",
                "message":
                    f"Guest's primary game by playing time is {primary_game}.",
            },
        })


    # -----------------------------------------------------
    # DINING
    # -----------------------------------------------------

    normalized_tier = normalize_tier(
        tier
    )

    if normalized_tier in {
        "silver",
        "gold",
        "vip",
        "chairman",
    }:

        recommendations.append({
            "category": "DINING",
            "recommendation": {
                "type": "CHECK_DINING_ELIGIBILITY",
                "approval": "RULE_BASED",
                "message":
                    "Check restaurant eligibility for the selected date and service.",
            },
        })


    # -----------------------------------------------------
    # PERSONAL HOST CONTACT
    # -----------------------------------------------------

    inactivity = inactivity_status(
        guest_id
    )

    if inactivity.get(
        "level"
    ) in {
        "FOLLOW_UP",
        "INACTIVE",
        "REACTIVATION",
    }:

        recommendations.append({
            "category": "HOST_CONTACT",
            "recommendation": {
                "type": "PERSONAL_CONTACT_REVIEW",
                "approval": "HOST",
                "message":
                    "Personal host contact may be appropriate, subject to contact permissions.",
            },
        })


    return recommendations


# =========================================================
# COMPLETE HOST SNAPSHOT
# =========================================================

def build_host_snapshot(
    guest_id,
    tier,
    marketing_allowed=True,
    self_excluded=False,
    blocked=False,
    do_not_contact=False,
):

    gaming_profile = (
        build_gaming_profile(
            guest_id
        )
    )

    inactivity = (
        inactivity_status(
            guest_id
        )
    )

    host_actions = (
        build_host_actions(
            guest_id=guest_id,
            tier=tier,
            marketing_allowed=
                marketing_allowed,
            self_excluded=
                self_excluded,
            blocked=
                blocked,
            do_not_contact=
                do_not_contact,
        )
    )

    service_recommendations = (
        build_service_recommendations(
            guest_id,
            tier
        )
    )

    hotel = hotel_recommendation(
        tier
    )

    return {

        "guest_id":
            str(guest_id),

        "tier":
            normalize_tier(
                tier
            ),

        "gaming_profile":
            gaming_profile,

        "inactivity":
            inactivity,

        "hotel":
            hotel,

        "host_actions":
            host_actions,

        "service_recommendations":
            service_recommendations,

        "contact_allowed":
            contact_allowed(
                marketing_allowed=
                    marketing_allowed,

                self_excluded=
                    self_excluded,

                blocked=
                    blocked,

                do_not_contact=
                    do_not_contact,
            ),
    }


# =========================================================
# TEXT SUMMARY FOR REPORTS / EMAILS
# =========================================================

def host_snapshot_text(
    snapshot
):

    gaming = snapshot.get(
        "gaming_profile",
        {}
    )

    inactivity = snapshot.get(
        "inactivity",
        {}
    )

    lines = [

        "CASINO HOST AI — GUEST SNAPSHOT",
        "",

        f"Guest ID: {snapshot.get('guest_id')}",
        f"Tier: {snapshot.get('tier')}",

        "",

        f"Visits: {gaming.get('visit_count', 0)}",

        f"Gaming sessions: {gaming.get('game_sessions', 0)}",

        (
            "Total gaming hours: "
            f"{gaming.get('total_gaming_hours', 0):.1f}"
        ),

        (
            "Average gaming session: "
            f"{gaming.get('average_game_duration', 0):.1f} h"
        ),

        (
            "Primary game: "
            f"{gaming.get('primary_game') or '-'}"
        ),

        (
            "Average bet: €"
            f"{gaming.get('average_bet', 0):.2f}"
        ),

        (
            "Turnover: €"
            f"{gaming.get('turnover', 0):.2f}"
        ),

        (
            "Casino Win/Loss: €"
            f"{gaming.get('casino_win_loss', 0):.2f}"
        ),

        (
            "Theoretical: €"
            f"{gaming.get('theoretical_value', 0):.2f}"
        ),

        "",

        (
            "Days since last visit: "
            f"{inactivity.get('days_since_last_visit')}"
        ),

        (
            "CRM status: "
            f"{inactivity.get('level')}"
        ),

        "",

        (
            "Marketing contact allowed: "
            f"{snapshot.get('contact_allowed')}"
        ),
    ]

    return "\n".join(
        lines
    )