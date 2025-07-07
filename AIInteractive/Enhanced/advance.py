import random

class Node:
    def __init__(self, text, options, effects=None):
        self.text = text
        self.options = options
        self.effects = effects or {}

class Character:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.traits = {}
        self.health = 100

class Game:
    def __init__(self):
        self.nodes = {
            "start": Node("You are at the start. Do you go left or right?", ["left", "right"]),
            "left": Node("You went left. You see a door. Do you open it or go back?", ["open_door", "go_back"]),
            "right": Node("You went right. You see a treasure chest. Do you open it or go back?", ["open_chest", "go_back"]),
            "open_door": Node("You opened the door. You see a room with a key. Do you take the key or leave it?", ["take_key", "leave_key"], {"take_key": "add_item"}),
            "open_chest": Node("You opened the chest. You found treasure! Congratulations!", [], {"found_treasure": True}),
            "go_back": Node("You went back to the start. Do you go left or right?", ["left", "right"]),
            "take_key": Node("You took the key. You can now unlock a secret door. Do you unlock it or go back?", ["unlock_door", "go_back"]),
            "leave_key": Node("You left the key. You can still go back.", ["go_back"]),
            "unlock_door": Node("You unlocked the door. You see a hidden room. Congratulations!", []),
        }
        self.current_node = self.nodes["start"]
        self.character = Character("Player")
        self.found_treasure = False

    def play(self):
        while True:
            print(self.current_node.text)
            if self.current_node.options:
                for i, option in enumerate(self.current_node.options):
                    print(f"{i+1}. {option}")
                choice = input("Enter your choice (number): ")
                try:
                    choice = int(choice) - 1
                    if choice < 0 or choice >= len(self.current_node.options):
                        print("Invalid choice. Please try again.")
                        continue
                    next_node_id = self.current_node.options[choice]
                    self.current_node = self.nodes[next_node_id]
                    if self.current_node.effects:
                        self.apply_effects(self.current_node.effects)
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                if self.found_treasure:
                    print("Congratulations! You won the game!")
                else:
                    print("Game over!")
                break

    def apply_effects(self, effects):
        for key, value in effects.items():
            if key == "add_item":
                self.character.inventory.append("key")
                print("You added a key to your inventory.")
            elif key == "found_treasure":
                self.found_treasure = True

    def display_character_info(self):
        print(f"Name: {self.character.name}")
        print(f"Inventory: {self.character.inventory}")
        print(f"Health: {self.character.health}")

    def game_menu(self):
        while True:
            print("Game Menu:")
            print("1. Continue playing")
            print("2. Display character info")
            print("3. Quit game")
            choice = input("Enter your choice (number): ")
            if choice == "1":
                break
            elif choice == "2":
                self.display_character_info()
            elif choice == "3":
                print("Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")

game = Game()
while True:
    game.play()
    game.game_menu()