import random

def game():
    choices = ['rock', 'paper', 'scissors', 'lizard', 'spock']
    beats = {
        'rock': ['scissors', 'lizard'],
        'paper': ['rock', 'spock'],
        'scissors': ['paper', 'lizard'],
        'lizard': ['paper', 'spock'],
        'spock': ['rock', 'scissors']
    }

    print("Welcome to Rock Paper Scissors Lizard Spock!")
    while True:
        user_choice = input("Enter your choice (rock, paper, scissors, lizard, spock) or 'q' to quit: ").lower()
        if user_choice == 'q':
            break
        if user_choice not in choices:
            print("Invalid choice. Please try again.")
            continue

        computer_choice = random.choice(choices)
        print(f"\nYou chose: {user_choice}")
        print(f"Computer chose: {computer_choice}\n")

        if user_choice == computer_choice:
            print("It's a tie!")
        elif computer_choice in beats[user_choice]:
            print("You win!")
        else:
            print("Computer wins!")

if __name__ == "__main__":
    game()