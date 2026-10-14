# reports.py

from datetime import datetime

from activity import (
    VISITS,
    guest_statistics,
    guest_primary_game,
    average_days_between_visits,
)

from automation_engine import (
    daily_report_data,
    weekly_report_data,
    monthly_report_data,
    build_all_guest_tasks,
)

from offers_engine import (
    build_host_snapshot,
)


# =========================================================
# HELPERS
# =========================================================

def money(value):
    return f"€{float(value or 0):,.2f}"


def number(value):
    return f"{float(value or 0):,.1f}"


def safe_date(value):

    if not value:
        return "-"

    if isinstance(value, datetime):
        return value.strftime(
            "%d.%m.%Y"
        )

    return str(value)


# =========================================================
# GUEST REPORT
# =========================================================

def guest_report(
    guest_id,
    guest,
):

    stats = guest_statistics(
        guest_id
    )

    primary_game = guest_primary_game(
        guest_id
    )

    frequency = average_days_between_visits(
        guest_id
    )

    tier = guest.get(
        "tier",
        "-"
    )

    name = (
        guest.get("first_name", "")
        + " "
        + guest.get("last_name", "")
    ).strip()

    if not name:
        name = guest.get(
            "name",
            guest_id
        )

    report = {
        "guest_id": guest_id,
        "name": name,
        "tier": tier,

        "country": guest.get(
            "country",
            guest.get(
                "nationality",
                "-"
            )
        ),

        "email": guest.get(
            "email",
            "-"
        ),

        "phone": guest.get(
            "phone",
            guest.get(
                "mobile",
                "-"
            )
        ),

        "visits": stats.get(
            "visits",
            0
        ),

        "game_sessions": stats.get(
            "game_sessions",
            0
        ),

        "last_visit": stats.get(
            "last_visit"
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

        "primary_game":
            primary_game or "-",

        "average_bet":
            stats.get(
                "average_bet",
                0.0
            ),

        "turnover":
            stats.get(
                "turnover",
                0.0
            ),

        "casino_win_loss":
            stats.get(
                "casino_win_loss",
                0.0
            ),

        "theoretical":
            stats.get(
                "theoretical_value",
                0.0
            ),

        "hotel_total_cost":
            stats.get(
                "hotel_total_cost",
                0.0
            ),

        "hotel_coverage":
            stats.get(
                "casino_hotel_coverage",
                0.0
            ),

        "hotel_reimbursements":
            stats.get(
                "hotel_reimbursements",
                0.0
            ),

        "average_days_between_visits":
            frequency,
    }

    return report


# =========================================================
# GUEST REPORT TEXT
# =========================================================

def guest_report_text(
    report
):

    frequency = report.get(
        "average_days_between_visits"
    )

    frequency_text = (
        f"{frequency:.1f} dana"
        if frequency is not None
        else "-"
    )

    lines = [

        "GRAND CASINO PORTOROŽ",
        "CASINO HOST AI — GUEST REPORT",
        "",

        f"Guest: {report.get('name')}",
        f"Guest ID: {report.get('guest_id')}",
        f"Tier: {report.get('tier')}",
        f"Country: {report.get('country')}",

        "",

        f"Visits: {report.get('visits', 0)}",
        f"Last visit: {safe_date(report.get('last_visit'))}",

        (
            "Average visit frequency: "
            f"{frequency_text}"
        ),

        (
            "Gaming sessions: "
            f"{report.get('game_sessions', 0)}"
        ),

        (
            "Total gaming hours: "
            f"{number(report.get('total_gaming_hours'))}"
        ),

        (
            "Average game duration: "
            f"{number(report.get('average_game_duration'))} h"
        ),

        (
            "Primary game: "
            f"{report.get('primary_game')}"
        ),

        (
            "Average bet: "
            f"{money(report.get('average_bet'))}"
        ),

        (
            "Turnover: "
            f"{money(report.get('turnover'))}"
        ),

        (
            "Casino Win/Loss: "
            f"{money(report.get('casino_win_loss'))}"
        ),

        (
            "Theoretical: "
            f"{money(report.get('theoretical'))}"
        ),

        "",

        (
            "Hotel total cost: "
            f"{money(report.get('hotel_total_cost'))}"
        ),

        (
            "Casino hotel coverage: "
            f"{money(report.get('hotel_coverage'))}"
        ),

        (
            "Hotel reimbursements: "
            f"{money(report.get('hotel_reimbursements'))}"
        ),
    ]

    return "\n".join(
        lines
    )


# =========================================================
# MANAGEMENT REPORT
# =========================================================

def management_report(
    report_type="DAILY"
):

    report_type = report_type.upper()

    if report_type == "DAILY":

        data = daily_report_data()

    elif report_type == "WEEKLY":

        data = weekly_report_data()

    elif report_type == "MONTHLY":

        data = monthly_report_data()

    else:

        raise ValueError(
            "Unknown report type."
        )

    return data


# =========================================================
# MANAGEMENT REPORT TEXT
# =========================================================

def management_report_text(
    report
):

    title = (
        f"GCP {report.get('report_type', 'REPORT')} REPORT"
    )

    lines = [
        title,
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
            f"{number(report.get('gaming_hours'))}"
        ),

        (
            "Turnover: "
            f"{money(report.get('turnover'))}"
        ),

        (
            "Casino Win/Loss: "
            f"{money(report.get('casino_win_loss'))}"
        ),

        (
            "Theoretical: "
            f"{money(report.get('theoretical'))}"
        ),

        (
            "Hotel cost: "
            f"{money(report.get('hotel_total_cost'))}"
        ),

        (
            "Hotel coverage: "
            f"{money(report.get('hotel_coverage'))}"
        ),
    ]

    return "\n".join(
        lines
    )


