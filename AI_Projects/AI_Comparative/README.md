
# AI Adjective Comparative & Superlative Generator

A simple, 1-page Python program for beginners that generates the comparative and superlative forms of English adjectives.

No external libraries required — just Python 3.

Features

- Handles regular rules (`tall -> taller / tallest`)
- Handles `e` ending (`nice -> nicer / nicest`)
- Handles `y` ending (`happy -> happier / happiest`)
- Handles doubling (`big -> bigger / biggest`)
- Handles long adjectives (`beautiful -> more beautiful / most beautiful`)
- Handles irregulars (`good -> better / best`, `bad -> worse / worst`)
- Simple AI syllable counter to guess when to use `more / most`

 How It Works
The program uses a rule-based approach:

1. Irregular Check: Checks a dictionary of irregular adjectives.
2. Syllable Count: Counts vowel groups to estimate syllables. If >= 3, it uses `more / most`.
3. Suffix Rules: Applies English grammar rules for `y`, `e`, and CVC (consonant-vowel-consonant) patterns.
4. Default: Adds `-er / -est`.

 Installation

1. Make sure you have Python 3 installed.
2. Download `adjective.py`


 Usage

Run it from your terminal:

```bash
python adjective.py
```

Then type any adjective when prompted:

=== AI Adjective Generator (comparative & superlative) ===
Type 'quit' to exit

Enter an adjective: tall
 -> Comparative: taller
 -> Superlative: tallest

Enter an adjective: happy
 -> Comparative: happier
 -> Superlative: happiest

Enter an adjective: beautiful
 -> Comparative: more beautiful
 -> Superlative: most beautiful

Type `quit`, `exit`, or `q` to stop.

 File Structure
.
├── adjective.py    Main program
└── README.md       This file

License
MIT - Free to use for learning and projects.
