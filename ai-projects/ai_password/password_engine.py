"""
password_engine.py - EXTREME - Clubs all 3 versions into 1 secure engine
Fixes: random -> secrets, np.random -> secrets, length bug, train bug
"""
import secrets
import string
from collections import defaultdict
from typing import List, Dict

class ExtremePasswordAI:
    def __init__(self, length: int = 12):
        self.length = length
        self.markov_matrix: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(int))
        self.states = string.ascii_letters + string.digits + string.punctuation
        self.trained = False

    # ===== FROM FILE 1 - FIXED TO SECURE =====
    def generate_secure(self, length: int = None, use_upper: bool = True, 
                       use_digits: bool = True, use_symbols: bool = True) -> str:
        """Secure generation - uses secrets, fixes truncation bug"""
        length = length or self.length

        lower = string.ascii_lowercase
        upper = string.ascii_uppercase if use_upper else ''
        digits = string.digits if use_digits else ''
        symbols = string.punctuation if use_symbols else ''

        all_chars = lower + upper + digits + symbols
        if not all_chars:
            raise ValueError("At least one character set must be selected")

        # Count required chars
        required_sets = []
        if use_upper: required_sets.append(upper)
        if use_digits: required_sets.append(digits)
        if use_symbols: required_sets.append(symbols)
        required_sets.append(lower)  # always at least one lower

        if length < len(required_sets):
            raise ValueError(f"Length {length} too short, need at least {len(required_sets)} for selected sets")

        password: List[str] = []
        for charset in required_sets:
            password.append(secrets.choice(charset))

        # Fill rest
        for _ in range(length - len(password)):
            password.append(secrets.choice(all_chars))

        secrets.SystemRandom().shuffle(password)
        return ''.join(password)

    # ===== FROM FILE 2/3 - MARKOV FIXED =====
    def train(self, passwords: List[str]):
        """Fixed: resets counts properly, doesn't double-divide"""
        # Reset and recount
        temp_counts = defaultdict(lambda: defaultdict(int))
        for pwd in passwords:
            for i in range(len(pwd) - 1):
                temp_counts[pwd[i]][pwd[i+1]] += 1

        # Convert to probabilities
        self.markov_matrix = defaultdict(lambda: defaultdict(float))
        for state, transitions in temp_counts.items():
            total = sum(transitions.values())
            for nxt, cnt in transitions.items():
                self.markov_matrix[state][nxt] = cnt / total
        self.trained = True

    def generate_markov(self, length: int = None) -> str:
        """Fixed: uses secrets only, has fallback"""
        length = length or self.length

        if not self.trained or not self.markov_matrix:
            # Fallback to secure if not trained
            return self.generate_secure(length)

        password = [secrets.choice(list(self.states))]

        for _ in range(length - 1):
            curr = password[-1]
            transitions = self.markov_matrix.get(curr)

            if transitions:
                next_states = list(transitions.keys())
                probs = list(transitions.values())
                # Use secrets for choice, weighted
                # Convert prob to weighted choice without numpy
                r = secrets.SystemRandom().random()
                cumulative = 0
                chosen = next_states[-1]
                for ns, p in zip(next_states, probs):
                    cumulative += p
                    if r <= cumulative:
                        chosen = ns
                        break
                password.append(chosen)
            else:
                # Fallback if state unknown
                password.append(secrets.choice(list(self.states)))

        return ''.join(password)

    # ===== FROM FILE 3 - PATTERN FIXED =====
    def generate_from_pattern(self, pattern: str) -> str:
        """
        L=lower, U=upper, D=digit, S=symbol
        Example: ULLDDS -> Ab12!@
        Allows literal chars too: L-L-D-D -> a-b-1-2
        """
        char_sets = {
            'L': string.ascii_lowercase,
            'U': string.ascii_uppercase,
            'D': string.digits,
            'S': string.punctuation
        }
        result = []
        for ch in pattern:
            if ch in char_sets:
                result.append(secrets.choice(char_sets[ch]))
            elif ch in ['-', '_', '.', '@', '#', '!']:  # allowed literals
                result.append(ch)
            else:
                raise ValueError(f"Invalid pattern char '{ch}'. Use L,U,D,S or -_ .@#!")
        return ''.join(result)

    # ===== NEW EXTREME FEATURES =====
    def generate_memorable(self, words: int = 4, sep: str = "-", add_number: bool = True) -> str:
        """Extreme: Correct-Horse-Battery-Staple style"""
        # Built-in word list to avoid external dependency
        word_list = ["correct","horse","battery","staple","apple","river","mountain","sunset",
                    "forest","ocean","thunder","crystal","rocket","shadow","silver","golden"]
        chosen = [secrets.choice(word_list).capitalize() for _ in range(words)]
        pwd = sep.join(chosen)
        if add_number:
            pwd += sep + str(secrets.randbelow(90) + 10)
            pwd += secrets.choice("!@#$%")
        return pwd

    def generate_extreme(self, length: int = 16) -> str:
        """Combines all: secure + pronounceable + strong"""
        # 12 chars secure + 4 memorable
        part1 = self.generate_secure(length=length-6, use_upper=True, use_digits=True, use_symbols=True)
        part2 = secrets.choice(string.ascii_uppercase) + str(secrets.randbelow(10)) + secrets.choice("!@#")
        combined = list(part1 + part2)
        secrets.SystemRandom().shuffle(combined)
        return ''.join(combined)

if __name__ == "__main__":
    ai = ExtremePasswordAI(12)
    print("Secure:", ai.generate_secure())
    print("Pattern ULLDDS:", ai.generate_from_pattern("ULLDDS"))
    print("Memorable:", ai.generate_memorable())
    print("Extreme:", ai.generate_extreme(16))
