"""
word_engine.py - Replaces words.py + word_generator.py
Handles categorized words with JSON backend
"""
import json
import random
import os

WORDS_FILE = "words.json"

class WordEngine:
    def __init__(self, file=WORDS_FILE):
        self.file = file
        self.data = self.load()

    def load(self):
        if not os.path.exists(self.file):
            return {}
        with open(self.file, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_all_categories(self):
        return list(self.data.keys())

    def generate_random_word(self, category=None):
        if category:
            if category not in self.data or not self.data[category]:
                print(f"Category {category} empty")
                return None
            return random.choice(self.data[category])
        # weighted by fails - show weak words more often
        all_words = []
        for cat, words in self.data.items():
            for w in words:
                weight = w.get('fails', 0) + 1
                all_words.extend([ (w, cat) ] * weight)
        if not all_words: return None
        word, cat = random.choice(all_words)
        return {**word, "category": cat}

    def search_word(self, query):
        query = query.lower()
        for cat, words in self.data.items():
            for w in words:
                if w['word'].lower() == query:
                    return {**w, "category": cat}
        return None

    def add_word(self, category, word, meaning, difficulty="medium"):
        if category not in self.data:
            self.data[category] = []
        # avoid duplicates
        if self.search_word(word):
            print("Word already exists, updating meaning")
            self.delete_word(word)
        self.data[category].append({
            "word": word, "meaning": meaning, 
            "difficulty": difficulty, "fails": 0
        })
        self.save()
        print(f"Added '{word}' to {category}")

    def delete_word(self, word):
        for cat in self.data:
            for w in self.data[cat]:
                if w['word'].lower() == word.lower():
                    self.data[cat].remove(w)
                    self.save()
                    return True
        return False

    def display_all(self):
        for cat, words in self.data.items():
            print(f"\n== {cat.upper()} ({len(words)} words) ==")
            for w in words:
                print(f"  {w['word']}: {w['meaning']}")

    def teach_new_word(self, brain):
        # AI teaches weakest category
        conn_cat = brain  # placeholder
        word = self.generate_random_word()
        if not word: return
        print(f"\nNew word for you: {word['word']}")
        print(f"Category: {word.get('category')}")
        print(f"Meaning: {word['meaning']}")
        print(f"\nHint: {brain.get_hint(word['word'])}")