# =========================================================
# HOST TASK REPORT
# =========================================================

def host_task_report(
    guests
):

    tasks = build_all_guest_tasks(
        guests
    )

    grouped = {
        "CRITICAL": [],
        "HIGH": [],
        "MEDIUM": [],
        "NORMAL": [],
        "LOW": [],
    }

    for task in tasks:

        priority = task.get(
            "priority",
            "NORMAL"
        )

        if priority not in grouped:
            grouped[priority] = []

        grouped[priority].append(
            task
        )

    return grouped


# =========================================================
# HOST TASK REPORT TEXT
# =========================================================

def host_task_report_text(
    grouped_tasks
):

    lines = [
        "GCP CASINO HOST TASK REPORT",
        ""
    ]

    order = [
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "NORMAL",
        "LOW",
    ]

    for priority in order:

        tasks = grouped_tasks.get(
            priority,
            []
        )

        if not tasks:
            continue

        lines.append(
            f"{priority} PRIORITY"
        )

        for task in tasks:

            guest_id = task.get(
                "guest_id",
                "-"
            )

            title = task.get(
                "title",
                ""
            )

            message = task.get(
                "message",
                ""
            )

            lines.append(
                f"- {guest_id}: {title}"
            )

            if message:
                lines.append(
                    f"  {message}"
                )

        lines.append("")

    return "\n".join(
        lines
    )


# =========================================================
# GUEST SNAPSHOT REPORT
# =========================================================

def guest_snapshot_report(
    guest_id,
    tier,
    marketing_allowed=True,
    self_excluded=False,
    blocked=False,
    do_not_contact=False,
):

    snapshot = build_host_snapshot(
        guest_id=guest_id,
        tier=tier,
        marketing_allowed=marketing_allowed,
        self_excluded=self_excluded,
        blocked=blocked,
        do_not_contact=do_not_contact,
    )

    return snapshot


# =========================================================
# DAILY HOST SUMMARY
# =========================================================

def daily_host_summary(
    guests
):

    management = management_report(
        "DAILY"
    )

    tasks = host_task_report(
        guests
    )

    return {
        "management": management,
        "tasks": tasks,
    }


# =========================================================
# WEEKLY HOST SUMMARY
# =========================================================

def weekly_host_summary(
    guests
):

    management = management_report(
        "WEEKLY"
    )

    tasks = host_task_report(
        guests
    )

    return {
        "management": management,
        "tasks": tasks,
    }


# =========================================================
# MONTHLY HOST SUMMARY
# =========================================================

def monthly_host_summary(
    guests
):

    management = management_report(
        "MONTHLY"
    )

    tasks = host_task_report(
        guests
    )

    return {
        "management": management,
        "tasks": tasks,
    }


# =========================================================
# COMPLETE EMAIL BODY
# =========================================================

def build_report_email_body(
    report_type,
    guests
):

    report_type = report_type.upper()

    if report_type == "DAILY":

        summary = daily_host_summary(
            guests
        )

    elif report_type == "WEEKLY":

        summary = weekly_host_summary(
            guests
        )

    elif report_type == "MONTHLY":

        summary = monthly_host_summary(
            guests
        )

    else:

        raise ValueError(
            "Invalid report type."
        )

    management_text = (
        management_report_text(
            summary["management"]
        )
    )

    task_text = (
        host_task_report_text(
            summary["tasks"]
        )
    )

    body = (
        management_text
        + "\n\n"
        + "------------------------------"
        + "\n\n"
        + task_text
    )

    return body