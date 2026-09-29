# EXTREME MUSIC AI - 3 Engines Clubbed Properly

This is the fixed and enhanced version of your 3 separate files.
Kept separate for development, clubbed via `composer.py` for final output.

## Structure

```
extreme_music_ai/
├── melody_engine.py   # FIXED - Markov chain, seed support, validation
├── harmony_engine.py  # FIXED - Correct semitones, actually uses chords
├── rhythm_engine.py   # FIXED - No globals, proper bar overflow handling
├── composer.py        # NEW - Clubs all 3 into full song [EXTREME]
├── main.py            # CLI to test each engine
├── composition.json   # Auto-generated export
└── README.md
```

## What Was Wrong Before (Immediate Fixes Applied)

### File 1: Harmony
- **BUG:** `chord_progression` passed but never used
- **BUG:** Intervals `[3,5]` wrong - 3 = minor third, 5 = perfect 4th. Fixed to `[4,7]` for major triad
- **BUG:** No validation for invalid notes like `Am`
- **FIXED:** Now maps chords to chord tones, validates style, supports 5 styles: classical, jazz, pop, minor, blues

### File 2: Melody
- **BUG:** Mixed `random` and `np.random`, no seed = not reproducible
- **BUG:** No check for `length <=0`
- **FIXED:** Added seed param, validation, `validate_matrix()` to ensure probs sum to 1, added `generate_melody_with_constraints()`

### File 3: Rhythm
- **BUG:** `genre` and `musical_style` were GLOBAL, function had no args
- **BUG:** `if current_time >= time_signature[0]: current_time -= time_signature[0]` loses leftover
- **BUG:** Returned same start_time for different bars
- **FIXED:** Now takes genre/style as args, returns `(start, duration, bar, duration_name)`, proper floating point handling, supports 5 genres

## How to Run

```bash
pip install -r requirements.txt
python main.py

# Option 4 = Full composition
```

## Example Output

```
Bar  Start  Dur      Melody  Harmony         Chord
------------------------------------------------------------
1    0.0    16th     C       E,G             C
1    0.25   8th      D       F#,A            G
1    0.75   quarter  E       G#,B            Am
```

## Why Keep 3 Separate?

**Pros of 3 separate (this approach):**
- You can test melody without breaking harmony
- You can upgrade Markov matrix to LSTM later without touching rhythm
- Real music software works this way (Ableton, Magenta)

**Pros of 1 single file:**
- Easy to submit as single assignment
- Quick demo

**Verdict:** Keep 3 separate + composer.py = extreme professional way.

## Next Extreme Ideas

- [ ] Add `mido` to export real `.mid` file
- [ ] Replace Markov with Transformer
- [ ] Add drum pattern engine
- [ ] Web UI with piano roll visualization

## Comparison to Your Word Assistant

Your `ai_assistant/` was:
`words.py + word_generator + file_manager + quiz + brain = 1 AI`

This is:
`melody_engine + harmony_engine + rhythm_engine + composer = 1 Song AI`

Same clubbing philosophy.
