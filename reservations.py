from datetime import datetime
from guests import full_name


reservations = []


def create_reservation(guest):

    print("\n=== NOVA REZERVACIJA ===")

    arrival = input("Datum dolaska: ").strip()
    departure = input("Datum odlaska: ").strip()
    persons = input("Broj osoba: ").strip()

    reservation = {
        "guest_id": guest["guest_id"],
        "guest_name": full_name(guest),
        "tier": guest["tier"],
        "arrival": arrival,
        "departure": departure,
        "persons": persons,
        "status": "CONFIRMED",
        "created": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )
    }

    reservations.append(reservation)

    print()
    print("Rezervacija uspješno kreirana.")
    print("Guest ID:", guest["guest_id"])
    print("Gost:", full_name(guest))
    print("Dolazak:", arrival)
    print("Odlazak:", departure)
    print("Broj osoba:", persons)


def show_reservations():

    print("\n=== SVE REZERVACIJE ===")

    if not reservations:

        print("Nema rezervacija.")
        return

    for reservation in reservations:

        print()
        print("Guest ID:", reservation["guest_id"])
        print("Gost:", reservation["guest_name"])
        print("Tier:", reservation["tier"])
        print("Dolazak:", reservation["arrival"])
        print("Odlazak:", reservation["departure"])
        print("Osobe:", reservation["persons"])
        print("Status:", reservation["status"])