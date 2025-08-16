import random

def roll_dice(sides: int = 6) -> int:
    return random.randint(1, sides)

def main():
    print("Welcome to the Dice Roll Simulator!")
    while True:
        print("\nOptions:")
        print("1. Roll a standard 6-sided dice")
        print("2. Roll a custom dice")
        print("3. Roll multiple dice")
        print("4. Quit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            result = roll_dice()
            print(f"You rolled a {result}")
        elif choice == '2':
            sides = int(input("Enter the number of sides for the custom dice: "))
            result = roll_dice(sides)
            print(f"You rolled a {result} on a {sides}-sided dice")
        elif choice == '3':
            num_dice = int(input("Enter the number of dice to roll: "))
            sides = int(input("Enter the number of sides for each dice: "))
            results = [roll_dice(sides) for _ in range(num_dice)]
            print(f"You rolled: {results}")
            print(f"Total: {sum(results)}")
        elif choice == '4':
            print("Thanks for playing!")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()