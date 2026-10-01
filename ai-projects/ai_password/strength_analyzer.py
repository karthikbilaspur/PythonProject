"""
strength_analyzer.py - Fixed consistent return type
"""
import re
import math
import string
from typing import List, Dict

class StrengthAnalyzer:
    def check_strength(self, password: str) -> Dict:
        """Always returns Dict, not Union - consistent"""
        score = 0
        errors: List[str] = []
        feedback: List[str] = []

        # Length
        if len(password) < 8:
            errors.append("Password should be at least 8 characters")
        else:
            score += 1
            if len(password) >= 12:
                score += 1
                feedback.append("Good length")

        # Lowercase
        if not re.search("[a-z]", password):
            errors.append("Add at least one lowercase letter")
        else:
            score += 1

        # Uppercase
        if not re.search("[A-Z]", password):
            errors.append("Add at least one uppercase letter")
        else:
            score += 1

        # Number
        if not re.search("[0-9]", password):
            errors.append("Add at least one number")
        else:
            score += 1

        # Special
        if not re.search("[^A-Za-z0-9]", password):
            errors.append("Add at least one special character")
        else:
            score += 1

        # Entropy
        charset_size = 0
        if re.search("[a-z]", password): charset_size += 26
        if re.search("[A-Z]", password): charset_size += 26
        if re.search("[0-9]", password): charset_size += 10
        if re.search("[^A-Za-z0-9]", password): charset_size += 32
        entropy = len(password) * math.log2(charset_size) if charset_size else 0

        # Label
        if score >= 6:
            label = "Very Strong"
        elif score >= 5:
            label = "Strong"
        elif score >= 3:
            label = "Medium"
        else:
            label = "Weak"

        return {
            "password": password,
            "score": score,
            "max_score": 6,
            "label": label,
            "entropy_bits": round(entropy, 1),
            "crack_time": self._estimate_crack_time(entropy),
            "errors": errors,
            "feedback": feedback,
            "length": len(password)
        }

    def _estimate_crack_time(self, entropy: float) -> str:
        # Very rough estimate at 1B guesses/sec
        guesses = 2 ** entropy
        seconds = guesses / 1e9
        if seconds < 60: return f"{seconds:.1f} seconds"
        if seconds < 3600: return f"{seconds/60:.1f} minutes"
        if seconds < 86400: return f"{seconds/3600:.1f} hours"
        if seconds < 31536000: return f"{seconds/86400:.1f} days"
        return f"{seconds/31536000:.1f} years"

if __name__ == "__main__":
    analyzer = StrengthAnalyzer()
    print(analyzer.check_strength("P@ssw0rd!"))
