"""
file_manager.py - Handles JSON, CSV and AI import
Fixed version of your old file
"""
import json
import csv
import os

class FileManager:
    def save_words_to_file(self, data, filename="words.json"):
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Saved to {filename}")
        except Exception as e:
            print(f"Error saving: {e}")

    def load_words_from_file(self, filename="words.json"):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{filename} not found")
            return None
        except Exception as e:
            print(f"Error loading: {e}")
            return None

    def export_to_csv(self, data, filename="words.csv"):
        try:
            with open(filename, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Category", "Word", "Meaning", "Difficulty"])
                for cat, words in data.items():
                    for w in words:
                        writer.writerow([cat, w['word'], w['meaning'], w.get('difficulty','medium')])
            print(f"Exported to {filename}")
        except Exception as e:
            print(f"CSV export error: {e}")

    def import_from_csv(self, filename="words.csv"):
        try:
            data = {}
            with open(filename, "r", encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cat = row['Category']
                    if cat not in data:
                        data[cat] = []
                    data[cat].append({
                        "word": row['Word'],
                        "meaning": row['Meaning'],
                        "difficulty": row.get('Difficulty','medium'),
                        "fails": 0
                    })
            print(f"Imported {sum(len(v) for v in data.values())} words from {filename}")
            return data
        except Exception as e:
            print(f"CSV import error: {e}")
            return None

    def ai_import(self, prompt="20 difficult GRE words"):
        """
        Extreme feature: In real app, call OpenAI/LLM here.
        For now, mock with template - you can wire your API key
        """
        print(f"AI Import requested: '{prompt}'")
        print(">>> [MOCK] In production, this would call LLM API to generate words")
        print(">>> Example: Connect OpenAI API and append to words.json")
        # Example structure you would get from AI:
        # {"category": "startup", "words": [{"word": "pivot", "meaning": "..."}]}
        return None
