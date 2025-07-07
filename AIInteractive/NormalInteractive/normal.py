class Node:
    def __init__(self, text, options):
        self.text = text
        self.options = options

class Game:
    def __init__(self):
        self.nodes = {
            "start": Node("You are at the start. Do you go left or right?", ["left", "right"]),
            "left": Node("You went left. You see a door. Do you open it or go back?", ["open_door", "go_back"]),
            "right": Node("You went right. You see a treasure chest. Do you open it or go back?", ["open_chest", "go_back"]),
            "open_door": Node("You opened the door. You see a room with a key. Do you take the key or leave it?", ["take_key", "leave_key"]),
            "open_chest": Node("You opened the chest. You found treasure! Congratulations!", []),
            "go_back": Node("You went back to the start. Do you go left or right?", ["left", "right"]),
            "take_key": Node("You took the key. You can now unlock a secret door. Do you unlock it or go back?", ["unlock_door", "go_back"]),
            "leave_key": Node("You left the key. You can still go back.", ["go_back"]),
            "unlock_door": Node("You unlocked the door. You see a hidden room. Congratulations!", []),
        }
        self.current_node = self.nodes["start"]

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
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                print("Game over!")
                break

game = Game()
game.play()