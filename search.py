# search.py

import unicodedata

from guests import guests, full_name


def normalize_text(text):
    """
    Pretvara tekst u oblik pogodan za pretragu.

    Primjeri:
    Marco Rossi
    marco rossi
    MARCO ROSSI
      marco    rossi

    Sve će biti tretirano praktički jednako.
    """

    if text is None:
        return ""

    text = str(text).strip().lower()

    # uklanjanje naglasaka / dijakritike
    text = unicodedata.normalize("NFKD", text)

    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    # više razmaka pretvara u jedan
    text = " ".join(text.split())

    return text


def normalize_phone(phone):
    """
    Iz telefona ostavlja samo brojke.

    Primjeri:
    +385 91 123 4567
    385911234567
    +385-91-123-4567

    postaju isti format.
    """

    if phone is None:
        return ""

    return "".join(
        char
        for char in str(phone)
        if char.isdigit()
    )


def masked_phone(phone):
    """
    Sakriva dio telefonskog broja radi privatnosti.

    Primjer:
    +39 333 1234567

    prikaz:
    ******4567
    """

    phone_normalized = normalize_phone(phone)

    if not phone_normalized:
        return "-"

    if len(phone_normalized) <= 4:
        return phone_normalized

    return "*" * (len(phone_normalized) - 4) + phone_normalized[-4:]


def get_guest_value(guest, *keys, default=""):
    """
    Sigurno dohvaća vrijednost iz gosta čak i ako
    se naziv polja malo razlikuje.
    """

    for key in keys:
        if key in guest:
            value = guest.get(key)

            if value is not None:
                return value

    return default


def guest_full_name(guest):
    """
    Vraća ime i prezime gosta.
    """

    first_name = get_guest_value(
        guest,
        "first_name",
        "name"
    )

    last_name = get_guest_value(
        guest,
        "last_name",
        "surname"
    )

    return f"{first_name} {last_name}".strip()


def search_guests(query):
    """
    Glavna funkcija za traženje gosta.

    Redoslijed prioriteta:

    1. Guest ID
    2. Email
    3. Telefon
    4. Točno ime i prezime
    5. Djelomično ime/prezime
    """

    if not query:
        return []

    query_original = str(query).strip()

    if not query_original:
        return []

    query_normalized = normalize_text(query_original)
    query_phone = normalize_phone(query_original)

    exact_id_results = []
    exact_email_results = []
    exact_phone_results = []
    exact_name_results = []
    partial_results = []

    for guest_id, guest in guests.items():

        # -----------------------------
        # GUEST ID
        # -----------------------------

        normalized_guest_id = normalize_text(guest_id)

        if normalized_guest_id == query_normalized:
            exact_id_results.append(
                (guest_id, guest)
            )

        # -----------------------------
        # EMAIL
        # -----------------------------

        email = get_guest_value(
            guest,
            "email"
        )

        if email:

            if normalize_text(email) == query_normalized:
                exact_email_results.append(
                    (guest_id, guest)
                )

        # -----------------------------
        # TELEFON
        # -----------------------------

        phone = get_guest_value(
            guest,
            "phone",
            "telephone",
            "mobile"
        )

        guest_phone = normalize_phone(phone)

        if (
            query_phone
            and guest_phone
            and query_phone == guest_phone
        ):

            exact_phone_results.append(
                (guest_id, guest)
            )

        # -----------------------------
        # IME + PREZIME
        # -----------------------------

        name = guest_full_name(guest)

        normalized_name = normalize_text(name)

        if normalized_name == query_normalized:

            exact_name_results.append(
                (guest_id, guest)
            )

        # -----------------------------
        # DJELOMIČNA PRETRAGA
        # -----------------------------

        query_parts = query_normalized.split()

        name_parts = normalized_name.split()

        all_parts_found = all(
            any(
                query_part in name_part
                for name_part in name_parts
            )
            for query_part in query_parts
        )

        if (
            query_parts
            and all_parts_found
            and normalized_name != query_normalized
        ):

            partial_results.append(
                (guest_id, guest)
            )

    # Prioritet rezultata

    if exact_id_results:
        return exact_id_results

    if exact_email_results:
        return exact_email_results

    if exact_phone_results:
        return exact_phone_results

    if exact_name_results:
        return exact_name_results

    return partial_results


def choose_guest(results):
    """
    Ako je pronađen samo jedan gost,
    odmah ga vraća.

    Ako ih ima više,
    korisnik bira točnog gosta.
    """

    if not results:

        print(
            "\nGost nije pronađen.\n"
        )

        return None

    # samo jedan rezultat

    if len(results) == 1:

        guest_id, guest = results[0]

        return guest

    # više rezultata

    print(
        "\nPronađeno je više gostiju:\n"
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        guest_id, guest = result

        name = guest_full_name(guest)

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

        phone = get_guest_value(
            guest,
            "phone",
            "telephone",
            "mobile",
            default=""
        )

        print(
            f"{index}. "
            f"{name} | "
            f"ID: {guest_id} | "
            f"Tier: {tier} | "
            f"Država: {country} | "
            f"Tel: {masked_phone(phone)}"
        )

    while True:

        choice = input(
            "\nOdaberi broj gosta ili 0 za odustajanje: "
        ).strip()

        if choice == "0":

            return None

        if not choice.isdigit():

            print(
                "Molim upiši broj."
            )

            continue

        number = int(choice)

        if 1 <= number <= len(results):

            guest_id, guest = results[number - 1]

            return guest

        print(
            "Neispravan odabir."
        )