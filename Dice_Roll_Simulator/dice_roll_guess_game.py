import random

def guess_game():
    print("Welcome to the Dice Roll Guess Game!")
    sides = int(input("Enter the number of sides for the dice (default is 6): ") or 6)
    score = 0
    play_again = 'y'

    while play_again.lower() == 'y':
        user_number = int(input(f"Think of a number between 1 and {sides}. Enter your number: "))
        user_guess = input("Will the dice roll be higher or lower than your number? (h/l): ")

        roll = random.randint(1, sides)
        print(f"You rolled a {roll}!")

        if (user_guess.lower() == 'h' and roll > user_number) or (user_guess.lower() == 'l' and roll < user_number):
            print("Congratulations, you won this round!")
            score += 1
        else:
            print("Sorry, you lost this round!")

        print(f"Your current score is: {score}")
        play_again = input("Do you want to play again? (y/n): ")

    print(f"Game over! Your final score is: {score}")

def main():
    print("Dice Roll Guess Game Menu:")
    print("1. Play Game")
    print("2. Rules")
    print("3. Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        guess_game()
    elif choice == '2':
        print("Game Rules:")
        print("1. Think of a number between 1 and the number of sides on the dice.")
        print("2. Guess whether the dice roll will be higher or lower than your number.")
        print("3. If your guess is correct, you win the round!")
        main()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        main()

if __name__ == "__main__":
    main()