"""
quiz_engine.py - Extreme Adaptive Quiz
Replaces old quiz.py + merges OpenTDB + your vocab
"""
import random
import time
import requests
from datetime import datetime

class AdaptiveQuiz:
    def __init__(self, brain, word_engine=None):
        self.brain = brain
        self.word_engine = word_engine
        # Lazy import to avoid circular
        if word_engine is None:
            from word_engine import WordEngine
            self.word_engine = WordEngine()

    def get_opentdb_questions(self, difficulty="medium", amount=5):
        try:
            url = f"https://opentdb.com/api.php?amount={amount}&type=multiple&difficulty={difficulty}"
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            return r.json().get("results", [])
        except Exception as e:
            print(f"API offline ({e}), using local vocab only")
            return []

    def quiz_vocab_mode(self, category=None, total=5):
        score = 0
        print(f"\n--- VOCAB QUIZ [{category or 'MIXED'}] ---")
        for i in range(total):
            q = self.word_engine.generate_random_word(category)
            if not q: 
                print("No words found")
                break
            ans = input(f"Q{i+1}: What does '{q['word']}' mean? > ").strip()
            if ans.lower() == q['meaning'].lower():
                print("Correct!")
                score += 1
            else:
                print(f"Wrong. Correct: {q['meaning']}")
                print(self.brain.get_hint(q['word']))
                self.brain.log_mistake(q['word'], q.get('category','general'))
        print(f"\nScore: {score}/{total}")
        self.brain.save_score("user", score, total, category or "mixed")
        return score

    def quiz_mcq_mode(self, category=None, total=5):
        # Advanced MCQ from your original advanced_quiz_mode but fixed
        print(f"\n--- MCQ MODE ---")
        score = 0
        all_words = []
        for cat, ws in self.word_engine.data.items():
            all_words.extend(ws)
        
        if len(all_words) < 4:
            print("Need at least 4 words for MCQ")
            return self.quiz_vocab_mode(category, total)

        questions = random.sample(all_words, min(total, len(all_words)))
        for q in questions:
            print(f"\nWhat is the meaning of '{q['word']}'?")
            options = [q['meaning']]
            # get 3 random wrong options
            while len(options) < 4:
                wrong = random.choice(all_words)['meaning']
                if wrong not in options:
                    options.append(wrong)
            random.shuffle(options)
            for idx, opt in enumerate(options):
                print(f"  {chr(65+idx)}) {opt}")
            choice = input("Your answer (A-D): ").strip().upper()
            if not choice or ord(choice)-65 >= len(options):
                print("Invalid")
                continue
            if options[ord(choice)-65] == q['meaning']:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong. Answer: {q['meaning']}")
                self.brain.log_mistake(q['word'], q.get('category','general'))
        print(f"\nFinal: {score}/{len(questions)}")
        self.brain.save_score("user", score, len(questions), "mcq")
        return score

    def quiz_opentdb_mode(self, difficulty="medium"):
        questions = self.get_opentdb_questions(difficulty, 5)
        if not questions: return
        score = 0
        time_limits = {"easy": 15, "medium": 20, "hard": 30}
        limit = time_limits.get(difficulty, 20)
        for q in questions:
            answers = q["incorrect_answers"] + [q["correct_answer"]]
            random.shuffle(answers)
            print(f"\nQ: {q['question']}")
            for i,a in enumerate(answers):
                print(f"  {i+1}. {a}")
            start = time.time()
            ans_idx = input("Answer number: ").strip()
            elapsed = time.time() - start
            if elapsed > limit:
                print(f"Time's up! ({elapsed:.1f}s > {limit}s)")
                continue
            try:
                chosen = answers[int(ans_idx)-1]
                if chosen.lower() == q["correct_answer"].lower():
                    print("Correct!")
                    score += 1
                else:
                    print(f"Wrong. Correct: {q['correct_answer']}")
            except:
                print("Invalid")
        print(f"\nTrivia Score: {score}/{len(questions)}")
        self.brain.save_score("user", score, len(questions), f"trivia-{difficulty}")

    def start_extreme_mode(self, difficulty="adaptive"):
        print("\n=== EXTREME ADAPTIVE MODE ===")
        if difficulty == "adaptive":
            # Pick difficulty based on level
            level = self.brain.get_user_level()
            difficulty = "hard" if "EXPERT" in level else "medium" if "INTERMEDIATE" in level else "easy"
            print(f"Auto-difficulty: {difficulty} (based on {level})")
        
        # 1. Vocab, 2. MCQ, 3. Trivia
        self.quiz_vocab_mode(total=3)
        self.quiz_mcq_mode(total=2)
        self.quiz_opentdb_mode(difficulty)
