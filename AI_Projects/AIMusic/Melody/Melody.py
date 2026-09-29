import numpy as np
import random

# Define the scale and chord progression
scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
chord_progression = ['C', 'G', 'Am', 'F']

# Define the Markov Chain transition matrix
transition_matrix = {
    'C': {'C': 0.2, 'D': 0.3, 'E': 0.1, 'F': 0.1, 'G': 0.2, 'A': 0.05, 'B': 0.05},
    'D': {'C': 0.1, 'D': 0.2, 'E': 0.3, 'F': 0.1, 'G': 0.2, 'A': 0.05, 'B': 0.05},
    'E': {'C': 0.05, 'D': 0.2, 'E': 0.2, 'F': 0.3, 'G': 0.1, 'A': 0.1, 'B': 0.05},
    'F': {'C': 0.1, 'D': 0.1, 'E': 0.2, 'F': 0.2, 'G': 0.2, 'A': 0.1, 'B': 0.1},
    'G': {'C': 0.2, 'D': 0.1, 'E': 0.1, 'F': 0.1, 'G': 0.3, 'A': 0.1, 'B': 0.1},
    'A': {'C': 0.05, 'D': 0.1, 'E': 0.2, 'F': 0.2, 'G': 0.1, 'A': 0.3, 'B': 0.1},
    'B': {'C': 0.05, 'D': 0.05, 'E': 0.1, 'F': 0.1, 'G': 0.2, 'A': 0.2, 'B': 0.3}
}

# Function to generate a melody
def generate_melody(length: int):
    melody = [random.choice(scale)]
    for _ in range(length - 1):
        current_note = melody[-1]
        next_note = np.random.choice(list(transition_matrix[current_note].keys()), p=list(transition_matrix[current_note].values()))
        melody.append(next_note)
    return melody

# Generate a melody
melody = generate_melody(16)
print(melody)