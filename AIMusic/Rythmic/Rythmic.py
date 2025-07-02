import numpy as np

# Define the time signature
time_signature = (4, 4)  # 4/4 time

# Define the genre (e.g., rock, jazz, hip hop)
genre = 'rock'

# Define the musical style (e.g., fast, slow, complex)
musical_style = 'fast'

# Define the probability distributions for rhythmic patterns
rhythmic_patterns = {
    'rock': {
        'fast': [0.7, 0.2, 0.1],  # probability of 16th note, 8th note, quarter note
        'slow': [0.4, 0.3, 0.3]
    },
    'jazz': {
        'fast': [0.5, 0.3, 0.2],
        'slow': [0.3, 0.4, 0.3]
    },
    'hip hop': {
        'fast': [0.8, 0.1, 0.1],
        'slow': [0.5, 0.3, 0.2]
    }
}

# Function to generate rhythmic pattern
from typing import List

def generate_rhythmic_pattern(length: int) -> List[float]:
    pattern: List[float] = []
    probabilities = rhythmic_patterns[genre][musical_style]
    for _ in range(length):
        note_length = np.random.choice([0.25, 0.5, 1], p=probabilities)  # 16th note, 8th note, quarter note
        pattern.append(note_length)
    return pattern

# Function to generate rhythm
from typing import List, Tuple

def generate_rhythm(length: int) -> List[Tuple[float, float]]:
    rhythm: List[Tuple[float, float]] = []
    pattern = generate_rhythmic_pattern(length)
    current_time = 0
    for note_length in pattern:
        rhythm.append((current_time, note_length))
        current_time += note_length
        if current_time >= time_signature[0]:
            current_time -= time_signature[0]
    return rhythm

# Generate rhythm
rhythm = generate_rhythm(16)
for note in rhythm:
    print(f'Start Time: {note[0]}, Note Length: {note[1]}')