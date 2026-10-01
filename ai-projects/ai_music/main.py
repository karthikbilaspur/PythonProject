"""
main.py - CLI for Extreme Music AI
"""
from composer import ExtremeComposer
from melody_engine import generate_melody
from harmony_engine import generate_harmonies
from rhythm_engine import generate_rhythm, rhythm_to_string

def banner():
    print("""
    ╔═══════════════════════════════════════╗
    ║  EXTREME MUSIC AI - 3 ENGINES CLUBBED ║
    ║  Melody + Harmony + Rhythm Composer   ║
    ╚═══════════════════════════════════════╝
    """)

def main():
    banner()
    composer = ExtremeComposer()

    while True:
        print("\n--- MENU ---")
        print("1. Generate Melody only (Markov)")
        print("2. Generate Harmony only")
        print("3. Generate Rhythm only")
        print("4. COMPOSE FULL SONG [EXTREME]")
        print("5. Change chord progression")
        print("6. Exit")

        choice = input("> ").strip()

        if choice == "1":
            length = int(input("Length [16]: ") or 16)
            seed = input("Seed or blank: ").strip()
            seed = int(seed) if seed else None
            mel = generate_melody(length, seed=seed)
            print(f"Melody: {mel}")

        elif choice == "2":
            mel_input = input("Melody notes comma separated (C,D,E,G): ").strip()
            melody = [n.strip() for n in mel_input.split(",")] if mel_input else ['C','D','E','G']
            chords = ['C','G','Am','F']
            style = input("Style classical/jazz/pop/minor [classical]: ") or 'classical'
            harms = generate_harmonies(melody, chords, style)
            for m,h in zip(melody, harms):
                print(f"Melody {m} -> Harmony {h}")

        elif choice == "3":
            length = int(input("Length [16]: ") or 16)
            genre = input("Genre rock/jazz/hip hop/pop/classical [rock]: ") or 'rock'
            style = input("Style fast/slow [fast]: ") or 'fast'
            rhy = generate_rhythm(length, genre=genre, musical_style=style)
            print(rhythm_to_string(rhy))

        elif choice == "4":
            length = int(input("Length [16]: ") or 16)
            m_style = input("Harmonic style classical/jazz/pop/minor/blues [classical]: ") or 'classical'
            genre = input("Rhythmic genre rock/jazz/hip hop/pop [rock]: ") or 'rock'
            r_style = input("Rhythmic speed fast/slow [fast]: ") or 'fast'
            seed_input = input("Seed or blank: ").strip()
            seed = int(seed_input) if seed_input else None

            song = composer.compose(length=length, musical_style=m_style, genre=genre, rhythm_style=r_style, seed=seed)
            composer.print_score(song)
            if input("Export to composition.json? y/n [y]: ").lower() != 'n':
                composer.export_midi_like(song)

        elif choice == "5":
            prog = input("Enter chord progression comma separated (C,G,Am,F): ").strip()
            if prog:
                composer.chord_progression = [c.strip() for c in prog.split(",")]
                print(f"New progression: {composer.chord_progression}")

        elif choice == "6":
            break

if __name__ == "__main__":
    main()
