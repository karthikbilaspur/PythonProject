import random

def read_tarot_deck(filename: str):
    with open(filename, "r") as file_handle:
        return file_handle.readlines()

def draw_cards(deck: list[str], num_cards: int) -> list[str]:
    return random.sample(deck, num_cards)

def print_card(card: str) -> None:
    print(card.strip())

def youve_chosen_yes(deck: list[str]) -> None:
    print("I see that you've chosen to divine your future....")
    input(">> press enter")
    print("Let's make haste then...")
    input(">> press enter")
    print("Neither fame nor fortune wait for man")
    input(">> press enter")
    print()
    print("You have drawn three cards")
    print()
    cards = draw_cards(deck, 3)
    for i, card in enumerate(cards):
        print(f"Your {['first', 'second', 'third'][i]} card is...")
        print_card(card)
        input(">> press enter")
        print()

def youve_chosen_no():
    print("Are you wise...")
    input(">> press enter")
    print("Or foolish?")
    input(">> press enter")
    print("I suppose only time will tell")
    input(">> press enter")

def youve_chosen_neither():
    print("*le sigh*")
    input(">> press enter")
    print("I suppose you think this is a game...")
    input(">> press enter")
    print("You wouldn't be wrong...")
    input(">> press enter")
    print("But the only thing that you've played...")
    input(">> press enter")
    print("Is yourself.")
    input(">> press enter")
    print("\nNever gonna give you up,\nNever gonna let you down,\nNever gonna run around and desert you.\nNever gonna make you cry,\nNever gonna say goodbye,\nNever gonna tell a lie and hurt you.\n")

def main():
    deck = read_tarot_deck("./Tarot Reader/tarot.txt")
    print("In this black box, you read white words")
    input(">> press enter")
    print("Words that might warn you of danger...")
    input(">> press enter")
    print("Words that might foretell great fortune...")
    input(">> press enter")
    print("Or words that might make you laugh")
    input(">> press enter")
    print()
    print("Do you dare draw a card?")
    ch = input(">> enter Y/n: ")
    print("\nInteresting...")
    if ch.lower() == 'y':
        youve_chosen_yes(deck)
    elif ch.lower() == 'n':
        youve_chosen_no()
    else:
        youve_chosen_neither()
    print("Whichever your choice was...")
    input(">> press enter")
    print("May the cards ever be in your favour")
    input(">> press enter")
    print()
    print("\x1B[3mFin\x1B[23m".center(72))
    print("*"*72)

if __name__ == "__main__":
    main()