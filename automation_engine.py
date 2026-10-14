# automation_engine.py

from datetime import datetime, timedelta

from activity import (
    VISITS,
    guest_visits,
    guest_statistics,
)

from offers_engine import (
    build_host_snapshot,
    inactivity_status,
    contact_allowed,
)


# =========================================================
# AUTOMATION SETTINGS
# =========================================================
#
# Ove vrijednosti kasnije možemo mijenjati
# bez diranja ostatka sustava.
#
# =========================================================

AUTOMATION_CONFIG = {

    # CRM inactivity rules
    "inactive_guest": {
        "follow_up_days": 14,
        "inactive_days": 30,
        "reactivation_days": 60,
    },

    # Reports
    "daily_report_hour": 8,

    "weekly_report_weekday": 0,
    # Monday = 0

    "monthly_report_day": 1,

    # Safety
    "require_marketing_permission": True,
}


# =========================================================
# AUTOMATION TASK FORMAT
# =========================================================

def create_task(
    task_type,
    guest_id=None,
    priority="NORMAL",
    title="",
    message="",
    automatic=False,
    due_at=None,
    metadata=None,
):

    return {
        "task_type": task_type,
        "guest_id": guest_id,
        "priority": priority,
        "title": title,
        "message": message,
        "automatic": automatic,
        "due_at": due_at,
        "metadata": metadata or {},
        "created_at": datetime.now(),
        "status": "PENDING",
    }


# =========================================================
# GUEST INACTIVITY TASKS
# =========================================================

def guest_inactivity_tasks(
    guest_id,
    tier,
    marketing_allowed=True,
    self_excluded=False,
    blocked=False,
    do_not_contact=False,
):

    tasks = []

    snapshot = build_host_snapshot(
        guest_id=guest_id,
        tier=tier,
        marketing_allowed=marketing_allowed,
        self_excluded=self_excluded,
        blocked=blocked,
        do_not_contact=do_not_contact,
    )

    inactivity = snapshot.get(
        "inactivity",
        {}
    )

    days = inactivity.get(
        "days_since_last_visit"
    )

    level = inactivity.get(
        "level"
    )

    can_contact = snapshot.get(
        "contact_allowed",
        False
    )

    # -----------------------------------------------------
    # CONTACT BLOCKED
    # -----------------------------------------------------

    if not can_contact:

        tasks.append(
            create_task(
                task_type="NO_CONTACT",
                guest_id=guest_id,
                priority="CRITICAL",
                title="Marketing contact blocked",
                message=(
                    "Do not send promotional or reactivation "
                    "communications to this guest."
                ),
                automatic=True,
            )
        )

        return tasks

    # -----------------------------------------------------
    # NO HISTORY
    # -----------------------------------------------------

    if days is None:

        tasks.append(
            create_task(
                task_type="HOST_REVIEW",
                guest_id=guest_id,
                priority="NORMAL",
                title="New or unknown guest",
                message=(
                    "No previous visit history found. "
                    "Host review recommended."
                ),
                automatic=False,
            )
        )

        return tasks

    # -----------------------------------------------------
    # 14 DAYS
    # -----------------------------------------------------

    if level == "FOLLOW_UP":

        tasks.append(
            create_task(
                task_type="HOST_FOLLOW_UP",
                guest_id=guest_id,
                priority="NORMAL",
                title="Guest follow-up",
                message=(
                    f"Guest has not visited for {days} days. "
                    "Prepare a personal host follow-up."
                ),
                automatic=False,
            )
        )

    # -----------------------------------------------------
    # 30 DAYS
    # -----------------------------------------------------

    elif level == "INACTIVE":

        tasks.append(
            create_task(
                task_type="INACTIVE_GUEST",
                guest_id=guest_id,
                priority="MEDIUM",
                title="Inactive guest review",
                message=(
                    f"Guest has not visited for {days} days. "
                    "Add guest to inactive guest review."
                ),
                automatic=False,
            )
        )

    # -----------------------------------------------------
    # 60 DAYS
    # -----------------------------------------------------

    elif level == "REACTIVATION":

        tasks.append(
            create_task(
                task_type="REACTIVATION",
                guest_id=guest_id,
                priority="HIGH",
                title="Reactivation review",
                message=(
                    f"Guest has not visited for {days} days. "
                    "Prepare reactivation contact if appropriate."
                ),
                automatic=False,
            )
        )

    return tasks


# =========================================================
# ALL GUEST AUTOMATION TASKS
# =========================================================

