"""
brain.py - The Intelligence Layer
Replaces random logic with WordNet + Memory analysis + Spaced Repetition
"""
import sqlite3
import os
from datetime import datetime, timedelta

try:
    import nltk
    from nltk.corpus import wordnet
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

DB_PATH = "memory.db"

class AIBrain:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
                username TEXT, score INTEGER, total INTEGER,
                difficulty TEXT, date TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY,
                word TEXT, category TEXT, fails INTEGER DEFAULT 1,
                last_failed TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                word TEXT PRIMARY KEY,
                next_review TEXT,
                interval_days INTEGER DEFAULT 1
            )
        """)
        conn.commit()
        conn.close()

    def get_hint(self, word):
        if not NLTK_AVAILABLE:
            return f"Think about the root of '{word}'"
        synsets = wordnet.synsets(word)
        if not synsets:
            return f"No WordNet entry for {word}, try breaking it into roots."
        syn = synsets[0]
        definition = syn.definition()
        examples = syn.examples()
        synonyms = [l.name() for l in syn.lemmas()[:3]]
        hint = f"Definition: {definition}\n"
        if examples: hint += f"Example: {examples[0]}\n"
        if synonyms: hint += f"Synonyms: {', '.join(synonyms)}"
        return hint

    def get_user_level(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT AVG(CAST(score AS FLOAT)/total) FROM scores")
        avg = cur.fetchone()[0]
        conn.close()
        if avg is None: return "BEGINNER (new)"
        if avg > 0.8: return f"EXPERT ({avg*100:.1f}%)"
        if avg > 0.5: return f"INTERMEDIATE ({avg*100:.1f}%)"
        return f"BEGINNER ({avg*100:.1f}%)"

    def log_mistake(self, word, category="general"):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT fails FROM mistakes WHERE word=?", (word,))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE mistakes SET fails=fails+1, last_failed=? WHERE word=?", 
                        (datetime.now().isoformat(), word))
            fails = row[0] + 1
        else:
            cur.execute("INSERT INTO mistakes (word, category, fails, last_failed) VALUES (?,?,1,?)",
                        (word, category, datetime.now().isoformat()))
            fails = 1
        
        # Spaced Repetition SM-2 logic
        interval = 1 if fails == 1 else 3 if fails == 2 else 7 if fails == 3 else 14
        next_review = datetime.now() + timedelta(days=interval)
        cur.execute("INSERT OR REPLACE INTO reviews (word, next_review, interval_days) VALUES (?,?,?)",
                    (word, next_review.isoformat(), interval))
        conn.commit()
        conn.close()

    def show_weakness_analysis(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        print("\n--- BRAIN ANALYSIS ---")
        cur.execute("SELECT word, category, fails FROM mistakes ORDER BY fails DESC LIMIT 5")
        rows = cur.fetchall()
        if not rows:
            print("No weaknesses yet. You're perfect (for now).")
        else:
            for w, cat, f in rows:
                print(f"  {w} ({cat}) - failed {f} times")
        
        cur.execute("SELECT word, next_review FROM reviews WHERE next_review <= ?", (datetime.now().isoformat(),))
        due = cur.fetchall()
        if due:
            print(f"\nDue for review today: {', '.join([d[0] for d in due])}")
        conn.close()

    def get_xp(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT SUM(score) FROM scores")
        xp = cur.fetchone()[0] or 0
        conn.close()
        return xp

    def save_score(self, username, score, total, difficulty):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO scores (username, score, total, difficulty, date) VALUES (?,?,?,?,?)",
                    (username, score, total, difficulty, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
