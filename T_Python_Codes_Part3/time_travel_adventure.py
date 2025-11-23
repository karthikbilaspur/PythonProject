import random

# Define a dictionary to store the time periods
time_periods = {
    "Ancient Egypt": {
        "description": "You are in Ancient Egypt, surrounded by pyramids and pharaohs.",
        "options": ["Visit the Great Pyramid", "Meet Pharaoh Khufu", "Explore the Nile River", "Visit the Temple of Karnak"],
        "items": ["Ancient Egyptian Scroll", "Pharaoh's Crown"]
    },
    "Medieval Europe": {
        "description": "You are in Medieval Europe, surrounded by castles and knights.",
        "options": ["Attend a royal feast", "Join a jousting tournament", "Explore the forest", "Visit the local blacksmith"],
        "items": ["Knight's Armor", "Royal Invitation"]
    },
    "Future City": {
        "description": "You are in a futuristic city, surrounded by skyscrapers and robots.",
        "options": ["Visit the Space Station", "Meet the City's AI", "Explore the Undercity", "Visit the Virtual Reality Center"],
        "items": ["Space Suit", "AI Chip"]
    },
    "Ancient Greece": {
        "description": "You are in Ancient Greece, surrounded by philosophers and temples.",
        "options": ["Visit the Parthenon", "Meet Socrates", "Explore the Agora", "Visit the Theater of Dionysus"],
        "items": ["Ancient Greek Scroll", "Laurel Wrench"]
    },
    "Wild West": {
        "description": "You are in the Wild West, surrounded by cowboys and outlaws.",
        "options": ["Visit the local saloon", "Meet Wyatt Earp", "Explore the desert", "Visit the local sheriff"],
        "items": ["Colt Revolver", "Sheriff's Badge"]
    }
}

# Define a function to display the current time period
def display_time_period(time_period: str):
    print(time_periods[time_period]["description"])
    print("Options:")
    for i, option in enumerate(time_periods[time_period]["options"]):
        print(f"{i+1}. {option}")

# Define a function to handle the player's choice
def handle_choice(time_period: str, choice: int):
    if time_period == "Ancient Egypt":
        if choice == 1:
            print("You visit the Great Pyramid and marvel at its grandeur.")
            return "Ancient Egypt", ["You found a hidden chamber with a treasure chest!"]
        elif choice == 2:
            print("You meet Pharaoh Khufu and discuss the secrets of the pyramids.")
            return "Ancient Egypt", ["You received a Pharaoh's blessing!"]
        elif choice == 3:
            print("You explore the Nile River and encounter a crocodile.")
            return "Ancient Egypt", ["You escaped the crocodile's attack!"]
        elif choice == 4:
            print("You visit the Temple of Karnak and admire the architecture.")
            return "Ancient Egypt", ["You found an ancient artifact!"]
    elif time_period == "Medieval Europe":
        if choice == 1:
            print("You attend a royal feast and enjoy the music and food.")
            return "Medieval Europe", ["You made new friends at the royal feast!"]
        elif choice == 2:
            print("You join a jousting tournament and win the heart of a fair maiden.")
            return "Medieval Europe", ["You got a prize for winning the tournament!"]
        elif choice == 3:
            print("You explore the forest and stumble upon a hidden treasure.")
            return "Medieval Europe", ["You found a chest of gold coins!"]
        elif choice == 4:
            print("You visit the local blacksmith and admire his work.")
            return "Medieval Europe", ["You got a new sword!"]
    elif time_period == "Future City":
        if choice == 1:
            print("You visit the Space Station and see the Earth from orbit.")
            return "Future City", ["You got a space mission badge!"]
        elif choice == 2:
            print("You meet the City's AI and discuss the future of humanity.")
            return "Future City", ["You got an AI upgrade!"]
        elif choice == 3:
            print("You explore the Undercity and discover a hidden underground lake.")
            return "Future City", ["You found a hidden underwater cave!"]
        elif choice == 4:
            print("You visit the Virtual Reality Center and experience a new world.")
            return "Future City", ["You got a VR headset!"]
    elif time_period == "Ancient Greece":
        if choice == 1:
            print("You visit the Parthenon and admire its architecture.")
            return "Ancient Greece", ["You found a piece of the Parthenon!"]
        elif choice == 2:
            print("You meet Socrates and discuss philosophy.")
            return "Ancient Greece", ["You learned a new philosophical concept!"]
        elif choice == 3:
            print("You explore the Agora and encounter a group of merchants.")
            return "Ancient Greece", ["You bought some ancient Greek goods!"]
        elif choice == 4:
            print("You visit the Theater of Dionysus and watch a play.")
            return "Ancient Greece", ["You got a theater ticket!"]
    elif time_period == "Wild West":
        if choice == 1:
            print("You visit the local saloon and order a drink.")
            return "Wild West", ["You made new friends at the saloon!"]
        elif choice == 2:
            print("You meet Wyatt Earp and discuss the law.")
            return "Wild West", ["You got a badge from Wyatt Earp!"]
        elif choice == 3:
            print("You explore the desert and encounter a rattlesnake.")
            return "Wild West", ["You escaped the rattlesnake's attack!"]
        elif choice == 4:
            print("You visit the local sheriff and discuss the town's problems.")
            return "Wild West", ["You helped the sheriff solve a case!"]

# Define the main game loop
def game_loop():
    print("Welcome to the Time Travel Adventure Game!")
    time_period = random.choice(list(time_periods.keys()))
    inventory = []
    while True:
        display_time_period(time_period)
        try:
            choice = int(input("Enter your choice: "))
            if choice < 1 or choice > len(time_periods[time_period]["options"]):
                print("Invalid choice. Please try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        time_period, items = handle_choice(time_period, choice)
        inventory.extend(items)
        print("Inventory:")
        for item in inventory:
            print(item)
        play_again = input("Do you want to continue? (yes/no): ")
        if play_again.lower() != "yes":
            break

# Run the game loop
game_loop()