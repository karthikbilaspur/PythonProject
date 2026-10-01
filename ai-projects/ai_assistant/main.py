"""
main.py - Extreme AI Assistant Entry Point
Merges all your mains (enhanced + final) into one
"""
from brain import AIBrain
from word_engine import WordEngine
from quiz_engine import AdaptiveQuiz
from file_manager import FileManager
try:
    from voice_mode import voice_quiz
except:
    voice_quiz = None
import os

def print_banner():
    print("""
    ╔════════════════════════════════════════╗
    ║   AI_ASSISTANT - EXTREME EDITION     ║
    ║   Vocab + Trivia + Memory + Brain    ║
    ╚════════════════════════════════════════╝
    """)

def main():
    print_banner()
    brain = AIBrain()
    words = WordEngine()
    quiz = AdaptiveQuiz(brain, words)
    files = FileManager()

    print(f"Level: {brain.get_user_level()}")
    print(f"Categories: {', '.join(words.get_all_categories())}")
    print(f"Total words: {sum(len(v) for v in words.data.values())}")

    while True:
        print("\n--- EXTREME MENU ---")
        print("1. Generate Random Word")
        print("2. Search Word")
        print("3. Add Word")
        print("4. Display All")
        print("5. Quiz - Vocab (type meaning)")
        print("6. Quiz - MCQ (advanced)")
        print("7. Quiz - Trivia (OpenTDB API)")
        print("8. EXTREME Adaptive Mode [RECOMMENDED]")
        print("9. Weakness Analysis")
        print("10. File Manager (Save/Load/CSV)")
        print("11. Stats / Leaderboard")
        print("12. Voice Quiz [EXTREME]")
        print("13. Web API Mode")
        print("14. Exit")

        choice = input("Enter choice > ").strip()

        if choice == "1":
            cat = input(f"Category {words.get_all_categories()} or blank for random: ").strip() or None
            w = words.generate_random_word(cat)
            if w: print(f"{w['word']} ({w.get('category')}): {w['meaning']}")

        elif choice == "2":
            q = input("Word to search: ")
            res = words.search_word(q)
            print(res if res else "Not found")

        elif choice == "3":
            cat = input("Category: ")
            w = input("Word: ")
            m = input("Meaning: ")
            d = input("Difficulty (easy/medium/hard) [medium]: ") or "medium"
            words.add_word(cat, w, m, d)

        elif choice == "4":
            words.display_all()

        elif choice == "5":
            cat = input("Category or blank: ").strip() or None
            quiz.quiz_vocab_mode(cat, total=5)

        elif choice == "6":
            cat = input("Category or blank: ").strip() or None
            quiz.quiz_mcq_mode(cat, total=5)

        elif choice == "7":
            diff = input("Difficulty easy/medium/hard [medium]: ").strip() or "medium"
            quiz.quiz_opentdb_mode(diff)

        elif choice == "8":
            quiz.start_extreme_mode(difficulty="adaptive")

        elif choice == "9":
            brain.show_weakness_analysis()

        elif choice == "10":
            print("\n a) Save JSON  b) Load JSON  c) Export CSV  d) Import CSV  e) AI Import")
            sub = input("> ").lower()
            if sub == "a": files.save_words_to_file(words.data)
            elif sub == "b":
                loaded = files.load_words_from_file()
                if loaded: words.data = loaded; words.save()
            elif sub == "c": files.export_to_csv(words.data)
            elif sub == "d":
                imported = files.import_from_csv()
                if imported: words.data = imported; words.save()
            elif sub == "e":
                prompt = input("What words to AI generate? e.g. '20 startup words': ")
                files.ai_import(prompt)

        elif choice == "11":
            import sqlite3
            conn = sqlite3.connect("memory.db")
            cur = conn.cursor()
            cur.execute("SELECT username, score, total, difficulty, date FROM scores ORDER BY date DESC LIMIT 10")
            rows = cur.fetchall()
            print("\n--- Last 10 Scores ---")
            for r in rows: print(r)
            conn.close()
            print(f"\n{brain.get_user_level()}")

        elif choice == "12":
            if voice_quiz:
                voice_quiz(words, brain)
            else:
                print("Install pyttsx3: pip install pyttsx3")
        elif choice == "13":
            print("Starting API at http://localhost:8000 ...")
            print("Run: uvicorn app:app --reload")
            import os
            os.system("uvicorn app:app --reload")
        elif choice == "14":
            print(f"Final XP: {brain.get_xp()} | Level: {brain.get_user_level()}")
            print("Shutting down AI...")
            break
        else:
            print("Invalid")

if __name__ == "__main__":
    main()
