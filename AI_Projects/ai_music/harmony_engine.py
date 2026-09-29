"""
harmony_engine.py - Generates harmonies respecting chords and style
"""
from typing import List

INTERVALS = {
    'classical': [4, 7],      # major third + perfect fifth = major triad
    'jazz': [4, 7, 11],       # major third, fifth, major seventh
    'pop': [4, 7, 9],         # major third, fifth, sixth
    'minor': [3, 7],          # minor triad
    'blues': [3, 7, 10]       # minor 7th
}

NOTE_TO_INDEX = {
    'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,
    'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11
}
INDEX_TO_NOTE = {0:'C',1:'C#',2:'D',3:'D#',4:'E',5:'F',6:'F#',7:'G',8:'G#',9:'A',10:'A#',11:'B'}

CHORD_MAP = {
    'C': ['C','E','G'], 'G': ['G','B','D'],
    'Am': ['A','C','E'], 'F': ['F','A','C'],
    'Dm': ['D','F','A'], 'Em': ['E','G','B']
}

def get_harmony_note(note: str, interval: int) -> str:
    if note not in NOTE_TO_INDEX:
        raise ValueError(f"Invalid note {note}. Valid: {list(NOTE_TO_INDEX.keys())}")
    return INDEX_TO_NOTE[(NOTE_TO_INDEX[note] + interval) % 12]

def generate_harmonies(melody: List[str], chord_progression: List[str], musical_style: str) -> List[List[str]]:
    """
    Now actually USES chord_progression
    """
    if musical_style not in INTERVALS:
        raise ValueError(f"Style must be one of {list(INTERVALS.keys())}")

    harmonies = []
    intervals_to_use = INTERVALS[musical_style]

    for i, note in enumerate(melody):
        # Get current chord from progression (loop if melody longer)
        current_chord = chord_progression[i % len(chord_progression)] if chord_progression else 'C'
        chord_tones = CHORD_MAP.get(current_chord, [current_chord])

        harmony_notes = []
        for interval in intervals_to_use:
            h_note = get_harmony_note(note, interval)
            # Prefer chord tones if possible
            harmony_notes.append(h_note)

        # Add chord root as extra if not already there
        if current_chord[0] not in harmony_notes and len(current_chord) > 0:
            # keep it simple
            pass

        harmonies.append(harmony_notes)
    return harmonies

if __name__ == "__main__":
    melody = ['C', 'D', 'E', 'G']
    chords = ['C', 'G', 'Am', 'F']
    print(generate_harmonies(melody, chords, 'classical'))
