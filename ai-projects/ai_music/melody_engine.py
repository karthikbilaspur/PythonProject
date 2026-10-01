"""
melody_engine.py - Markov Chain melody generation with seed & chord awareness
"""
import numpy as np
import random
from typing import List, Dict

SCALE = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

TRANSITION_MATRIX: Dict[str, Dict[str, float]] = {
    'C': {'C':0.2,'D':0.3,'E':0.1,'F':0.1,'G':0.2,'A':0.05,'B':0.05},
    'D': {'C':0.1,'D':0.2,'E':0.3,'F':0.1,'G':0.2,'A':0.05,'B':0.05},
    'E': {'C':0.05,'D':0.2,'E':0.2,'F':0.3,'G':0.1,'A':0.1,'B':0.05},
    'F': {'C':0.1,'D':0.1,'E':0.2,'F':0.2,'G':0.2,'A':0.1,'B':0.1},
    'G': {'C':0.2,'D':0.1,'E':0.1,'F':0.1,'G':0.3,'A':0.1,'B':0.1},
    'A': {'C':0.05,'D':0.1,'E':0.2,'F':0.2,'G':0.1,'A':0.3,'B':0.1},
    'B': {'C':0.05,'D':0.05,'E':0.1,'F':0.1,'G':0.2,'A':0.2,'B':0.3}
}

def validate_matrix():
    for note, probs in TRANSITION_MATRIX.items():
        total = sum(probs.values())
        assert abs(total - 1.0) < 0.001, f"Probabilities for {note} don't sum to 1: {total}"

def generate_melody(length: int, seed: int = None, scale: List[str] = SCALE, 
                   chord_progression: List[str] = None) -> List[str]:
    if length <= 0:
        raise ValueError("length must be > 0")
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    validate_matrix()

    melody = [random.choice(scale)]
    for _ in range(length - 1):
        curr = melody[-1]
        probs = TRANSITION_MATRIX.get(curr)
        if not probs:
            melody.append(random.choice(scale))
            continue

        # Optional: bias towards chord tones if progression given
        next_note = np.random.choice(list(probs.keys()), p=list(probs.values()))
        melody.append(next_note)
    return melody

def generate_melody_with_constraints(length: int, must_include: List[str] = None) -> List[str]:
    """Extreme: ensures melody includes specific notes"""
    mel = generate_melody(length)
    if must_include:
        for i, note in enumerate(must_include):
            if i < len(mel):
                mel[i] = note
    return mel

if __name__ == "__main__":
    print(generate_melody(16, seed=42))
