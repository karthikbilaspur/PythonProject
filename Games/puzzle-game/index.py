import random
import sys
from typing import Callable, TypedDict


class Puzzle(TypedDict):
    prompt: str
    answer: str
    hint: str
    check: Callable[[str], bool]

WORDS = ["hello", "world", "python", "cipher", "puzzle", "secret",
         "galaxy", "rocket", "garden", "silver", "planet", "wizard",
         "bridge", "candle", "forest", "harbour", "lantern", "marble"]

# word -> ALL valid anagrams (not just one, and correctly paired)
ANAGRAMS = {
    "listen": ["silent", "enlist", "tinsel"],
    "acts": ["cats", "cast", "scat"],
    "weird": ["wired", "widder"],  # "widder" is obscure; keep "wired" primary
    "dusty": ["study"],
    "night": ["thing"],
    "loop": ["pool", "polo"],
    "evil": ["vile", "live", "veil"],
    "below": ["elbow", "bowel"],
    "state": ["taste"],
    "inch": ["chin"],
    "strain": ["trains", "satin", "saint"],
}


def _is_anagram(a: str, b: str) -> bool:
    """True if a and b use exactly the same letters (case-insensitive)."""
    a, b = a.strip().lower(), b.strip().lower()
    return len(a) == len(b) and sorted(a) == sorted(b) and a != b


class CryptoMind:
    def __init__(self):
        self.score = 0
        self.streak = 0
        self.played = 0
        # FIX: dispatch table is now actually used by play().
        self.puzzles: dict[str, tuple[str, Callable[[], Puzzle]]] = {
            "1": ("Caesar Cipher", self.caesar_cipher),
            "2": ("Vigenere Cipher", self.vigenere_cipher),
            "3": ("Word Scramble", self.word_scramble),
            "4": ("Anagram", self.anagram),
        }

    # ---------- Puzzle generators (each returns a dict) ----------
    def caesar_cipher(self) -> Puzzle:
        shift = random.randint(1, 25)  # was 1-10: too narrow, too easy
        word = random.choice(WORDS)
        encrypted = "".join(
            chr((ord(c) - 97 + shift) % 26 + 97) for c in word
        )
        return {
            "prompt": f"Decrypt the word: {encrypted}  (shift = ?)",
            "answer": word,
            "hint": f"Hint: shift is {shift} (each letter moved {shift} forward).",
            "check": lambda ans: ans.strip().lower() == word,
        }

    def vigenere_cipher(self) -> Puzzle:
        keyword = random.choice(["secret", "code", "cipher", "key", "puzzle", "magic"])
        word = random.choice(WORDS)
        encrypted, ki = "", 0
        for char in word:
            shift = ord(keyword[ki % len(keyword)]) - 97
            encrypted += chr((ord(char) - 97 + shift) % 26 + 97)
            ki += 1
        return {
            # FIX: tell the player the keyword, otherwise unsolvable.
            "prompt": f"Decrypt the word: {encrypted}  (keyword = '{keyword}')",
            "answer": word,
            "hint": f"Hint: keyword is '{keyword}'. Subtract each keyword letter's shift.",
            "check": lambda ans: ans.strip().lower() == word,
        }

    def word_scramble(self) -> Puzzle:
        word = random.choice(WORDS)
        # FIX: keep shuffling until scrambled != original.
        for _ in range(50):
            letters = list(word)
            random.shuffle(letters)
            scrambled = "".join(letters)
            if scrambled != word:
                break
        else:
            scrambled = word[::-1]  # fallback for words like "aaa"
        return {
            "prompt": f"Unscramble the word: {scrambled}",
            "answer": word,
            "hint": f"Hint: it starts with '{word[0]}' and has {len(word)} letters.",
            "check": lambda ans: ans.strip().lower() == word,
        }

    def anagram(self) -> Puzzle:
        word = random.choice(list(ANAGRAMS.keys()))
        valid = ANAGRAMS[word]
        return {
            "prompt": f"Find an anagram of: {word}  (any valid one counts)",
            "answer": valid[0],
            "hint": f"Hint: one answer is '{valid[0]}'.",
            # FIX: accept ANY anagram, not one randomly-picked string.
            # Also reject the word itself: "listen" is not an anagram of "listen".
            "check": lambda ans: _is_anagram(ans, word),
        }

    # ---------- Game loop ----------
    def _ask(self, puzzle: Puzzle) -> None:
        print(f"\n{puzzle['prompt']}")
        print("Type 'hint' for a hint, or 'quit' to stop this round.")
        try:
            answer = input("Enter your answer: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)
        answer = answer.strip()
        if answer.lower() == "quit":
            return
        if answer.lower() == "hint":
            print(puzzle["hint"])
            try:
                answer = input("Enter your answer: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                sys.exit(0)

        self.played += 1
        if puzzle["check"](answer):
            self.score += 1
            self.streak += 1
            print(f"Correct!  Score: {self.score}  |  Streak: {self.streak}")
        else:
            self.streak = 0
            # For anagrams, show all valid answers, not one arbitrary one.
            if "anagram" in puzzle["prompt"].lower():
                word = puzzle["prompt"].split(":")[-1].strip().split()[0]
                all_valid = ANAGRAMS.get(word, [puzzle["answer"]])
                print(f"Sorry, valid answers were: {', '.join(all_valid)}.")
            else:
                print(f"Sorry, the correct answer is '{puzzle['answer']}'.")
            print(f"Score: {self.score}  |  Streak reset.")

    def play(self):
        print("Welcome to CryptoMind!")
        print("Solve ciphers, scrambles and anagrams. Type 'hint' if stuck.")
        while True:
            print(f"\n--- Score: {self.score} | Streak: {self.streak} | Played: {self.played} ---")
            print("Choose a puzzle type:")
            for key, (name, _) in self.puzzles.items():
                print(f"{key}. {name}")
            print("5. Quit")
            try:
                choice = input("Enter your choice: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            if choice == "5":
                print(f"\nFinal score: {self.score}/{self.played}. Thanks for playing!")
                break
            if choice in self.puzzles:
                _, generator = self.puzzles[choice]
                self._ask(generator())
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    CryptoMind().play()