from guests import guests, full_name
from tiers import tier_rules
from hotels import show_hotels
from promotions import show_promotions
from reservations import (
    create_reservation,
    show_reservations
)
from ai_host import (
    start_chat,
    show_conversation
)
from search import (
    search_guests,
    choose_guest,
    masked_phone
)


def show_guest(guest):

    print("\n=== PROFIL GOSTA ===")

    print("Guest ID:", guest["guest_id"])
    print("Ime:", full_name(guest))
    print("Tier:", guest["tier"])
    print("Jezik:", guest["language"])
    print("Država:", guest["country"])
    print("Bodovi:", guest["points"])
    print("Zadnji posjet:", guest["last_visit"])
    print("Omiljena igra:", guest["preferred_game"])
    print("Email:", guest["email"])
    print("Telefon:", guest["phone"])

    if guest["human_host"]:
        print(
            "Osobni host:",
            guest["human_host"]
        )


def nexio_demo(guest):

    print("\n=== NEXIO DEMO ===")

    print(
        "SIMULIRANI PODACI IZ NEXIO CRM-a"
    )

    print("Guest ID:", guest["guest_id"])
    print("Gost:", full_name(guest))
    print("Tier:", guest["tier"])
    print("Bodovi:", guest["points"])
    print("Zadnji posjet:", guest["last_visit"])
    print("Igra:", guest["preferred_game"])

    print()
    print(
        "Kasnije će ovaj dio koristiti "
        "pravi Nexio connector."
    )


def guest_menu(guest):

    while True:

        print()
        print("=================================")
        print("CASINOHOST AI")
        print("Guest ID:", guest["guest_id"])
        print("Gost:", full_name(guest))
        print("Tier:", guest["tier"])
        print("=================================")

        print("1 - Profil gosta")
        print("2 - Razgovor s AI hostom")
        print("3 - Hoteli")
        print("4 - Promocije")
        print("5 - Nova rezervacija")
        print("6 - Povijest razgovora")
        print("7 - Sve rezervacije")
        print("8 - Nexio demo")
        print("9 - WhatsApp")
        print("10 - Email")
        print("11 - Telefon")
        print("0 - Povratak")

        choice = input(
            "\nOdaberi: "
        ).strip()

        if choice == "1":

            show_guest(guest)

        elif choice == "2":

            start_chat(
                guest,
                tier_rules
            )

        elif choice == "3":

            show_hotels(
                guest,
                tier_rules
            )

        elif choice == "4":

            show_promotions(
                guest
            )

        elif choice == "5":

            create_reservation(
                guest
            )

        elif choice == "6":

            show_conversation(
                guest
            )

        elif choice == "7":

            show_reservations()

        elif choice == "8":

            nexio_demo(
                guest
            )

        elif choice == "9":

            print()
            print("=== WHATSAPP ===")
            print(
                "Sljedeće spajamo pravi "
                "Twilio WhatsApp test."
            )

        elif choice == "10":

            print()
            print("=== EMAIL ===")
            print(
                "Sljedeće spajamo pravi "
                "email connector."
            )

        elif choice == "11":

            print()
            print("=== TELEFON ===")
            print(
                "Kasnije spajamo pravi "
                "AI voice broj."
            )

        elif choice == "0":

            break

        else:

            print(
                "Nepoznata opcija."
            )


def find_guest_menu():

    print()
    print("=== PRONALAZAK GOSTA ===")

    print(
        "Možeš upisati ime, Guest ID, "
        "email ili telefon."
    )

    query = input(
        "Traži gosta: "
    ).strip()

    if not query:

        print("Nisi ništa upisao.")
        return

    results = search_guests(
        query
    )

    if not results:

        print(
            "Gost nije pronađen."
        )
        return

    guest = choose_guest(
        results
    )

    if guest:

        guest_menu(
            guest
        )


def show_all_guests():

    print()
    print("=== DEMO GOSTI ===")

    for guest_id, guest in guests.items():

        print(
            guest_id,
            "-",
            full_name(guest),
            "-",
            guest["tier"],
            "-",
            guest["country"],
            "-",
            masked_phone(guest["phone"])
        )


def main():

    while True:

        print()
        print("#################################")
        print("#       CASINOHOST AI v2        #")
        print("#################################")

        print()
        print("1 - Pronađi gosta")
        print("2 - Prikaži sve demo goste")
        print("3 - Sve rezervacije")
        print("0 - Izlaz")

        choice = input(
            "\nOdaberi: "
        ).strip()

        if choice == "1":

            find_guest_menu()

        elif choice == "2":

            show_all_guests()

        elif choice == "3":

            show_reservations()

        elif choice == "0":

            print(
                "CasinoHost AI ugašen."
            )
            break

        else:

            print(
                "Nepoznata opcija."
            )


if __name__ == "__main__":
    main()