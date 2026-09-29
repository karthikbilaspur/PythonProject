"""
composer.py - EXTREME - Clubs all 3 engines into a full composition
This is the file that does what you asked: club all in 3 but keep separate
"""
from melody_engine import generate_melody
from harmony_engine import generate_harmonies
from rhythm_engine import generate_rhythm
from typing import List, Dict
import json

class ExtremeComposer:
    def __init__(self, time_signature=(4,4), chord_progression=None):
        self.time_signature = time_signature
        self.chord_progression = chord_progression or ['C','G','Am','F']

    def compose(self, length: int = 16, musical_style: str = 'classical', 
               genre: str = 'rock', rhythm_style: str = 'fast', seed: int = None) -> List[Dict]:
        """
        Full pipeline: melody -> harmony -> rhythm -> song
        """
        melody = generate_melody(length, seed=seed, chord_progression=self.chord_progression)
        harmonies = generate_harmonies(melody, self.chord_progression, musical_style)
        rhythm = generate_rhythm(length, self.time_signature, genre, rhythm_style)

        song = []
        for i in range(length):
            start, duration, bar, dur_name = rhythm[i]
            song.append({
                "beat": i+1,
                "bar": bar,
                "start_time": start,
                "duration": duration,
                "duration_name": dur_name,
                "melody_note": melody[i],
                "harmony_notes": harmonies[i],
                "chord": self.chord_progression[i % len(self.chord_progression)]
            })
        return song

    def export_midi_like(self, song: List[Dict], filename: str = "composition.json"):
        """Export to JSON (can be converted to MIDI later with mido)"""
        with open(filename, "w") as f:
            json.dump(song, f, indent=2)
        print(f"Exported {len(song)} notes to {filename}")
        return filename

    def print_score(self, song: List[Dict]):
        print(f"\n{'Bar':<4} {'Start':<6} {'Dur':<8} {'Melody':<7} {'Harmony':<15} {'Chord'}")
        print("-"*60)
        for n in song:
            print(f"{n['bar']:<4} {n['start_time']:<6} {n['duration_name']:<8} {n['melody_note']:<7} {','.join(n['harmony_notes']):<15} {n['chord']}")

if __name__ == "__main__":
    composer = ExtremeComposer()
    song = composer.compose(length=16, musical_style='classical', genre='rock', seed=42)
    composer.print_score(song)
    composer.export_midi_like(song)