def build_all_guest_tasks(
    guests,
):

    """
    guests očekuje dictionary kao u guests.py

    {
        "G0001": {
            ...
        }
    }
    """

    tasks = []

    for guest_id, guest in guests.items():

        tier = guest.get(
            "tier",
            ""
        )

        marketing_allowed = guest.get(
            "marketing_allowed",
            True
        )

        self_excluded = guest.get(
            "self_excluded",
            False
        )

        blocked = guest.get(
            "blocked",
            False
        )

        do_not_contact = guest.get(
            "do_not_contact",
            False
        )

        guest_tasks = (
            guest_inactivity_tasks(
                guest_id=guest_id,
                tier=tier,
                marketing_allowed=marketing_allowed,
                self_excluded=self_excluded,
                blocked=blocked,
                do_not_contact=do_not_contact,
            )
        )

        tasks.extend(
            guest_tasks
        )

    return tasks


# =========================================================
# DATE RANGE HELPERS
# =========================================================

def start_of_day(value):

    return value.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )


def end_of_day(value):

    return value.replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999
    )


def visits_between(
    start,
    end,
):

    results = []

    for visit in VISITS:

        arrival = visit.get(
            "arrival"
        )

        if not arrival:
            continue

        if start <= arrival <= end:
            results.append(
                visit
            )

    return results


# =========================================================
# DAILY REPORT DATA
# =========================================================

def daily_report_data(
    report_date=None,
):

    if report_date is None:
        report_date = (
            datetime.now()
            - timedelta(days=1)
        )

    start = start_of_day(
        report_date
    )

    end = end_of_day(
        report_date
    )

    visits = visits_between(
        start,
        end
    )

    unique_guests = set()

    total_gaming_hours = 0.0
    total_win_loss = 0.0
    total_theoretical = 0.0
    total_turnover = 0.0

    total_hotel_cost = 0.0
    total_hotel_coverage = 0.0

    for visit in visits:

        guest_id = visit.get(
            "guest_id"
        )

        if guest_id:
            unique_guests.add(
                guest_id
            )

        hotel = visit.get(
            "hotel",
            {}
        )

        total_hotel_cost += float(
            hotel.get(
                "total_cost",
                0.0
            )
        )

        total_hotel_coverage += float(
            hotel.get(
                "casino_coverage",
                0.0
            )
        )

        for game in visit.get(
            "games",
            []
        ):

            total_gaming_hours += float(
                game.get(
                    "duration_hours",
                    0.0
                )
            )

            total_win_loss += float(
                game.get(
                    "casino_win_loss",
                    0.0
                )
            )

            total_theoretical += float(
                game.get(
                    "theoretical_value",
                    0.0
                )
            )

            total_turnover += float(
                game.get(
                    "turnover",
                    0.0
                )
            )

    return {
        "report_type": "DAILY",
        "date": report_date.date(),

        "visits": len(
            visits
        ),

        "unique_guests": len(
            unique_guests
        ),

        "gaming_hours":
            total_gaming_hours,

        "casino_win_loss":
            total_win_loss,

        "theoretical":
            total_theoretical,

        "turnover":
            total_turnover,

        "hotel_total_cost":
            total_hotel_cost,

        "hotel_coverage":
            total_hotel_coverage,
    }


# =========================================================
# WEEKLY REPORT DATA
# =========================================================

def weekly_report_data(
    now=None,
):

    if now is None:
        now = datetime.now()

    end = (
        start_of_day(
            now
        )
        - timedelta(
            microseconds=1
        )
    )

    start = (
        start_of_day(
            now
        )
        - timedelta(
            days=7
        )
    )

    visits = visits_between(
        start,
        end
    )

    return period_report_data(
        "WEEKLY",
        start,
        end,
        visits
    )


# =========================================================
# MONTHLY REPORT DATA
# =========================================================

def monthly_report_data(
    now=None,
):

    if now is None:
        now = datetime.now()

    first_this_month = (
        now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
    )

    end = (
        first_this_month
        - timedelta(
            microseconds=1
        )
    )

    start = (
        end.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
    )

    visits = visits_between(
        start,
        end
    )

    return period_report_data(
        "MONTHLY",
        start,
        end,
        visits
    )


# =========================================================
# GENERIC PERIOD REPORT
# =========================================================

