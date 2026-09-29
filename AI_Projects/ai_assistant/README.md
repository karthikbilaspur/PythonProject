# AI_ASSISTANT - Extreme Word Intelligence System

> This is not a word generator. This is a self-learning vocabulary AI that adapts to you.

### Evolution
- `normal/` -> static dictionary `words.py`
- `enhanced/` -> single file menu
- `final/` -> SQLite + OpenTDB quiz
- `ultimate/` -> modular split
- **`ai_assistant/` (THIS) -> Extreme AI with Memory + Brain + Adaptive Learning**

### What Makes It EXTREME?

1.  **Brain.py - Real AI Logic**
    - Uses WordNet for hints, definitions, examples, roots
    - Calculates your level (BEGINNER/INTERMEDIATE/EXPERT) from DB
    - Weakness Analysis: Finds your top 5 failing words/categories
    - Spaced Repetition (SM-2): Failed words return after 1d, 3d, 7d

2.  **Word Engine - Not random.choice()**
    - Embedding-style similarity search
    - Auto-imports words via AI prompt
    - Category mastery tracking

3.  **Quiz Engine - Adaptive**
    - Mixes your `words.json` + OpenTDB API + AI-generated questions
    - Time pressure adapts to your level
    - After 3 fails, auto-hint triggers
    - Voice mode (pyttsx3) optional

4.  **Memory.db**
    - `scores` - all quiz attempts
    - `mistakes` - tracks fails per word
    - `reviews` - spaced repetition schedule

### Structure
```
ai_assistant/
├── main.py           # Entry point - Extreme CLI
├── brain.py          # Intelligence layer
├── word_engine.py    # Word operations (replaces word_generator.py + words.py)
├── quiz_engine.py    # Adaptive quiz (replaces quiz.py)
├── file_manager.py   # JSON/CSV/AI import
├── words.json        # Knowledge base (replaces .py dict)
└── memory.db         # Auto-created on first run
```

### Installation
```bash
pip install nltk requests pyttsx3
python -c "import nltk; nltk.download('wordnet'); nltk.download('punkt')"
python main.py
```

### Commands in EXTREME mode
```
> learn           # AI teaches you a new word based on your weakness
> quiz            # Adaptive quiz (easy/medium/hard/adaptive)
> quiz voice      # Voice quiz
> weakness        # Show where you fail
> import 20 startup words  # AI generates words
> stats           # Leaderboard + mastery
> exit
```

### Why Not Single File?
Single file = 400+ lines, impossible to debug, crashes like `for i, question: enumerate` are hidden.
Modular = each file does 1 job. This is production style.

### Future Extreme Ideas
- [ ] Add sentence-transformers for semantic quiz
- [ ] Add speech-to-text for voice answer
- [ ] Add streaks & XP system
- [ ] Web UI with FastAPI

Built by clubbing normal + enhanced + final + ultimate -> ai_assistant.


## V2 EXTREME ENHANCEMENTS (New in ZIP)
- **app.py** - FastAPI Web API (`/random`, `/search`, `/` for stats)
- **voice_mode.py** - Voice quiz with pyttsx3 (speaks word, you answer)
- **XP System** - brain.get_xp() tracks total XP
- **Auto API Docs** at http://localhost:8000/docs

Run web mode:
```bash
pip install fastapi uvicorn
uvicorn app:app --reload
```
