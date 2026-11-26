# Notepad + Spell Check Suite

Mixed your 3 codes into ONE app.

index Files

- `index.py` - main app (run this)
- `requirements.txt` - optional ML libs
- `README.md` - this file

index How to Run
bash
Works with ZERO extra install (edit-distance checker + fallback wordlist)
python notepad_spellcheck_suite.py

For full ML checker + full NLTK dictionary:
pip install -r requirements.txt

index What Was Mixed
| Original File | Where It Lives Now |

|---|---|
| Notepad (Tkinter) | Whole app: File / Edit / Help menus, Open/Save, Cut/Copy/Paste |
| Spell Checker - Edit Distance (NLTK) | Tools > Check Spelling (F7) - default checker |
| Spell Checker - ML (TF-IDF + Naive Bayes) | Tools > Train ML Model + Check Single Word (ML) |

index New Mixed Features

- indexF7 Check Spelling:index highlights unknown words in RED underline
- indexSuggestions popup:index shows top 5 suggestions per word (ranked by Brown Corpus frequency)
- indexType correctionindex to replace first error instantly
- indexStatus bar:index live Words | Chars | Errors count
- indexML Check:index trains TF-IDF + Naive Bayes on correct words + synthetic typos (insert/delete/replace), then predicts correct/incorrect
- indexLoad Sample Text:index loads `Ths is a sampl text with som spelling errrs` - press F7 to test instantly
- indexShortcuts:index Ctrl+N / Ctrl+O / Ctrl+S / F7, Undo, Select All

index Try It in 10 Seconds

1. Run the app
2. Tools > Load Sample Text with Errors
3. Press F7
4. See red highlights + suggestions like `Ths -> this, thus, ...`

index How Spell Check Works
index# Edit-Distance (File 3 logic)

if word not in english_words:
    candidates = [w for w in english_words if edit_distance(w, word) <= 2]
    ranked = sorted(candidates, by Brown frequency)
    return top 5

index# ML (File 2 logic)
For each real word:

- keep it as label=1 (correct)
- 50% chance: make typo (insert/delete/replace) as label=0 (incorrect)

TF-IDF vectorize -> train MultinomialNB -> predict new word

Note: ML version in original trained on ALL ~236k NLTK words (very slow).
This merged version trains on a 3000-word SAMPLE so Notepad doesn't freeze - accuracy still shows on train.

index Requirements

- Python 3.8+, `tkinter` (usually included, Linux: `sudo apt install python3-tk`)
- Optional for full dictionary: `nltk`
- Optional for ML: `pandas numpy scikit-learn nltk`
