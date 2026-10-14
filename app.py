import os
from datetime import datetime

import streamlit as st

from search import (
    search_guests,
    get_guest_value,
    guest_full_name,
)

from rules import (
    normalize_tier,
    get_hotel_policy,
    calculate_hotel_coverage,
    build_new_guest_review_ticket,
    format_new_guest_ticket,
    restaurant_eligibility,
    whatsapp_url,
    mailto_url,
    tel_url,
)

from activity import (
    guest_statistics,
    guest_primary_game,
    guest_game_type_statistics,
    guest_visits,
    average_days_between_visits,
)

from offers_engine import (
    build_host_snapshot,
    inactivity_status,
)

from reports import (
    guest_report,
    guest_report_text,
    management_report,
    management_report_text,
)

from notifications import (
    send_test_email,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Grand Casino Portorož — Casino Host AI Demo",
    page_icon="♠️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# LANGUAGES
# =========================================================

LANGUAGES = {
    "SI": "🇸🇮 Slovenščina",
    "IT": "🇮🇹 Italiano",
    "DE": "🇩🇪 Deutsch",
    "HR": "🇭🇷 Hrvatski",
    "EN": "🇬🇧 English",
    "RU": "🇷🇺 Русский",
    "HU": "🇭🇺 Magyar",
    "PL": "🇵🇱 Polski",
}


TEXT = {

    "HR": {
        "guest_crm": "Guest CRM",
        "system_demo": "System Demo",
        "admin": "Admin",

        "search": "VIP pretraga gosta",
        "find": "PRONAĐI GOSTA",
        "placeholder": "Ime gosta, Guest ID, email ili telefon...",
        "not_found": "Gost nije pronađen.",
        "multiple": "Pronađeno je više gostiju. Odaberi pravog gosta.",
        "choose": "ODABERI",

        "profile": "VIP profil gosta",
        "overview": "Pregled",
        "gaming": "Gaming",
        "hotel": "Hotel",
        "dining": "Restoran",
        "automation": "CRM & automatizacija",
        "reports": "Izvještaji",
        "contact": "Kontakt",

        "country": "Država",
        "email": "Email",
        "phone": "Telefon",
        "tier": "VIP kategorija",
        "language": "Jezik",

        "visits": "Posjete",
        "last_visit": "Zadnja posjeta",
        "gaming_hours": "Sati igre",
        "primary_game": "Glavna igra",
        "average_bet": "Prosječan bet",
        "turnover": "Turnover",
        "winloss": "Casino Win/Loss",
        "theoretical": "Theoretical",
        "frequency": "Prosječna učestalost dolazaka",

        "days_inactive": "Dana bez posjete",
        "crm_status": "CRM status",
        "contact_allowed": "Marketing kontakt dopušten",

        "hotel_title": "Hotel & smještaj",
        "external_hotel": "Grand Casino Portorož surađuje s vanjskim hotelima.",
        "nights": "Broj noćenja",
        "night_price": "Cijena sobe po noćenju (€)",
        "calculate": "IZRAČUNAJ POKRIĆE",
        "room_total": "Ukupni trošak sobe",
        "casino_cover": "GCP pokriva",
        "guest_difference": "Doplata gosta",
        "extras": "Parking, minibar i ostali dodatni troškovi nisu uključeni.",

        "hotel_paid": "Trošak hotela koji je gost platio (€)",
        "loss": "Gaming loss (€)",
        "hours": "Trajanje igre (sati)",
        "game_type": "Vrsta igre",
        "notes": "Napomena hosta",
        "ticket": "KREIRAJ REVIEW TICKET",

        "restaurant": "Restaurant & Dining",
        "date": "Datum",
        "party": "Broj osoba",
        "meal": "Usluga",
        "lunch": "Ručak",
        "dinner": "Večera",
        "eligible": "Gost ima pravo na ovu uslugu.",
        "not_eligible": "Gost prema trenutnim pravilima nema automatsko pravo.",
        "closed": "Restoran taj dan ne radi za odabranu uslugu.",
        "last_arrival": "Zadnji prijem gosta",

        "whatsapp": "WhatsApp",
        "email_guest": "Email gostu",
        "call": "Pozovi gosta",

        "another": "ODABERI DRUGOG GOSTA",

        "admin_pin": "Admin PIN",
        "wrong_pin": "Pogrešan PIN.",
        "admin_ok": "Admin pristup odobren.",
        "send_test": "POŠALJI TEST EMAIL",
        "email_ok": "Testni email je uspješno poslan.",

        "daily": "Dnevni izvještaj",
        "weekly": "Tjedni izvještaj",
        "monthly": "Mjesečni izvještaj",
    },

    "SI": {
        "guest_crm": "Guest CRM",
        "system_demo": "System Demo",
        "admin": "Admin",

        "search": "VIP iskanje gosta",
        "find": "POIŠČI GOSTA",
        "placeholder": "Ime gosta, Guest ID, e-pošta ali telefon...",
        "not_found": "Gost ni bil najden.",
        "multiple": "Najdenih je več gostov. Izberi pravega gosta.",
        "choose": "IZBERI",

        "profile": "VIP profil gosta",
        "overview": "Pregled",
        "gaming": "Gaming",
        "hotel": "Hotel",
        "dining": "Restavracija",
        "automation": "CRM & avtomatizacija",
        "reports": "Poročila",
        "contact": "Kontakt",

        "country": "Država",
        "email": "E-pošta",
        "phone": "Telefon",
        "tier": "VIP kategorija",
        "language": "Jezik",

        "visits": "Obiski",
        "last_visit": "Zadnji obisk",
        "gaming_hours": "Ure igre",
        "primary_game": "Glavna igra",
        "average_bet": "Povprečna stava",
        "turnover": "Turnover",
        "winloss": "Casino Win/Loss",
        "theoretical": "Theoretical",
        "frequency": "Povprečna pogostost obiskov",

        "days_inactive": "Dni brez obiska",
        "crm_status": "CRM status",
        "contact_allowed": "Marketing kontakt dovoljen",

        "hotel_title": "Hotel & nastanitev",
        "external_hotel": "Grand Casino Portorož sodeluje z zunanjimi hoteli.",
        "nights": "Število nočitev",
        "night_price": "Cena sobe na noč (€)",
        "calculate": "IZRAČUNAJ KRITJE",
        "room_total": "Skupni strošek sobe",
        "casino_cover": "GCP krije",
        "guest_difference": "Doplačilo gosta",
        "extras": "Parkiranje, minibar in drugi dodatni stroški niso vključeni.",

        "hotel_paid": "Strošek hotela, ki ga je plačal gost (€)",
        "loss": "Gaming loss (€)",
        "hours": "Trajanje igre (ure)",
        "game_type": "Vrsta igre",
        "notes": "Opomba hosta",
        "ticket": "USTVARI REVIEW TICKET",

        "restaurant": "Restavracija & Dining",
        "date": "Datum",
        "party": "Število oseb",
        "meal": "Storitev",
        "lunch": "Kosilo",
        "dinner": "Večerja",
        "eligible": "Gost je upravičen do te storitve.",
        "not_eligible": "Gost po trenutnih pravilih nima samodejne pravice.",
        "closed": "Restavracija na izbrani dan ne obratuje.",
        "last_arrival": "Zadnji sprejem gosta",

        "whatsapp": "WhatsApp",
        "email_guest": "E-pošta gostu",
        "call": "Pokliči gosta",

        "another": "IZBERI DRUGEGA GOSTA",

        "admin_pin": "Admin PIN",
        "wrong_pin": "Napačen PIN.",
        "admin_ok": "Admin dostop odobren.",
        "send_test": "POŠLJI TESTNI EMAIL",
        "email_ok": "Testni email je bil poslan.",

        "daily": "Dnevno poročilo",
        "weekly": "Tedensko poročilo",
        "monthly": "Mesečno poročilo",
    },

    "EN": {
        "guest_crm": "Guest CRM",
        "system_demo": "System Demo",
        "admin": "Admin",

        "search": "VIP Guest Search",
        "find": "FIND GUEST",
        "placeholder": "Guest name, Guest ID, email or phone...",
        "not_found": "Guest not found.",
        "multiple": "Multiple guests found. Select the correct guest.",
        "choose": "SELECT",

        "profile": "VIP Guest Profile",
        "overview": "Overview",
        "gaming": "Gaming",
        "hotel": "Hotel",
        "dining": "Dining",
        "automation": "CRM & Automation",
        "reports": "Reports",
        "contact": "Contact",

        "country": "Country",
        "email": "Email",
        "phone": "Telephone",
        "tier": "VIP Tier",
        "language": "Language",

        "visits": "Visits",
        "last_visit": "Last visit",
        "gaming_hours": "Gaming hours",
        "primary_game": "Primary game",
        "average_bet": "Average bet",
        "turnover": "Turnover",
        "winloss": "Casino Win/Loss",
        "theoretical": "Theoretical",
        "frequency": "Average visit frequency",

        "days_inactive": "Days inactive",
        "crm_status": "CRM status",
        "contact_allowed": "Marketing contact allowed",

        "hotel_title": "Hotel & Accommodation",
        "external_hotel": "Grand Casino Portorož cooperates with external hotels.",
        "nights": "Number of nights",
        "night_price": "Room price per night (€)",
        "calculate": "CALCULATE COVERAGE",
        "room_total": "Total room cost",
        "casino_cover": "GCP coverage",
        "guest_difference": "Guest contribution",
        "extras": "Parking, minibar and other extras are not included.",

        "hotel_paid": "Hotel cost paid by guest (€)",
        "loss": "Gaming loss (€)",
        "hours": "Play duration (hours)",
        "game_type": "Game type",
        "notes": "Host notes",
        "ticket": "CREATE REVIEW TICKET",

        "restaurant": "Restaurant & Dining",
        "date": "Date",
        "party": "Number of guests",
        "meal": "Service",
        "lunch": "Lunch",
        "dinner": "Dinner",
        "eligible": "The guest is eligible for this service.",
        "not_eligible": "The guest is not automatically eligible.",
        "closed": "The restaurant is closed for this service.",
        "last_arrival": "Last guest arrival",

        "whatsapp": "WhatsApp",
        "email_guest": "Email Guest",
        "call": "Call Guest",

        "another": "SELECT ANOTHER GUEST",

        "admin_pin": "Admin PIN",
        "wrong_pin": "Incorrect PIN.",
        "admin_ok": "Admin access granted.",
        "send_test": "SEND TEST EMAIL",
        "email_ok": "Test email successfully sent.",

        "daily": "Daily Report",
        "weekly": "Weekly Report",
        "monthly": "Monthly Report",
    },
}


# Za IT/DE/RU/HU/PL trenutno koristimo EN tekst za nove
# dashboard elemente. Jezični izbor i guest language ostaju aktivni.

for code in ["IT", "DE", "RU", "HU", "PL"]:
    TEXT[code] = dict(
        TEXT["EN"]
    )


if "language" not in st.session_state:
    st.session_state.language = "SI"


language = st.selectbox(
    "Language / Jezik / Lingua / Sprache",
    list(LANGUAGES.keys()),
    index=list(
        LANGUAGES.keys()
    ).index(
        st.session_state.language
    ),
    format_func=lambda x:
        LANGUAGES[x],
)

st.session_state.language = language

T = TEXT[language]


# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at top,
            #281f08 0%,
            #111111 32%,
            #050505 78%
        );

    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.hero {

    background:
        linear-gradient(
            135deg,
            #090909,
            #2d2308,
            #080808
        );

    border:
        1px solid #a78928;

    border-radius:
        22px;

    padding:
        28px 20px;

    text-align:
        center;

    margin-bottom:
        22px;

    box-shadow:
        0 0 30px rgba(212,175,55,.12);
}

