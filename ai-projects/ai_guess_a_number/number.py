import random
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

STATS_FILE = Path(__file__).parent / "guess_stats.json"

@dataclass
class Difficulty:
    name: str
    upper: int
    max_tries: int # for human-guess mode

DIFFICULTIES = {
    'easy': Difficulty('easy', 50, 10),
    'medium': Difficulty('medium', 75, 8),
    'hard': Difficulty('hard', 100, 7),
    'insane': Difficulty('insane', 500, 10)
}

@dataclass
class GameStats:
    mode: str
    difficulty: str
    guesses: int
    won: bool
    date: str

class StatsManager:
    def __init__(self, path=STATS_FILE):
        self.path = path
        self.history: List[dict] = self._load()

    def _load(self):
        if self.path.exists():
            try: return json.loads(self.path.read_text())
            except: return []
        return []

    def add(self, stat: GameStats):
        self.history.append(asdict(stat))
        self.path.write_text(json.dumps(self.history, indent=2))

    def summary(self):
        if not self.history: return "No games yet."
        total = len(self.history)
        wins = sum(1 for h in self.history if h['won'])
        avg = sum(h['guesses'] for h in self.history) / total
        best = min((h for h in self.history if h['won']), key=lambda x: x['guesses'], default=None)
        s = f"\n--- STATS ---\nGames: {total} | Wins: {wins} | Avg guesses: {avg:.1f}"
        if best: s += f"\nBest: {best['guesses']} guesses ({best['mode']}/{best['difficulty']})"
        return s

class GuessANumber:
    def __init__(self):
        self.stats = StatsManager()

    # ---------- MODE 1: COMPUTER GUESSES YOUR NUMBER ----------
    def computer_guesses(self, diff: Difficulty):
        low, high = 1, diff.upper
        guesses = 0
        history = [] # for undo

        print(f"\n[MODE 1] Think of a number 1-{high}. I will guess it.")
        input("Press ENTER when ready...")

        while low <= high:
            guess = (low + high) // 2
            guesses += 1
            print(f"\nMy guess #{guesses}: {guess} (range {low}-{high})")

            fb = input("Is it [h]igher, [l]ower, [c]orrect, [u]ndo? ").strip().lower()

            if fb == 'u':
                if history:
                    low, high, guesses = history.pop()
                    guesses -= 1
                    print(f"Undone. Back to range {low}-{high}")
                    continue
                else:
                    print("Nothing to undo.")
                    guesses -= 1
                    continue

            if fb not in ('h','l','c','higher','lower','correct'):
                print("Use h / l / c / u")
                guesses -= 1
                continue

            fb = fb[0]
            history.append((low, high, guesses))

            if fb == 'h': low = guess + 1
            elif fb == 'l': high = guess - 1
            else:
                print(f"Got it in {guesses} guesses! Optimal would be ~{diff.upper.bit_length()} guesses.")
                self.stats.add(GameStats("computer_guesses", diff.name, guesses, True, datetime.now().isoformat()))
                return

        print("Inconsistent hints! You changed your number?")
        self.stats.add(GameStats("computer_guesses", diff.name, guesses, False, datetime.now().isoformat()))

    # ---------- MODE 2: YOU GUESS COMPUTER'S NUMBER ----------
    def human_guesses(self, diff: Difficulty):
        secret = random.randint(1, diff.upper)
        tries_left = diff.max_tries
        print(f"\n[MODE 2] I picked a number 1-{diff.upper}. You have {tries_left} tries.")

        for attempt in range(1, tries_left + 1):
            try:
                g = int(input(f"Try {attempt}/{tries_left} > "))
            except ValueError:
                print("Enter a number!")
                continue

            if g == secret:
                print(f"Correct! It was {secret}. You won in {attempt} tries.")
                self.stats.add(GameStats("human_guesses", diff.name, attempt, True, datetime.now().isoformat()))
                return
            elif g < secret:
                print(f"Too low! {'Almost there!' if secret - g < 10 else ''}")
            else:
                print(f"Too high! {'Close!' if g - secret < 10 else ''}")

        print(f"Out of tries! My number was {secret}.")
        self.stats.add(GameStats("human_guesses", diff.name, tries_left, False, datetime.now().isoformat()))

    def get_difficulty(self):
        print("\nDifficulties: easy(1-50), medium(1-75), hard(1-100), insane(1-500)")
        choice = input("Choose [hard]: ").strip().lower() or 'hard'
        return DIFFICULTIES.get(choice, DIFFICULTIES['hard'])

    def play(self):
        while True:
            print("\n==== GUESS A NUMBER 2x ====")
            print("1. Computer guesses your number (binary search)")
            print("2. You guess computer's number")
            print("3. View stats")
            print("4. Quit")
            c = input("> ").strip()

            if c == '1':
                self.computer_guesses(self.get_difficulty())
            elif c == '2':
                self.human_guesses(self.get_difficulty())
            elif c == '3':
                print(self.stats.summary())
            elif c == '4':
                print("Bye! Stats saved to", STATS_FILE)
                break
            else:
                print("Pick 1-4")

def main():
    GuessANumber().play()

if __name__ == "__main__":
    main()