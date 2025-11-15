import random

class StoryGenerator:
    def __init__(self):
        self.characters = ["Alice", "Bob", "Charlie", "David", "Emily"]
        self.locations = ["Paris", "New York", "Tokyo", "London", "Sydney"]
        self.objects = ["book", "key", "phone", "wallet", "jacket"]
        self.actions = ["found", "lost", "stole", "discovered", "hid"]
        self.adjectives = ["mysterious", "beautiful", "old", "shiny", "expensive"]

    def generate_story(self):
        character = random.choice(self.characters)
        location = random.choice(self.locations)
        object = random.choice(self.objects)
        action = random.choice(self.actions)
        adjective = random.choice(self.adjectives)

        story = f"One day, {character} was walking through {location} when they {action} a {adjective} {object}. "
        story += f"It was so {adjective} that {character} decided to keep it. "
        story += f"But little did {character} know, this {object} would change their life forever."

        return story

def main():
    generator = StoryGenerator()
    print("Welcome to the Story Generator!")
    while True:
        print("\n1. Generate a new story")
        print("2. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print(generator.generate_story())
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()