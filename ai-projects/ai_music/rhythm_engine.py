"""
rhythm_engine.py - Genre-aware rhythm generation
"""
import numpy as np
from typing import List, Tuple

RHYTHMIC_PATTERNS = {
    'rock': {'fast':[0.7,0.2,0.1], 'slow':[0.4,0.3,0.3]},
    'jazz': {'fast':[0.5,0.3,0.2], 'slow':[0.3,0.4,0.3]},
    'hip hop': {'fast':[0.8,0.1,0.1], 'slow':[0.5,0.3,0.2]},
    'classical': {'fast':[0.3,0.4,0.3], 'slow':[0.2,0.3,0.5]},
    'pop': {'fast':[0.6,0.3,0.1], 'slow':[0.3,0.4,0.3]}
}

DURATIONS = [0.25, 0.5, 1.0]  # 16th, 8th, quarter
DURATION_NAMES = {0.25:'16th', 0.5:'8th', 1.0:'quarter'}

def generate_rhythmic_pattern(length: int, genre: str = 'rock', musical_style: str = 'fast') -> List[float]:
    if genre not in RHYTHMIC_PATTERNS:
        raise ValueError(f"Genre must be {list(RHYTHMIC_PATTERNS.keys())}")
    if musical_style not in RHYTHMIC_PATTERNS[genre]:
        raise ValueError(f"Style for {genre} must be {list(RHYTHMIC_PATTERNS[genre].keys())}")
    probs = RHYTHMIC_PATTERNS[genre][musical_style]
    return list(np.random.choice(DURATIONS, size=length, p=probs))

def generate_rhythm(length: int, time_signature: Tuple[int,int] = (4,4), 
                   genre: str = 'rock', musical_style: str = 'fast') -> List[Tuple[float,float,int,str]]:
    """
    Returns list of (start_time, duration, bar_number, duration_name)
    Fixed: properly handles bar overflow
    """
    pattern = generate_rhythmic_pattern(length, genre, musical_style)
    rhythm = []
    current_time = 0.0
    bar = 1
    beats_per_bar = time_signature[0]

    for dur in pattern:
        rhythm.append((current_time, dur, bar, DURATION_NAMES[dur]))
        current_time += dur
        if current_time >= beats_per_bar - 1e-6: # floating point safe
            current_time = round(current_time - beats_per_bar, 2)
            bar += 1
    return rhythm

def rhythm_to_string(rhythm: List[Tuple[float,float,int,str]]) -> str:
    out = []
    for start, dur, bar, name in rhythm:
        out.append(f"Bar {bar} @ {start:.2f}: {name} ({dur})")
    return "\n".join(out)

if __name__ == "__main__":
    r = generate_rhythm(16, genre='rock', musical_style='fast')
    print(rhythm_to_string(r))