.hero-title {

    color:
        #e4c45c;

    font-size:
        40px;

    font-weight:
        700;
}

.gold-title {

    color:
        #e4c45c;

    font-size:
        24px;

    font-weight:
        700;

    margin-top:
        22px;

    margin-bottom:
        12px;
}

.card {

    background:
        linear-gradient(
            145deg,
            #1a1a1a,
            #0c0c0c
        );

    border:
        1px solid #4d4020;

    border-radius:
        16px;

    padding:
        18px;

    margin-bottom:
        12px;
}

.guest-card {

    background:
        linear-gradient(
            135deg,
            #1b1b1b,
            #0b0b0b
        );

    border:
        1px solid #806b29;

    border-radius:
        18px;

    padding:
        20px;
}

.guest-name {

    font-size:
        29px;

    font-weight:
        700;
}

.gold {

    color:
        #e4c45c;
}

.green {

    color:
        #75db87;
}

.red {

    color:
        #ff7777;
}

.muted {

    color:
        #999999;
}

div.stButton > button {

    background:
        linear-gradient(
            100deg,
            #171717,
            #2c240d
        ) !important;

    color:
        #ead173 !important;

    border:
        1px solid #806b29 !important;

    border-radius:
        12px !important;

    min-height:
        46px;

    font-weight:
        600;
}

