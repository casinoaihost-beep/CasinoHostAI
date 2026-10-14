from promotions import show_promotions
from guests import full_name


conversation_history = {}


greetings = {
    "Croatian": "Pozdrav",
    "Italian": "Ciao",
    "German": "Guten Tag",
    "English": "Hello",
    "Russian": "Здравствуйте",
    "Slovenian": "Pozdravljeni",
    "French": "Bonjour",
    "Spanish": "Hola",
    "Portuguese": "Olá",
    "Polish": "Dzień dobry",
    "Czech": "Dobrý den",
    "Hungarian": "Üdvözlöm",
    "Turkish": "Merhaba",
    "Greek": "Γεια σας"
}


def build_reply(guest, message, tier_rules):

    guest_name = full_name(guest)
    language = guest["language"]
    tier = guest["tier"]

    greeting = greetings.get(
        language,
        "Hello"
    )

    if language == "Italian":

        answer = (
            f"{greeting} {guest_name}! "
            "Sarò felice di aiutarti. "
            "Posso controllare offerte, hotel, "
            "cena e prenotazioni."
        )

    elif language == "German":

        answer = (
            f"{greeting} {guest_name}! "
            "Ich helfe Ihnen gerne. "
            "Ich kann Angebote, Hotel, "
            "Abendessen und Reservierungen prüfen."
        )

    elif language == "Croatian":

        answer = (
            f"{greeting} {guest_name}! "
            "Rado ću vam pomoći. "
            "Mogu provjeriti ponude, hotel, "
            "večeru i rezervacije."
        )

    elif language == "Russian":

        answer = (
            f"{greeting}, {guest_name}! "
            "Я с удовольствием помогу вам."
        )

    else:

        answer = (
            f"{greeting} {guest_name}! "
            "I will be happy to assist you."
        )

    if tier_rules[tier]["human_approval"]:

        answer += (
            f"\n\n⚠ {tier} gost. "
            "Za određene odluke potrebna je "
            f"potvrda hosta: {guest['human_host']}."
        )

    return answer


def start_chat(guest, tier_rules):

    guest_id = guest["guest_id"]
    guest_name = full_name(guest)

    if guest_id not in conversation_history:
        conversation_history[guest_id] = []

    print()
    print("=== CASINOHOST AI CHAT ===")
    print("Gost:", guest_name)
    print("Guest ID:", guest_id)
    print("Za povratak upiši 0.")
    print()

    while True:

        message = input("Gost: ").strip()

        if message == "0":
            break

        if not message:
            continue

        conversation_history[guest_id].append({
            "role": "guest",
            "message": message
        })

        reply = build_reply(
            guest,
            message,
            tier_rules
        )

        conversation_history[guest_id].append({
            "role": "host",
            "message": reply
        })

        print()
        print("CasinoHost:")
        print(reply)

        print()
        print("Tier:", guest["tier"])
        print("Bodovi:", guest["points"])

        if guest["hotel"]:
            print("Hotel pogodnost: DA")

        if guest["dinner"]:
            print("Večera: DA")

        show_promotions(guest)

        print()


def show_conversation(guest):

    guest_id = guest["guest_id"]

    print("\n=== POVIJEST RAZGOVORA ===")

    history = conversation_history.get(
        guest_id,
        []
    )

    if not history:

        print("Nema razgovora.")
        return

    for item in history:

        print()
        print(item["role"].upper() + ":")
        print(item["message"])