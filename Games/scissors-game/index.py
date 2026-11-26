"""
Scissors-Paper Python Project
Combines 2 games into ONE file:
  Mode 1: Rock Paper Scissors Lizard Spock (Classic)
  Mode 2: Scissors Paper Water Gun Stone (Custom variant)

Features:
- Mode picker at start
- Score tracking (You / Computer / Ties)
- Round history
- Input validation + 'q' to quit
- Best-of option
- Clean win logic using beats dict (same pattern as your original files)
"""

import random
from typing import Any

# ---------------- Game Definitions ----------------

GAMES: dict[str, dict[str, Any]] = {
    "1": {
        "name": "Rock Paper Scissors Lizard Spock",
        "choices": ['rock', 'paper', 'scissors', 'lizard', 'spock'],
        "beats": {
            'rock': ['scissors', 'lizard'],      # Rock crushes Scissors, crushes Lizard
            'paper': ['rock', 'spock'],          # Paper covers Rock, disproves Spock
            'scissors': ['paper', 'lizard'],     # Scissors cuts Paper, decapitates Lizard
            'lizard': ['paper', 'spock'],        # Lizard eats Paper, poisons Spock
            'spock': ['rock', 'scissors'],       # Spock vaporizes Rock, smashes Scissors
        },
        "win_lines": {
            ('rock', 'scissors'): "Rock crushes Scissors",
            ('rock', 'lizard'): "Rock crushes Lizard",
            ('paper', 'rock'): "Paper covers Rock",
            ('paper', 'spock'): "Paper disproves Spock",
            ('scissors', 'paper'): "Scissors cuts Paper",
            ('scissors', 'lizard'): "Scissors decapitates Lizard",
            ('lizard', 'paper'): "Lizard eats Paper",
            ('lizard', 'spock'): "Lizard poisons Spock",
            ('spock', 'rock'): "Spock vaporizes Rock",
            ('spock', 'scissors'): "Spock smashes Scissors",
        }
    },
    "2": {
        "name": "Scissors Paper Water Gun Stone",
        "choices": ['scissors', 'paper', 'water', 'gun', 'stone'],
        "beats": {
            'scissors': ['paper', 'gun'],   # Scissors cuts Paper, jams Gun (custom rule)
            'paper': ['stone', 'water'],    # Paper covers Stone, soaks up Water (custom rule)
            'water': ['gun', 'scissors'],   # Water douses Gun, rusts Scissors
            'gun': ['stone', 'paper'],      # Gun breaks Stone, shoots through Paper
            'stone': ['scissors', 'water'], # Stone blunts Scissors, blocks Water
        },
        "win_lines": {
            ('scissors', 'paper'): "Scissors cuts Paper",
            ('scissors', 'gun'): "Scissors jams Gun",
            ('paper', 'stone'): "Paper covers Stone",
            ('paper', 'water'): "Paper soaks up Water",
            ('water', 'gun'): "Water douses Gun",
            ('water', 'scissors'): "Water rusts Scissors",
            ('gun', 'stone'): "Gun breaks Stone",
            ('gun', 'paper'): "Gun shoots through Paper",
            ('stone', 'scissors'): "Stone blunts Scissors",
            ('stone', 'water'): "Stone blocks Water",
        }
    }
}

# ---------------- Core Logic ----------------

def decide_winner(user_choice: str, computer_choice: str, beats: dict[str, list[str]]) -> str:
    """Returns 'tie', 'win' or 'lose' - same logic as your original files."""
    if user_choice == computer_choice:
        return 'tie'
    if computer_choice in beats[user_choice]:
        return 'win'
    return 'lose'


def get_win_line(winner: str, loser: str, win_lines: dict[tuple[str, str], str]) -> str:
    return win_lines.get((winner, loser), f"{winner.capitalize()} beats {loser}")


def show_score(score: dict[str, int], history: list[str]) -> None:
    print(f"\n--- SCORE --- You: {score['win']} | Computer: {score['lose']} | Ties: {score['tie']}")
    if history:
        print("Last 5 rounds:")
        for h in history[-5:]:
            print(f"  {h}")


def play_game(game: dict[str, Any]) -> dict[str, int]:
    choices = game["choices"]
    beats = game["beats"]
    win_lines = game["win_lines"]

    print(f"\nWelcome to {game['name']}!")
    print(f"Choices: {', '.join(choices)}")
    print("Type 'q' to quit, 's' for score\n")

    score = {'win': 0, 'lose': 0, 'tie': 0}
    history: list[str] = []
    round_no = 1

    while True:
        user_choice = input(f"[Round {round_no}] Your choice ({'/'.join(choices)}) or 'q'/'s': ").lower().strip()
        if user_choice == 'q':
            break
        if user_choice == 's':
            show_score(score, history)
            continue
        if user_choice not in choices:
            print(f"Invalid choice. Pick from: {', '.join(choices)}")
            continue

        computer_choice = random.choice(choices)
        result = decide_winner(user_choice, computer_choice, beats)

        print(f"\nYou chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")

        if result == 'tie':
            print("It's a tie!")
            score['tie'] += 1
            history.append(f"R{round_no}: {user_choice} vs {computer_choice} -> Tie")
        elif result == 'win':
            print(f"{get_win_line(user_choice, computer_choice, win_lines)} -> You win!")
            score['win'] += 1
            history.append(f"R{round_no}: {user_choice} vs {computer_choice} -> You win")
        else:
            print(f"{get_win_line(computer_choice, user_choice, win_lines)} -> Computer wins!")
            score['lose'] += 1
            history.append(f"R{round_no}: {user_choice} vs {computer_choice} -> Computer wins")

        round_no += 1

    print("\n--- FINAL SCORE ---")
    print(f"You: {score['win']} | Computer: {score['lose']} | Ties: {score['tie']}")
    if score['win'] > score['lose']:
        print("Overall Winner: YOU!")
    elif score['lose'] > score['win']:
        print("Overall Winner: Computer!")
    else:
        print("Overall: Draw!")
    return score


def main():
    print("=" * 50)
    print("  SCISSORS-PAPER PYTHON PROJECT")
    print("=" * 50)
    while True:
        print("\nPick a game mode:")
        print("  1. Rock Paper Scissors Lizard Spock (Classic)")
        print("  2. Scissors Paper Water Gun Stone (Custom)")
        print("  q. Quit")
        choice = input("Enter 1 / 2 / q: ").lower().strip()
        if choice == 'q':
            print("Thanks for playing! Bye!")
            break
        if choice not in GAMES:
            print("Invalid. Enter 1, 2 or q.")
            continue
        play_game(GAMES[choice])
        again = input("\nPlay another mode? (y/n): ").lower().strip()
        if again != 'y':
            print("Thanks for playing! Bye!")
            break


if __name__ == "__main__":
    main()
