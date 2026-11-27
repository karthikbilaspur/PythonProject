
import random
from typing import TypedDict

MAX_HEALTH = 10


class Choice(TypedDict):
    text: str
    result: str
    item: str | None
    health: int


class Era(TypedDict):
    description: str
    choices: list[Choice]

# All the story lives in this dictionary, so the game code below stays short.
# Each choice has:
#   text   - what the player sees in the menu
#   result - what happens when they pick it
#   item   - an artifact they receive (or None)
#   health - change in health (negative = damage, positive = healing)
ERAS: dict[str, Era] = {
    "Ancient Egypt": {
        "description": "You are in Ancient Egypt, surrounded by pyramids and pharaohs.",
        "choices": [
            {"text": "Visit the Great Pyramid",
             "result": "You find a hidden chamber with a shiny treasure!",
             "item": "Golden Scarab", "health": 0},
            {"text": "Meet Pharaoh Khufu",
             "result": "The Pharaoh gives you his blessing. You feel stronger!",
             "item": None, "health": 2},
            {"text": "Explore the Nile River",
             "result": "A crocodile attacks! You escape, but you are hurt.",
             "item": None, "health": -3},
            {"text": "Visit the Temple of Karnak",
             "result": "You admire the giant stone columns. Beautiful!",
             "item": None, "health": 0},
        ],
    },
    "Medieval Europe": {
        "description": "You are in Medieval Europe, surrounded by castles and knights.",
        "choices": [
            {"text": "Attend a royal feast",
             "result": "You enjoy the music and food. You feel great!",
             "item": None, "health": 2},
            {"text": "Join a jousting tournament",
             "result": "You win the round, but get bruised.",
             "item": None, "health": -2},
            {"text": "Explore the forest",
             "result": "Birds sing and the trees are lovely. Nothing else happens.",
             "item": None, "health": 0},
            {"text": "Visit the local blacksmith",
             "result": "The blacksmith gives you a piece of knight's armor!",
             "item": "Armor Plate", "health": 0},
        ],
    },
    "Future City": {
        "description": "You are in a futuristic city, surrounded by skyscrapers and robots.",
        "choices": [
            {"text": "Visit the Space Station",
             "result": "You see the Earth from orbit. Amazing view!",
             "item": None, "health": 0},
            {"text": "Meet the City's AI",
             "result": "The AI is friendly and gives you a small chip.",
             "item": "AI Chip", "health": 0},
            {"text": "Explore the Undercity",
             "result": "You trip over a loose cable and get shocked!",
             "item": None, "health": -2},
            {"text": "Visit the Virtual Reality Center",
             "result": "You relax inside a calm virtual world.",
             "item": None, "health": 1},
        ],
    },
    "Ancient Greece": {
        "description": "You are in Ancient Greece, surrounded by philosophers and temples.",
        "choices": [
            {"text": "Visit the Parthenon",
             "result": "A kind guard hands you a golden leaf crown!",
             "item": "Laurel Wreath", "health": 0},
            {"text": "Meet Socrates",
             "result": "He asks you many questions. Your head hurts a bit, but you learn a lot.",
             "item": None, "health": 0},
            {"text": "Explore the Agora",
             "result": "A pickpocket bumps into you and you fall over!",
             "item": None, "health": -2},
            {"text": "Visit the Theater of Dionysus",
             "result": "You watch a funny play and feel much better.",
             "item": None, "health": 2},
        ],
    },
    "Wild West": {
        "description": "You are in the Wild West, surrounded by cowboys and outlaws.",
        "choices": [
            {"text": "Visit the local saloon",
             "result": "You drink some cold lemonade and rest.",
             "item": None, "health": 1},
            {"text": "Meet Wyatt Earp",
             "result": "Wyatt Earp trusts you and gives you a badge!",
             "item": "Sheriff's Badge", "health": 0},
            {"text": "Explore the desert",
             "result": "A rattlesnake bites you! Ouch!",
             "item": None, "health": -3},
            {"text": "Visit the local sheriff",
             "result": "You chat about the town's problems. Nothing else happens.",
             "item": None, "health": 0},
        ],
    },
}


def show_status(era: str, health: int, inventory: list[str]) -> None:
    """Print where the player is, their health, and what they carry."""
    print("\n" + "=" * 50)
    print(f"Era: {era}")
    print(ERAS[era]["description"])
    print(f"Health: {health}/{MAX_HEALTH}")
    print(f"Artifacts ({len(inventory)}/{len(ERAS)}): {', '.join(inventory) if inventory else 'none yet'}")
    print("=" * 50)


def show_menu(era: str) -> None:
    """Print the numbered choices for the current era."""
    choices = ERAS[era]["choices"]
    for number, choice in enumerate(choices, start=1):
        print(f"{number}. {choice['text']}")
    print("T. Use the time machine (travel to another era)")
    print("Q. Quit")


def travel(current_era: str) -> str:
    """Let the player pick a new era. Returns the new era name."""
    other_eras = [name for name in ERAS if name != current_era]
    print("\nWhere do you want to travel?")
    for number, name in enumerate(other_eras, start=1):
        print(f"{number}. {name}")
    answer = input("Enter a number: ").strip()
    if answer.isdigit() and 1 <= int(answer) <= len(other_eras):
        new_era = other_eras[int(answer) - 1]
        print(f"\nZZZZAP! The time machine takes you to {new_era}!")
        return new_era
    print("The time machine sputters. You stay where you are.")
    return current_era


def do_choice(era: str, choice_number: int, health: int, inventory: list[str]) -> int:
    """Run one story choice. Returns the new health."""
    choice = ERAS[era]["choices"][choice_number - 1]
    print("\n" + choice["result"])

    # Handle an artifact.
    item = choice["item"]
    if item is not None:
        if item in inventory:
            print(f"You already have the {item}.")
        else:
            inventory.append(item)
            print(f"*** You got the {item}! ***")

    # Handle health changes (never go above the maximum).
    health = min(MAX_HEALTH, health + choice["health"])
    if choice["health"] < 0:
        print(f"You lost {-choice['health']} health.")
    elif choice["health"] > 0:
        print(f"You gained {choice['health']} health.")
    return health


def game_loop():
    print("Welcome to the Time Travel Adventure Game!")
    print(f"Your time machine is broken. Find {len(ERAS)} artifacts, one from each era, to fix it.")

    era = random.choice(list(ERAS))
    health = MAX_HEALTH
    inventory: list[str] = []

    while True:
        show_status(era, health, inventory)
        show_menu(era)
        answer = input("What do you do? ").strip().lower()

        if answer == "q":
            print("Thanks for playing. Goodbye!")
            break
        elif answer == "t":
            era = travel(era)
        elif answer.isdigit() and 1 <= int(answer) <= len(ERAS[era]["choices"]):
            health = do_choice(era, int(answer), health, inventory)
        else:
            print("Invalid choice. Please try again.")
            continue

        # Check for winning or losing after every action.
        if len(inventory) == len(ERAS):
            print("\nYou collected every artifact and fixed the time machine!")
            print("You travel home safely. YOU WIN!")
            break
        if health <= 0:
            print("\nYou are too hurt to continue. GAME OVER.")
            break


# This line makes the game start only when you run the file directly.
if __name__ == "__main__":
    game_loop()