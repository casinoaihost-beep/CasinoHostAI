# notifications.py

import smtplib
import streamlit as st

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# =========================================================
# READ STREAMLIT SECRETS
# =========================================================

def get_email_config():

    return {
        "smtp_server": st.secrets["email"]["smtp_server"],
        "smtp_port": int(st.secrets["email"]["smtp_port"]),
        "sender_email": st.secrets["email"]["sender_email"],
        "username": st.secrets["email"]["username"],
        "password": st.secrets["email"]["password"],
        "sender_name": "Grand Casino Portorož - Casino Host AI",
    }


def get_recipient_groups():

    return {
        "daily": list(
            st.secrets["recipients"]["daily"]
        ),

        "weekly": list(
            st.secrets["recipients"]["weekly"]
        ),

        "monthly": list(
            st.secrets["recipients"]["monthly"]
        ),

        "host_alerts": list(
            st.secrets["recipients"]["host_alerts"]
        ),

        "management": list(
            st.secrets["recipients"]["management"]
        ),
    }


# =========================================================
# HELPERS
# =========================================================

def clean_email_list(values):

    if values is None:
        return []

    if isinstance(values, str):
        values = [values]

    result = []

    for value in values:

        email = str(
            value or ""
        ).strip()

        if not email:
            continue

        if email not in result:
            result.append(email)

    return result


# =========================================================
# BUILD EMAIL
# =========================================================

def build_email_message(
    subject,
    body,
    recipients,
    cc=None,
):

    config = get_email_config()

    recipients = clean_email_list(
        recipients
    )

    cc = clean_email_list(
        cc
    )

    message = MIMEMultipart()

    message["From"] = (
        f'{config["sender_name"]} '
        f'<{config["sender_email"]}>'
    )

    message["To"] = ", ".join(
        recipients
    )

    if cc:
        message["Cc"] = ", ".join(cc)

    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "plain",
            "utf-8"
        )
    )

    all_recipients = (
        recipients + cc
    )

    return (
        message,
        all_recipients
    )


# =========================================================
# SEND EMAIL
# =========================================================

def send_email(
    subject,
    body,
    recipients,
    cc=None,
):

    config = get_email_config()

    recipients = clean_email_list(
        recipients
    )

    if not recipients:

        return {
            "success": False,
            "error": "No recipients provided.",
        }

    try:

        (
            message,
            all_recipients
        ) = build_email_message(
            subject=subject,
            body=body,
            recipients=recipients,
            cc=cc,
        )

        server = smtplib.SMTP(
            config["smtp_server"],
            config["smtp_port"],
            timeout=30,
        )

        server.starttls()

        server.login(
            config["username"],
            config["password"],
        )

        server.sendmail(
            config["sender_email"],
            all_recipients,
            message.as_string(),
        )

        server.quit()

        return {
            "success": True,
            "recipients": all_recipients,
            "subject": subject,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# =========================================================
# REPORT SUBJECTS
# =========================================================

def report_subject(
    report_type,
):

    report_type = str(
        report_type or ""
    ).upper()

    subjects = {

        "DAILY":
            "GCP Casino Host AI - Daily Report",

        "WEEKLY":
            "GCP Casino Host AI - Weekly Report",

        "MONTHLY":
            "GCP Casino Host AI - Monthly Report",

        "HOST_ALERT":
            "GCP Casino Host AI - Host Alert",

        "TEST":
            "GCP Casino Host AI - Test Email",
    }

    return subjects.get(
        report_type,
        "GCP Casino Host AI Report"
    )


# =========================================================
# SEND REPORT
# =========================================================

def send_report_email(
    report_type,
    body,
    recipients=None,
    cc=None,
):

    groups = get_recipient_groups()

    report_type = str(
        report_type or ""
    ).upper()

    if recipients is None:

        if report_type == "DAILY":
            recipients = groups["daily"]

        elif report_type == "WEEKLY":
            recipients = groups["weekly"]

        elif report_type == "MONTHLY":
            recipients = groups["monthly"]

        else:
            recipients = groups["management"]

    return send_email(
        subject=report_subject(
            report_type
        ),
        body=body,
        recipients=recipients,
        cc=cc,
    )


# =========================================================
# HOST ALERT
# =========================================================

def send_host_alert(
    title,
    message,
    recipients=None,
):

    groups = get_recipient_groups()

    if recipients is None:
        recipients = groups["host_alerts"]

    body = (
        "GRAND CASINO PORTOROŽ\n"
        "CASINO HOST AI\n\n"
        f"{title}\n\n"
        f"{message}"
    )

    return send_email(
        subject=report_subject(
            "HOST_ALERT"
        ),
        body=body,
        recipients=recipients,
    )


# =========================================================
# TEST EMAIL
# =========================================================

def send_test_email(
    recipient=None,
):

    groups = get_recipient_groups()

    if recipient is None:

        if groups["management"]:
            recipient = groups["management"][0]

        else:
            return {
                "success": False,
                "error": "No test recipient configured.",
            }

    body = (
        "Grand Casino Portorož\n"
        "Casino Host AI\n\n"
        "Test email successful.\n\n"
        "The email notification system is connected "
        "to Streamlit Secrets and Gmail SMTP."
    )

    return send_email(
        subject=report_subject(
            "TEST"
        ),
        body=body,
        recipients=[recipient],
    )