def period_report_data(
    report_type,
    start,
    end,
    visits,
):

    unique_guests = set()

    total_gaming_hours = 0.0
    total_win_loss = 0.0
    total_theoretical = 0.0
    total_turnover = 0.0

    total_hotel_cost = 0.0
    total_hotel_coverage = 0.0

    for visit in visits:

        guest_id = visit.get(
            "guest_id"
        )

        if guest_id:
            unique_guests.add(
                guest_id
            )

        hotel = visit.get(
            "hotel",
            {}
        )

        total_hotel_cost += float(
            hotel.get(
                "total_cost",
                0.0
            )
        )

        total_hotel_coverage += float(
            hotel.get(
                "casino_coverage",
                0.0
            )
        )

        for game in visit.get(
            "games",
            []
        ):

            total_gaming_hours += float(
                game.get(
                    "duration_hours",
                    0.0
                )
            )

            total_win_loss += float(
                game.get(
                    "casino_win_loss",
                    0.0
                )
            )

            total_theoretical += float(
                game.get(
                    "theoretical_value",
                    0.0
                )
            )

            total_turnover += float(
                game.get(
                    "turnover",
                    0.0
                )
            )

    return {
        "report_type":
            report_type,

        "period_start":
            start,

        "period_end":
            end,

        "visits":
            len(
                visits
            ),

        "unique_guests":
            len(
                unique_guests
            ),

        "gaming_hours":
            total_gaming_hours,

        "casino_win_loss":
            total_win_loss,

        "theoretical":
            total_theoretical,

        "turnover":
            total_turnover,

        "hotel_total_cost":
            total_hotel_cost,

        "hotel_coverage":
            total_hotel_coverage,
    }


# =========================================================
# REPORT TEXT
# =========================================================

def report_to_text(
    report
):

    report_type = report.get(
        "report_type",
        "REPORT"
    )

    lines = [

        f"GCP {report_type} REPORT",

        "",

        (
            "Visits: "
            f"{report.get('visits', 0)}"
        ),

        (
            "Unique guests: "
            f"{report.get('unique_guests', 0)}"
        ),

        (
            "Gaming hours: "
            f"{report.get('gaming_hours', 0):.1f}"
        ),

        (
            "Turnover: €"
            f"{report.get('turnover', 0):,.2f}"
        ),

        (
            "Casino Win/Loss: €"
            f"{report.get('casino_win_loss', 0):,.2f}"
        ),

        (
            "Theoretical: €"
            f"{report.get('theoretical', 0):,.2f}"
        ),

        (
            "Hotel cost: €"
            f"{report.get('hotel_total_cost', 0):,.2f}"
        ),

        (
            "Hotel coverage: €"
            f"{report.get('hotel_coverage', 0):,.2f}"
        ),
    ]

    return "\n".join(
        lines
    )


# =========================================================
# WHICH AUTOMATIONS SHOULD RUN?
# =========================================================

def scheduled_jobs_due(
    now=None,
):

    if now is None:
        now = datetime.now()

    jobs = []

    # -----------------------------------------------------
    # DAILY
    # -----------------------------------------------------

    if now.hour == AUTOMATION_CONFIG[
        "daily_report_hour"
    ]:

        jobs.append(
            "DAILY_REPORT"
        )

    # -----------------------------------------------------
    # WEEKLY
    # -----------------------------------------------------

    if (
        now.weekday()
        == AUTOMATION_CONFIG[
            "weekly_report_weekday"
        ]
        and
        now.hour
        == AUTOMATION_CONFIG[
            "daily_report_hour"
        ]
    ):

        jobs.append(
            "WEEKLY_REPORT"
        )

    # -----------------------------------------------------
    # MONTHLY
    # -----------------------------------------------------

    if (
        now.day
        == AUTOMATION_CONFIG[
            "monthly_report_day"
        ]
        and
        now.hour
        == AUTOMATION_CONFIG[
            "daily_report_hour"
        ]
    ):

        jobs.append(
            "MONTHLY_REPORT"
        )

    return jobs


# =========================================================
# COMPLETE AUTOMATION RUN
# =========================================================

def run_automation_cycle(
    guests,
    now=None,
):

    if now is None:
        now = datetime.now()

    result = {
        "timestamp": now,
        "jobs_due": [],
        "guest_tasks": [],
        "reports": [],
    }

    # -----------------------------------------------------
    # GUEST TASKS
    # -----------------------------------------------------

    result[
        "guest_tasks"
    ] = build_all_guest_tasks(
        guests
    )

    # -----------------------------------------------------
    # REPORT JOBS
    # -----------------------------------------------------

    jobs = scheduled_jobs_due(
        now
    )

    result[
        "jobs_due"
    ] = jobs

    if "DAILY_REPORT" in jobs:

        daily = daily_report_data(
            now
            - timedelta(days=1)
        )

        result[
            "reports"
        ].append(
            daily
        )

    if "WEEKLY_REPORT" in jobs:

        weekly = weekly_report_data(
            now
        )

        result[
            "reports"
        ].append(
            weekly
        )

    if "MONTHLY_REPORT" in jobs:

        monthly = monthly_report_data(
            now
        )

        result[
            "reports"
        ].append(
            monthly
        )

    return result