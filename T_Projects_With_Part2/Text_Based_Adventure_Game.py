import time
import random

def print_delay(text:str, delay:float=1):
    print(text)
    time.sleep(delay)

def intro():
    print_delay("You wake up in a dark, mysterious room.")
    print_delay("You can't remember how you got here.")
    print_delay("As you look around, you see two doors in front of you.")
    print_delay("One door is red, and the other door is blue.")

def choose_door():
    door = ""
    while door not in ["red", "blue"]:
        door = input("Which door do you choose? (red/blue): ").lower()
    return door

def red_door_scenario():
    print_delay("You open the red door and find yourself in a fiery cave.")
    print_delay("There's a dragon sleeping in the middle of the cave!")
    print_delay("You can either:")
    print_delay("1. Try to sneak around the dragon.")
    print_delay("2. Grab a nearby sword and fight the dragon.")

    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Enter 1 or 2: ")

    if choice == "1":
        print_delay("You try to sneak around the dragon.")
        if random.random() < 0.5:
            print_delay("You successfully sneak past the dragon!")
            print_delay("You find a treasure chest filled with gold and gems!")
            return 100
        else:
            print_delay("Unfortunately, the dragon wakes up and chases you!")
            print_delay("You barely manage to escape through the red door.")
            return 0
    elif choice == "2":
        print_delay("You pick up the sword and bravely attack the dragon.")
        if random.random() < 0.7:
            print_delay("After an intense battle, you defeat the dragon!")
            print_delay("You find a treasure chest behind the dragon's nest.")
            print_delay("The chest contains valuable gems and gold!")
            return 150
        else:
            print_delay("The dragon is too powerful, and you are defeated.")
            return -50

def blue_door_scenario():
    print_delay("You open the blue door and find yourself in a peaceful garden.")
    print_delay("There's a friendly fairy sitting on a bench.")
    print_delay("The fairy offers you a magical potion.")
    print_delay("You can either:")
    print_delay("1. Drink the potion.")
    print_delay("2. Politely decline the offer.")

    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Enter 1 or 2: ")

    if choice == "1":
        print_delay("You drink the potion and feel a sudden burst of energy.")
        print_delay("Your memory is restored, and you remember everything!")
        print_delay("The fairy thanks you for accepting her gift.")
        return 100
    elif choice == "2":
        print_delay("You politely decline the potion.")
        print_delay("The fairy understands and smiles at you.")
        print_delay("You feel a sense of peace in the garden.")
        return 50

def secret_room_scenario():
    print_delay("You find a hidden passage behind the bookshelf.")
    print_delay("You enter a mysterious room filled with ancient artifacts.")
    print_delay("In the center of the room, there's a glowing amulet.")
    print_delay("You can either:")
    print_delay("1. Take the amulet.")
    print_delay("2. Leave the room without taking anything.")

    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Enter 1 or 2: ")

    if choice == "1":
        print_delay("You take the amulet, and it starts to shine even brighter.")
        print_delay("Suddenly, you feel a surge of power flowing through you.")
        return 200
    elif choice == "2":
        print_delay("You decide not to touch anything and leave the room.")
        print_delay("As you exit the secret room, you feel a sense of relief.")
        return 50

def play_game():
    score = 0
    intro()
    chosen_door = choose_door()

    if chosen_door == "red":
        score += red_door_scenario()
    elif chosen_door == "blue":
        score += blue_door_scenario()

    print_delay("You continue exploring and find a hidden door behind a bookshelf.")
    print_delay("Do you want to open the door?")
    hidden_door_choice = input("Enter 'yes' or 'no': ").lower()

    if hidden_door_choice == "yes":
        score += secret_room_scenario()

    print_delay(f"Your final score is: {score}")

if __name__ == "__main__":
    play_game()