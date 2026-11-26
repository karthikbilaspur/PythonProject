# Scrabble Game

Tkinter word game for 2-6 players. Take turns entering words, score with standard Scrabble letter values, 5 rounds each, then a winner (or tie) is declared.

 Requirements

```bash
pip install nltk requests

```

`requests` is only for definitions — the game itself works offline without it.

 Run

```bash
python scrabble_game.py
```

 How to play

1. Enter number of players (2-6), then each player's name (must be unique).
2. On your turn, type a word and press Submit (or Enter).
3. Word must be letters only, in the word list, and not already played.
4. After 5 rounds each, the highest score wins.

 Rebuilt vs pasted version
The pasted version did not run at all:

- Syntax error: `WordListCorpusReader(...).words:()` is invalid Python.
- Two `__init__` definitions and no `class ScrabbleGame:` line at all.
- `self.root.wkids()` should be `winfo_children()`.
- `nltk.download('words')` on every import → now lazy, only if missing, with an offline fallback word set.
- `PyDictionary` is abandoned and its API is dead → removed. Definitions now use free DictionaryAPI (no key), with offline handling.
- Errors were only `print()`ed → now shown in the GUI status line.
- Game-over logic was wrong: it ended when nobody had score 0, i.e. after round 1. Now tracks rounds properly.
- Added validation: player count 2-6, non-empty/unique names, non-alpha words, duplicate words per game.
