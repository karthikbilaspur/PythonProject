# Define the melody
melody = ['C', 'D', 'E', 'G', 'A', 'G', 'F', 'E', 'D', 'C', 'G', 'A', 'B', 'A', 'G', 'F']

# Define the chord progression
chord_progression = ['C', 'G', 'Am', 'F']

# Define the musical style (e.g., classical, jazz, pop)
musical_style = 'classical'

# Define the intervals for harmony generation
intervals = {
    'classical': [3, 5],  # major third and perfect fifth
    'jazz': [3, 5, 7],  # major third, perfect fifth, and major seventh
    'pop': [3, 5, 6]  # major third, perfect fifth, and minor sixth
}

# Function to generate harmonies
from typing import List

def generate_harmonies(melody: list[str], chord_progression: list[str], musical_style: str) -> List[List[str]]:
    harmonies: List[List[str]] = []
    intervals_to_use = intervals[musical_style]
    for note in melody:
        harmony_notes: list[str] = []
        for interval in intervals_to_use:
            harmony_note = get_harmony_note(note, interval)
            harmony_notes.append(harmony_note)
        harmonies.append(harmony_notes)
    return harmonies

# Function to get the harmony note based on the interval
def get_harmony_note(note: str, interval: int) -> str:
    note_to_index = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
    index_to_note = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}
    note_index = note_to_index[note]
    harmony_index = (note_index + interval) % 12
    harmony_note = index_to_note[harmony_index]
    return harmony_note

# Generate harmonies
harmonies = generate_harmonies(melody, chord_progression, musical_style)
for i, harmony in enumerate(harmonies):
    print(f'Melody Note: {melody[i]}, Harmony Notes: {harmony}')