div[data-testid="stLinkButton"] a {

    background:
        linear-gradient(
            100deg,
            #171717,
            #2c240d
        ) !important;

    color:
        #ead173 !important;

    border:
        1px solid #806b29 !important;

    border-radius:
        12px !important;
}


@media(max-width:700px) {

    .hero-title {
        font-size: 27px;
    }

    .block-container {
        padding-left: .7rem;
        padding-right: .7rem;
    }

    .guest-name {
        font-size: 23px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# IMAGE
# =========================================================

if os.path.exists(
    "casino_demo_poster.png"
):

    st.image(
        "casino_demo_poster.png",
        use_container_width=True
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">

<div style="
color:#d9bd69;
letter-spacing:5px;
font-size:12px;
font-weight:700;
">
CASINO HOST AI
</div>

<div class="hero-title">
GRAND CASINO PORTOROŽ
</div>

<div style="
font-size:18px;
">
Intelligent VIP Guest Experience
</div>

<br>

<div style="
display:inline-block;
border:1px solid #a78928;
border-radius:25px;
padding:6px 15px;
color:#e4c45c;
font-size:11px;
letter-spacing:2px;
">
DEMO CONCEPT
</div>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# STATE
# =========================================================

if "selected_guest" not in st.session_state:

    st.session_state.selected_guest = None


if "selected_guest_id" not in st.session_state:

    st.session_state.selected_guest_id = None


# =========================================================
# MAIN MENU
# =========================================================

main_mode = st.radio(
    "",
    [
        T["guest_crm"],
        T["system_demo"],
        T["admin"],
    ],
    horizontal=True,
)


# =========================================================
# SYSTEM DEMO
# =========================================================

if main_mode == T["system_demo"]:

    st.markdown(
        """
<div class="gold-title">
🚀 Casino Host AI — System Capabilities
</div>
""",
        unsafe_allow_html=True
    )


    capabilities = [

        (
            "Guest Database",
            "ACTIVE",
            "80 demo guests across Chairman, VIP, Gold, Silver and New tiers."
        ),

        (
            "Smart Guest Search",
            "ACTIVE",
            "Name, Guest ID, email, phone, upper/lower case and duplicate names."
        ),

        (
            "Multilingual Platform",
            "ACTIVE",
            "SI, IT, DE, HR, EN, RU, HU and PL language architecture."
        ),

        (
            "Gaming History",
            "ACTIVE",
            "Visits, gaming sessions, game types, playing time and host activity."
        ),

        (
            "Gaming Analytics",
            "ACTIVE",
            "Average bet, turnover, casino Win/Loss, theoretical and preferred game."
        ),

        (
            "Hotel Rules Engine",
            "ACTIVE",
            "Gold, VIP, Silver, Chairman and New Guest hotel logic."
        ),

        (
            "Restaurant Rules",
            "ACTIVE",
            "Tier eligibility, lunch/dinner schedules and last guest arrival."
        ),

        (
            "CRM Automation",
            "ACTIVE",
            "14 / 30 / 60 day inactivity monitoring and host follow-up logic."
        ),

        (
            "Responsible Contact Controls",
            "ACTIVE",
            "Marketing permission, self-exclusion, blocked and do-not-contact checks."
        ),

        (
            "Daily Reports",
            "ACTIVE",
            "Guest activity, gaming metrics, hotel cost and casino coverage."
        ),

        (
            "Weekly Reports",
            "ACTIVE",
            "Aggregated operational reporting."
        ),

        (
            "Monthly Reports",
            "ACTIVE",
            "Monthly management overview."
        ),

        (
            "Email Engine",
            "ACTIVE",
            "Secure Gmail SMTP through Streamlit Secrets."
        ),

        (
            "Scheduled Email Automation",
            "IN DEVELOPMENT",
            "Automatic timed execution of daily, weekly and monthly reports."
        ),

        (
            "AI Recommendation Engine",
            "IN DEVELOPMENT",
            "Guest snapshots and rule-based host recommendations."
        ),

        (
            "Production Database",
            "NEXT",
            "Persistent cloud database replacing demo Python data."
        ),

        (
            "WhatsApp Business API",
            "NEXT",
            "Approved automated communication workflows."
        ),

        (
            "Role-Based Login",
            "NEXT",
            "Host, management and administrator access levels."
        ),
    ]


    for (
        title,
        status,
        description
    ) in capabilities:

        if status == "ACTIVE":

            status_color = "#75db87"

        elif status == "IN DEVELOPMENT":

            status_color = "#e4c45c"

        else:

            status_color = "#999999"


        st.markdown(
            f"""
<div class="card">

<div style="
font-size:19px;
font-weight:700;
color:#e4c45c;
">
{title}
</div>

<div style="
font-size:12px;
font-weight:700;
color:{status_color};
margin-top:5px;
">
{status}
</div>

<br>

{description}

</div>
""",
            unsafe_allow_html=True
        )


    st.stop()


# =========================================================
# ADMIN
# =========================================================

if main_mode == T["admin"]:

    st.markdown(
        """
<div class="gold-title">
🔐 Casino Host AI Admin
</div>
""",
        unsafe_allow_html=True
    )


    try:

        correct_pin = str(
            st.secrets[
                "admin"
            ][
                "pin"
            ]
        )

    except Exception:

        st.error(
            "Admin PIN nije pronađen u Streamlit Secrets."
        )

        st.code(
            '[admin]\npin = "1234"'
        )

        st.stop()


    pin = st.text_input(
        T["admin_pin"],
        type="password",
    )


    if not pin:

        st.stop()


    if pin != correct_pin:

        st.error(
            T["wrong_pin"]
        )

        st.stop()


    st.success(
        T["admin_ok"]
    )


    admin_function = st.selectbox(
        "Admin function",
        [
            "Email Test",
            T["daily"],
            T["weekly"],
            T["monthly"],
        ]
    )


    # -----------------------------------------------------
    # EMAIL TEST
    # -----------------------------------------------------

    if admin_function == "Email Test":

        st.info(
            "Test Gmail SMTP + Streamlit Secrets connection."
        )

        if st.button(
            T["send_test"],
            use_container_width=True
        ):

            with st.spinner(
                "Sending..."
            ):

                result = (
                    send_test_email()
                )


            if result.get(
                "success"
            ):

                st.success(
                    T["email_ok"]
                )

            else:

                st.error(
                    result.get(
                        "error",
                        "Unknown email error."
                    )
                )


    # -----------------------------------------------------
    # REPORT PREVIEW
    # -----------------------------------------------------

    else:

        if admin_function == T["daily"]:

            report_type = "DAILY"

        elif admin_function == T["weekly"]:

            report_type = "WEEKLY"

        else:

            report_type = "MONTHLY"


        report = management_report(
            report_type
        )


        report_text = management_report_text(
            report
        )


        st.code(
            report_text
        )


    st.stop()


# =========================================================
# GUEST SEARCH
# =========================================================

st.markdown(
    f"""
<div class="gold-title">
🔎 {T["search"]}
</div>
""",
    unsafe_allow_html=True
)


query = st.text_input(
    "guest_search",
    label_visibility="collapsed",
    placeholder=T[
        "placeholder"
    ],
)


if st.button(
    f'🔎 {T["find"]}',
    use_container_width=True
):

    if not query.strip():

        st.warning(
            T[
                "placeholder"
            ]
        )

    else:

        results = search_guests(
            query
        )


        if not results:

            st.error(
                T[
                    "not_found"
                ]
            )


        elif len(
            results
        ) == 1:

            (
                guest_id,
                guest
            ) = results[0]


            st.session_state.selected_guest = (
                guest
            )

            st.session_state.selected_guest_id = (
                guest_id
            )

            st.rerun()


        else:

            st.warning(
                T[
                    "multiple"
                ]
            )


            for (
                guest_id,
                guest
            ) in results:

                name = guest_full_name(
                    guest
                )

                tier = get_guest_value(
                    guest,
                    "tier",
                    default="-"
                )

                country = get_guest_value(
                    guest,
                    "country",
                    "nationality",
                    default="-"
                )


                with st.expander(
                    f"{name} • {guest_id} • {tier.upper()} • {country}"
                ):

                    st.write(
                        T["email"],
                        get_guest_value(
                            guest,
                            "email",
                            default="-"
                        )
                    )

                    st.write(
                        T["phone"],
                        get_guest_value(
                            guest,
                            "phone",
                            "mobile",
                            default="-"
                        )
                    )


                    if st.button(
                        f'{T["choose"]} {name}',
                        key=f"guest_{guest_id}",
                        use_container_width=True
                    ):

                        st.session_state.selected_guest = (
                            guest
                        )

                        st.session_state.selected_guest_id = (
                            guest_id
                        )

                        st.rerun()


# =========================================================
# SELECTED GUEST
# =========================================================

guest = (
    st.session_state.selected_guest
)

guest_id = (
    st.session_state.selected_guest_id
)


if not guest:

    st.stop()


name = guest_full_name(
    guest
)

tier = get_guest_value(
    guest,
    "tier",
    default="-"
)

country = get_guest_value(
    guest,
    "country",
    "nationality",
    default="-"
)

email = get_guest_value(
    guest,
    "email",
    default="-"
)

phone = get_guest_value(
    guest,
    "phone",
    "mobile",
    default="-"
)

guest_language = get_guest_value(
    guest,
    "language",
    default="-"
)


# =========================================================
# PROFILE
# =========================================================

st.markdown(
    f"""
<div class="gold-title">
👤 {T["profile"]}
</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    f"""
<div class="guest-card">

<div class="guest-name">
{name}
</div>

<div class="muted">
Guest ID: {guest_id}
</div>

<br>

<b>{T["tier"]}:</b>
<span class="gold">
{str(tier).upper()}
</span>

<br>

<b>{T["country"]}:</b>
{country}

<br>

<b>{T["language"]}:</b>
{guest_language}

<br>

<b>{T["email"]}:</b>
{email}

<br>

<b>{T["phone"]}:</b>
{phone}

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# SECTION MENU
# =========================================================

section = st.selectbox(
    "Guest section",
    [
        T["overview"],
        T["gaming"],
        T["hotel"],
        T["dining"],
        T["automation"],
        T["reports"],
        T["contact"],
    ]
)


# =========================================================
# OVERVIEW
# =========================================================

if section == T["overview"]:

    stats = guest_statistics(
        guest_id
    )

    inactive = inactivity_status(
        guest_id
    )

    primary_game = guest_primary_game(
        guest_id
    )

    frequency = average_days_between_visits(
        guest_id
    )


    c1, c2, c3 = st.columns(
        3
    )

    c1.metric(
        T["visits"],
        stats.get(
            "visits",
            0
        )
    )

    c2.metric(
        T["gaming_hours"],
        f'{stats.get("total_gaming_hours", 0):.1f} h'
    )

    c3.metric(
        T["primary_game"],
        primary_game
        or "-"
    )


    c4, c5, c6 = st.columns(
        3
    )

    c4.metric(
        T["average_bet"],
        f'€{stats.get("average_bet", 0):,.2f}'
    )

    c5.metric(
        T["turnover"],
        f'€{stats.get("turnover", 0):,.2f}'
    )

    c6.metric(
        T["theoretical"],
        f'€{stats.get("theoretical_value", 0):,.2f}'
    )


    st.markdown(
        f"""
<div class="card">

<b>{T["winloss"]}:</b>
€{stats.get("casino_win_loss", 0):,.2f}

<br><br>

<b>{T["days_inactive"]}:</b>
{inactive.get("days_since_last_visit")}

<br>

<b>{T["crm_status"]}:</b>
{inactive.get("level")}

<br>

<b>{T["frequency"]}:</b>
{
    f'{frequency:.1f} days'
    if frequency is not None
    else '-'
}

</div>
""",
        unsafe_allow_html=True
    )


# =========================================================
# GAMING
# =========================================================

elif section == T["gaming"]:

    st.markdown(
        """
<div class="gold-title">
🎰 Gaming History & Analytics
</div>
""",
        unsafe_allow_html=True
    )


    stats = guest_statistics(
        guest_id
    )

    game_stats = (
        guest_game_type_statistics(
            guest_id
        )
    )


    c1, c2, c3, c4 = st.columns(
        4
    )

    c1.metric(
        T["gaming_hours"],
        f'{stats.get("total_gaming_hours", 0):.1f}'
    )

    c2.metric(
        T["average_bet"],
        f'€{stats.get("average_bet", 0):,.2f}'
    )

    c3.metric(
        T["winloss"],
        f'€{stats.get("casino_win_loss", 0):,.2f}'
    )

    c4.metric(
        T["theoretical"],
        f'€{stats.get("theoretical_value", 0):,.2f}'
    )


    if game_stats:

        rows = []

        for (
            game_type,
            values
        ) in game_stats.items():

            rows.append({
                "Game":
                    game_type,

                "Sessions":
                    values.get(
                        "sessions",
                        0
                    ),

                "Hours":
                    round(
                        values.get(
                            "hours",
                            0
                        ),
                        1
                    ),

                "Turnover €":
                    round(
                        values.get(
                            "turnover",
                            0
                        ),
                        2
                    ),

                "Win/Loss €":
                    round(
                        values.get(
                            "casino_win_loss",
                            0
                        ),
                        2
                    ),

                "Theoretical €":
                    round(
                        values.get(
                            "theoretical_value",
                            0
                        ),
                        2
                    ),
            })


        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )


    st.markdown(
        """
<div class="gold-title">
🗓️ Visit History
</div>
""",
        unsafe_allow_html=True
    )


    visits = guest_visits(
        guest_id
    )


    if not visits:

        st.info(
            "No visit history."
        )


    for visit in visits:

        arrival = visit.get(
            "arrival"
        )

        arrival_text = (
            arrival.strftime(
                "%d.%m.%Y %H:%M"
            )
            if arrival
            else "-"
        )


        title = (
            f'{arrival_text} • '
            f'{visit.get("visit_type", "Regular")} • '
            f'{visit.get("host", "-")}'
        )


        with st.expander(
            title
        ):

            hotel = visit.get(
                "hotel",
                {}
            )


            st.write(
                "**Promotion:**",
                visit.get(
                    "promotion",
                    "-"
                )
                or "-"
            )

            st.write(
                "**Hotel:**",
                hotel.get(
                    "name",
                    "-"
                )
                or "-"
            )

            st.write(
                "**Hotel nights:**",
                hotel.get(
                    "nights",
                    0
                )
            )

            st.write(
                "**Hotel total:**",
                f'€{hotel.get("total_cost", 0):,.2f}'
            )

            st.write(
                "**GCP coverage:**",
                f'€{hotel.get("casino_coverage", 0):,.2f}'
            )


            games = visit.get(
                "games",
                []
            )


            for game in games:

                st.markdown(
                    f"""
<div class="card">

<b class="gold">
{game.get("game_type", "-")}
</b>

<br><br>

Duration:
{game.get("duration_hours", 0):.1f} h

<br>

Average bet:
€{game.get("average_bet", 0):,.2f}

<br>

Turnover:
€{game.get("turnover", 0):,.2f}

<br>

Casino Win/Loss:
€{game.get("casino_win_loss", 0):,.2f}

<br>

Theoretical:
€{game.get("theoretical_value", 0):,.2f}

</div>
""",
                    unsafe_allow_html=True
                )


# =========================================================
# HOTEL
# =========================================================

elif section == T["hotel"]:

    st.markdown(
        f"""
<div class="gold-title">
🏨 {T["hotel_title"]}
</div>
""",
        unsafe_allow_html=True
    )


    st.info(
        T["external_hotel"]
    )


    tier_normalized = normalize_tier(
        tier
    )


    policy = get_hotel_policy(
        tier_normalized
    )


    if tier_normalized == "gold":

        st.success(
            "Gold: max €150/night × 2 nights = €300."
        )

    elif tier_normalized == "vip":

        st.success(
            "VIP: max €200/night × 3 nights = €600."
        )

    elif tier_normalized == "silver":

        st.warning(
            "Silver: no automatic hotel benefit."
        )

    elif tier_normalized == "chairman":

        st.info(
            "Chairman: host / management approval."
        )

    elif tier_normalized == "new":

        st.info(
            "New guest pays hotel first. Reimbursement can be reviewed after play."
        )


    if policy.get(
        "type"
    ) == "fixed_cap":

        nights = st.number_input(
            T["nights"],
            min_value=1,
            max_value=30,
            value=1
        )


        price = st.number_input(
            T["night_price"],
            min_value=0.0,
            value=150.0,
            step=10.0
        )


        if st.button(
            T["calculate"],
            use_container_width=True
        ):

            result = calculate_hotel_coverage(
                tier,
                nights,
                price
            )


            c1, c2, c3 = st.columns(
                3
            )

            c1.metric(
                T["room_total"],
                f'€{result["total_room_cost"]:,.2f}'
            )

            c2.metric(
                T["casino_cover"],
                f'€{result["casino_covered"]:,.2f}'
            )

            c3.metric(
                T["guest_difference"],
                f'€{result["guest_room_difference"]:,.2f}'
            )


            st.warning(
                T["extras"]
            )


    elif policy.get(
        "type"
    ) == "post_play_review":

        hotel_paid = st.number_input(
            T["hotel_paid"],
            min_value=0.0,
            value=150.0
        )


        loss = st.number_input(
            T["loss"],
            min_value=0.0,
            value=0.0
        )


        hours = st.number_input(
            T["hours"],
            min_value=0.0,
            value=0.0,
            step=.5
        )


        game_type = st.selectbox(
            T["game_type"],
            [
                "Slots",
                "Roulette",
                "Blackjack",
                "Baccarat",
                "Poker",
                "Mixed Play",
                "Other",
            ]
        )


        notes = st.text_area(
            T["notes"]
        )


        if st.button(
            T["ticket"],
            use_container_width=True
        ):

            ticket = build_new_guest_review_ticket(
                name,
                guest_id,
                hotel_paid,
                loss,
                hours,
                game_type,
                notes,
            )


            ticket_text = format_new_guest_ticket(
                ticket
            )


            st.code(
                ticket_text
            )


            st.link_button(
                "💬 WhatsApp Host",
                whatsapp_url(
                    ticket_text
                ),
                use_container_width=True
            )


# =========================================================
# DINING
# =========================================================

elif section == T["dining"]:

    st.markdown(
        f"""
<div class="gold-title">
🍽️ {T["restaurant"]}
</div>
""",
        unsafe_allow_html=True
    )


    meal = st.selectbox(
        T["meal"],
        [
            "dinner",
            "lunch",
        ],
        format_func=lambda x:
            T["dinner"]
            if x == "dinner"
            else T["lunch"]
    )


    booking_date = st.date_input(
        T["date"]
    )


    party_size = st.number_input(
        T["party"],
        min_value=1,
        max_value=20,
        value=2
    )


    check = restaurant_eligibility(
        tier,
        meal,
        booking_date.weekday()
    )


    st.markdown(
        f"""
<div class="card">

<b>
{check["from"]} – {check["to"]}
</b>

<br>

{T["last_arrival"]}:
<b>
{check["last_arrival"]}
</b>

</div>
""",
        unsafe_allow_html=True
    )


    if not check[
        "service_open"
    ]:

        st.error(
            T["closed"]
        )


    elif not check[
        "tier_allowed"
    ]:

        st.warning(
            T["not_eligible"]
        )


    else:

        st.success(
            T["eligible"]
        )


        reservation = (
            "GCP RESTAURANT RESERVATION\n\n"
            f"Guest: {name}\n"
            f"Guest ID: {guest_id}\n"
            f"Tier: {tier}\n"
            f"Date: {booking_date}\n"
            f"Service: {meal}\n"
            f"Persons: {party_size}"
        )


        st.link_button(
            "💬 Prepare reservation",
            whatsapp_url(
                reservation
            ),
            use_container_width=True
        )


# =========================================================
# CRM AUTOMATION
# =========================================================

elif section == T["automation"]:

    st.markdown(
        """
<div class="gold-title">
🤖 CRM & Host Automation
</div>
""",
        unsafe_allow_html=True
    )


    snapshot = build_host_snapshot(
        guest_id=guest_id,
        tier=tier,

        marketing_allowed=guest.get(
            "marketing_allowed",
            True
        ),

        self_excluded=guest.get(
            "self_excluded",
            False
        ),

        blocked=guest.get(
            "blocked",
            False
        ),

        do_not_contact=guest.get(
            "do_not_contact",
            False
        ),
    )


    inactive = snapshot.get(
        "inactivity",
        {}
    )


    c1, c2 = st.columns(
        2
    )


    c1.metric(
        T["days_inactive"],
        inactive.get(
            "days_since_last_visit"
        )
        if inactive.get(
            "days_since_last_visit"
        ) is not None
        else "-"
    )


    c2.metric(
        T["crm_status"],
        inactive.get(
            "level",
            "-"
        )
    )


    contact_ok = snapshot.get(
        "contact_allowed",
        False
    )


    if contact_ok:

        st.success(
            "Marketing / host contact allowed."
        )

    else:

        st.error(
            "Marketing contact blocked for this guest."
        )


    st.markdown(
        """
<div class="gold-title">
Host Actions
</div>
""",
        unsafe_allow_html=True
    )


    actions = snapshot.get(
        "host_actions",
        []
    )


    for action in actions:

        st.markdown(
            f"""
<div class="card">

<b class="gold">
{action.get("title", action.get("action", "-"))}
</b>

<br><br>

Priority:
<b>{action.get("priority", "-")}</b>

<br>

{action.get("message", "")}

</div>
""",
            unsafe_allow_html=True
        )


# =========================================================
# REPORTS
# =========================================================

elif section == T["reports"]:

    st.markdown(
        """
<div class="gold-title">
📊 Guest Report
</div>
""",
        unsafe_allow_html=True
    )


    report = guest_report(
        guest_id,
        guest
    )


    text_report = guest_report_text(
        report
    )


    st.code(
        text_report
    )


    stats = guest_statistics(
        guest_id
    )


    c1, c2, c3 = st.columns(
        3
    )


    c1.metric(
        "Hotel Cost",
        f'€{stats.get("hotel_total_cost", 0):,.2f}'
    )


    c2.metric(
        "GCP Hotel Coverage",
        f'€{stats.get("casino_hotel_coverage", 0):,.2f}'
    )


    c3.metric(
        "Hotel Reimbursements",
        f'€{stats.get("hotel_reimbursements", 0):,.2f}'
    )


# =========================================================
# CONTACT
# =========================================================

elif section == T["contact"]:

    st.markdown(
        """
<div class="gold-title">
📲 Guest Contact
</div>
""",
        unsafe_allow_html=True
    )


    message = (
        "Grand Casino Portorož\n"
        "Casino Host AI\n\n"
        f"Guest: {name}\n"
        f"Guest ID: {guest_id}\n"
        f"Tier: {tier}"
    )


    st.link_button(
        f'💬 {T["whatsapp"]}',
        whatsapp_url(
            message
        ),
        use_container_width=True
    )


    email_link = mailto_url(
        email,
        "Grand Casino Portorož",
        f"Dear {name},\n\n"
    )


    if email_link:

        st.link_button(
            f'✉️ {T["email_guest"]}',
            email_link,
            use_container_width=True
        )


    call_link = tel_url(
        phone
    )


    if call_link:

        st.link_button(
            f'📞 {T["call"]}',
            call_link,
            use_container_width=True
        )


# =========================================================
# NEW GUEST
# =========================================================

st.divider()


if st.button(
    f'← {T["another"]}',
    use_container_width=True
):

    st.session_state.selected_guest = None
    st.session_state.selected_guest_id = None

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<br><br>

<div style="
text-align:center;
color:#777;
font-size:11px;
letter-spacing:1px;
">

GRAND CASINO PORTOROŽ — CASINO HOST AI DEMO

<br>

Demonstration prototype • Not an official production system

</div>
""",
    unsafe_allow_html=True
)