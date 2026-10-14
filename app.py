import os
import streamlit as st

from search import (
    search_guests,
    get_guest_value,
    guest_full_name,
)

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Grand Casino Portorož — Casino Host AI Demo",
    page_icon="♠️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top, #261d08 0%, #101010 32%, #050505 75%);
    color: #ffffff;
}

.block-container {
    max-width: 1180px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

.hero {
    background: linear-gradient(135deg, #0a0a0a, #2b2108, #080808);
    border: 1px solid #b9952b;
    border-radius: 22px;
    padding: 28px 20px;
    text-align: center;
    margin-bottom: 22px;
    box-shadow: 0 0 35px rgba(212,175,55,0.12);
}

.hero-small {
    color: #d9bd69;
    font-size: 12px;
    letter-spacing: 5px;
    font-weight: 700;
}

.hero-title {
    color: #e4c45c;
    font-size: 42px;
    font-weight: 700;
    margin-top: 8px;
}

.hero-subtitle {
    color: #ffffff;
    font-size: 20px;
    margin-top: 6px;
}

.hero-info {
    color: #c3c3c3;
    font-size: 14px;
    margin-top: 8px;
}

.demo-badge {
    display: inline-block;
    margin-top: 14px;
    padding: 6px 15px;
    border-radius: 30px;
    border: 1px solid #b9952b;
    color: #e5c866;
    font-size: 11px;
    letter-spacing: 2px;
}

.section-title {
    color: #e2c14f;
    font-size: 24px;
    font-weight: 700;
    margin-top: 22px;
    margin-bottom: 12px;
}

.guest-card {
    background: linear-gradient(135deg, #191919, #0d0d0d);
    border: 1px solid #80691f;
    border-radius: 18px;
    padding: 22px;
    margin: 15px 0 20px 0;
}

.guest-name {
    font-size: 30px;
    font-weight: 700;
    color: #ffffff;
}

.guest-id {
    color: #999999;
    font-size: 13px;
    margin-top: 3px;
}

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 12px;
}

.badge-gold {
    background: linear-gradient(90deg, #7c5c00, #d4af37);
    color: #080808;
}

.badge-silver {
    background: linear-gradient(90deg, #6f6f6f, #d9d9d9);
    color: #111111;
}

.badge-platinum {
    background: linear-gradient(90deg, #9e9e9e, #eeeeee, #8c8c8c);
    color: #090909;
}

.badge-standard {
    border: 1px solid #777777;
    color: #dddddd;
}

.info-box {
    background: rgba(255,255,255,0.025);
    border: 1px solid #333333;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 10px;
}

.info-label {
    color: #ad944b;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.info-value {
    color: white;
    font-size: 16px;
    margin-top: 5px;
}

.offer-card {
    background: linear-gradient(145deg, #1c1c1c, #0d0d0d);
    border: 1px solid #4b4020;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
}

.offer-title {
    color: #e1c052;
    font-size: 20px;
    font-weight: 700;
}

.offer-description {
    color: #c8c8c8;
    font-size: 14px;
    margin-top: 6px;
}

div.stButton > button {
    background: linear-gradient(100deg, #171717, #2c240d) !important;
    color: #ead173 !important;
    border: 1px solid #806b29 !important;
    border-radius: 12px !important;
    min-height: 48px;
    font-weight: 600;
}

div.stButton > button:hover {
    background: linear-gradient(100deg, #30270d, #4c3b0f) !important;
    border-color: #d4af37 !important;
    color: white !important;
}

div[data-baseweb="input"] > div {
    background-color: #151515 !important;
    border: 1px solid #5d4c1c !important;
    border-radius: 12px !important;
}

input {
    color: white !important;
}

hr {
    border-color: #332b16 !important;
}

@media (max-width: 700px) {

    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
        padding-top: 0.6rem;
    }

    .hero {
        padding: 22px 10px;
        border-radius: 16px;
    }

    .hero-title {
        font-size: 27px;
    }

    .hero-subtitle {
        font-size: 16px;
    }

    .guest-name {
        font-size: 23px;
    }

    .guest-card {
        padding: 16px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PROMO IMAGE
# =========================================================

POSTER = "casino_demo_poster.png"

if os.path.exists(POSTER):
    st.image(
        POSTER,
        use_container_width=True
    )

# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">
<div class="hero-small">CASINO HOST AI</div>
<div class="hero-title">GRAND CASINO PORTOROŽ</div>
<div class="hero-subtitle">Intelligent VIP Guest Experience</div>
<div class="hero-info">
Hotel • Casino • Dining • VIP Events • Promotions • Transfers
</div>
<div class="demo-badge">DEMO CONCEPT</div>
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

if "active_section" not in st.session_state:
    st.session_state.active_section = "Dashboard"

# =========================================================
# HELPERS
# =========================================================

def value(guest, *keys):
    return get_guest_value(
        guest,
        *keys,
        default="-"
    )

def tier_badge(tier):

    tier_lower = str(tier).lower()

    if tier_lower == "gold":
        css = "badge-gold"

    elif tier_lower == "silver":
        css = "badge-silver"

    elif tier_lower == "platinum":
        css = "badge-platinum"

    else:
        css = "badge-standard"

    return f"""
<span class="badge {css}">
{str(tier).upper()} VIP
</span>
"""

# =========================================================
# SEARCH
# =========================================================

st.markdown(
    '<div class="section-title">🔎 VIP Guest Search</div>',
    unsafe_allow_html=True
)

query = st.text_input(
    "Search guest",
    label_visibility="collapsed",
    placeholder="Ime gosta, Guest ID, email ili telefon..."
)

if st.button(
    "🔍 PRONAĐI GOSTA",
    use_container_width=True
):

    if not query.strip():

        st.warning(
            "Upiši ime gosta, Guest ID, email ili telefon."
        )

    else:

        results = search_guests(query)

        if not results:

            st.error(
                "Gost nije pronađen."
            )

        elif len(results) == 1:

            guest_id, guest = results[0]

            st.session_state.selected_guest = guest
            st.session_state.selected_guest_id = guest_id
            st.session_state.active_section = "Dashboard"

            st.rerun()

        else:

            st.warning(
                f"Pronađeno je {len(results)} gostiju."
            )

            for guest_id, guest in results:

                name = guest_full_name(guest)

                tier = value(
                    guest,
                    "tier"
                )

                country = value(
                    guest,
                    "country",
                    "nationality"
                )

                with st.expander(
                    f"{name} • {guest_id} • {tier} • {country}"
                ):

                    st.write(
                        "Email:",
                        value(
                            guest,
                            "email"
                        )
                    )

                    st.write(
                        "Telefon:",
                        value(
                            guest,
                            "phone",
                            "telephone",
                            "mobile"
                        )
                    )

                    if st.button(
                        f"ODABERI {name.upper()}",
                        key=f"choose_{guest_id}",
                        use_container_width=True
                    ):

                        st.session_state.selected_guest = guest
                        st.session_state.selected_guest_id = guest_id
                        st.session_state.active_section = "Dashboard"

                        st.rerun()

# =========================================================
# SELECTED GUEST
# =========================================================

guest = st.session_state.selected_guest
guest_id = st.session_state.selected_guest_id

if guest:

    st.divider()

    name = guest_full_name(guest)

    tier = value(
        guest,
        "tier"
    )

    country = value(
        guest,
        "country",
        "nationality"
    )

    email = value(
        guest,
        "email"
    )

    phone = value(
        guest,
        "phone",
        "telephone",
        "mobile"
    )

    st.markdown(
        '<div class="section-title">👤 VIP Guest Profile</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
<div class="guest-card">
<div class="guest-name">{name}</div>
<div class="guest-id">Guest ID: {guest_id}</div>
{tier_badge(tier)}
</div>
""",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
<div class="info-box">
<div class="info-label">Country</div>
<div class="info-value">{country}</div>
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="info-box">
<div class="info-label">Email</div>
<div class="info-value">{email}</div>
</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
<div class="info-box">
<div class="info-label">VIP Tier</div>
<div class="info-value">{tier}</div>
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="info-box">
<div class="info-label">Telephone</div>
<div class="info-value">{phone}</div>
</div>
""",
            unsafe_allow_html=True
        )

    # =====================================================
    # SERVICES
    # =====================================================

    st.markdown(
        '<div class="section-title">✨ Casino Host Services</div>',
        unsafe_allow_html=True
    )

    row1 = st.columns(3)

    with row1[0]:

        if st.button(
            "🏨 HOTEL",
            use_container_width=True
        ):
            st.session_state.active_section = "Hotel"
            st.rerun()

    with row1[1]:

        if st.button(
            "🎁 PROMOCIJE",
            use_container_width=True
        ):
            st.session_state.active_section = "Promotions"
            st.rerun()

    with row1[2]:

        if st.button(
            "🥂 VIP EVENTS",
            use_container_width=True
        ):
            st.session_state.active_section = "Events"
            st.rerun()

    row2 = st.columns(3)

    with row2[0]:

        if st.button(
            "🍽️ DINING",
            use_container_width=True
        ):
            st.session_state.active_section = "Dining"
            st.rerun()

    with row2[1]:

        if st.button(
            "🎰 CASINO OFFERS",
            use_container_width=True
        ):
            st.session_state.active_section = "Casino"
            st.rerun()

    with row2[2]:

        if st.button(
            "🚘 VIP TRANSFER",
            use_container_width=True
        ):
            st.session_state.active_section = "Transfer"
            st.rerun()

    active = st.session_state.active_section

    # =====================================================
    # DASHBOARD
    # =====================================================

    if active == "Dashboard":

        st.markdown(
            """
<div class="offer-card">
<div class="offer-title">Personalised VIP Experience</div>
<div class="offer-description">
Odaberi jednu od usluga iznad kako bi sustav prikazao
ponude i pogodnosti za odabranog gosta.
</div>
</div>
""",
            unsafe_allow_html=True
        )

    # =====================================================
    # HOTEL
    # =====================================================

    elif active == "Hotel":

        st.markdown(
            '<div class="section-title">🏨 Hotel & Accommodation</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="offer-card">
<div class="offer-title">VIP Hotel Stay</div>
<div class="offer-description">
Provjera raspoloživih soba, complimentary boravka,
VIP smještaja i posebnih casino cijena.
</div>
</div>
""",
            unsafe_allow_html=True
        )

        st.date_input(
            "Datum dolaska"
        )

        st.number_input(
            "Broj noćenja",
            min_value=1,
            max_value=30,
            value=1
        )

        st.button(
            "🔎 PROVJERI RASPOLOŽIVOST",
            use_container_width=True
        )

    # =====================================================
    # PROMOTIONS
    # =====================================================

    elif active == "Promotions":

        st.markdown(
            '<div class="section-title">🎁 VIP Promotions</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="offer-card">
<div class="offer-title">VIP Weekend Experience</div>
<div class="offer-description">
Casino experience • Dinner invitation • Personalised host service
</div>
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="offer-card">
<div class="offer-title">Exclusive Guest Promotion</div>
<div class="offer-description">
Posebna ponuda prilagođena VIP statusu gosta.
</div>
</div>
""",
            unsafe_allow_html=True
        )

    # =====================================================
    # EVENTS
    # =====================================================

    elif active == "Events":

        st.markdown(
            '<div class="section-title">🥂 VIP Events</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="offer-card">
<div class="offer-title">Saturday VIP Dinner & Casino Night</div>
<div class="offer-description">
Ekskluzivna večera i premium casino iskustvo.
</div>
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="offer-card">
<div class="offer-title">Private Tournament Invitation</div>
<div class="offer-description">
Poziv za odabrane premium goste.
</div>
</div>
""",
            unsafe_allow_html=True
        )

    # =====================================================
    # DINING
    # =====================================================

    elif active == "Dining":

        st.markdown(
            '<div class="section-title">🍽️ VIP Dining</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="offer-card">
<div class="offer-title">Complimentary Dinner</div>
<div class="offer-description">
VIP rezervacija stola i posebna dining ponuda.
</div>
</div>
""",
            unsafe_allow_html=True
        )

        st.number_input(
            "Broj osoba",
            min_value=1,
            max_value=20,
            value=2
        )

        st.button(
            "🍽️ REZERVIRAJ STOL",
            use_container_width=True
        )

    # =====================================================
    # CASINO
    # =====================================================

    elif active == "Casino":

        st.markdown(
            '<div class="section-title">🎰 Personalised Casino Offers</div>',
            unsafe_allow_html=True
        )

        if str(tier).lower() == "platinum":

            recommendation = (
                "Premium Platinum Experience • VIP Host • "
                "Exclusive Casino Benefits"
            )

        elif str(tier).lower() == "gold":

            recommendation = (
                "Gold VIP Experience • Dinner Invitation • "
                "Special Casino Promotion"
            )

        elif str(tier).lower() == "silver":

            recommendation = (
                "Silver Upgrade Promotion • Special Casino Benefits"
            )

        else:

            recommendation = (
                "Personalised casino offer based on guest profile."
            )

        st.markdown(
            f"""
<div class="offer-card">
<div class="offer-title">AI Recommended Offer</div>
<div class="offer-description">
{recommendation}
</div>
</div>
""",
            unsafe_allow_html=True
        )

    # =====================================================
    # TRANSFER
    # =====================================================

    elif active == "Transfer":

        st.markdown(
            '<div class="section-title">🚘 VIP Transfer</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="offer-card">
<div class="offer-title">Private VIP Transfer</div>
<div class="offer-description">
Organizacija prijevoza gosta do Grand Casino Portorož,
hotela ili druge lokacije.
</div>
</div>
""",
            unsafe_allow_html=True
        )

        st.text_input(
            "Mjesto preuzimanja"
        )

        st.button(
            "🚘 ORGANIZIRAJ TRANSFER",
            use_container_width=True
        )

    # =====================================================
    # CONTACT
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">📲 Contact Guest</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.button(
            "💬 WhatsApp",
            use_container_width=True
        )

    with c2:
        st.button(
            "✉️ Email",
            use_container_width=True
        )

    with c3:
        st.button(
            "📞 Call",
            use_container_width=True
        )

    st.divider()

    if st.button(
        "← ODABERI DRUGOG GOSTA",
        use_container_width=True
    ):

        st.session_state.selected_guest = None
        st.session_state.selected_guest_id = None
        st.session_state.active_section = "Dashboard"

        st.rerun()

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div style="
text-align:center;
color:#777;
font-size:11px;
letter-spacing:1px;
margin-top:35px;
">
GRAND CASINO PORTOROŽ — CASINO HOST AI DEMO CONCEPT
<br><br>
Demonstration prototype • Not an official production system
</div>
""",
    unsafe_allow_html=True
)