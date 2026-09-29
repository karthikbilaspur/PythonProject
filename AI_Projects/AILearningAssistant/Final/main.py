import requests
import sqlite3
import time
import random
import unittest
import nltk
from nltk.corpus import wordnet

# Create a SQLite database
conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

# Create a table to store user scores
cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY,
        username TEXT,
        score INTEGER,
        difficulty TEXT,
        date TEXT
    )
""")

def get_quiz_questions(difficulty):
    try:
        url = f"https://opentdb.com/api.php?amount=10&type=multiple&difficulty={difficulty}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["results"]
    except requests.RequestException as e:
        print(f"Error fetching questions: {e}")
        return []

def quiz(difficulty, username):
    questions = get_quiz_questions(difficulty)
    if not questions:
        print("Failed to fetch questions. Please try again later.")
        return

    score = 0
    
    # Time limit for each question
    time_limits = {
        "easy": 15,
        "medium": 20,
        "hard": 30
    }
    time_limit = time_limits[difficulty]
    
    start_time = time.time()
    for question in questions:
        # Shuffle the answers
        answers = question["incorrect_answers"] + [question["correct_answer"]]
        random.shuffle(answers)
        
        question_start_time = time.time()
        print(f"Question: {question['question']}")
        for i, answer in enumerate(answers):
            print(f"{i+1}. {answer}")
        answer_index = input("Enter the number of your answer: ")
        try:
            answer_index = int(answer_index) - 1
            if answer_index < 0 or answer_index >= len(answers):
                print("Invalid answer number.")
                continue
            answer = answers[answer_index]
        except ValueError:
            print("Invalid answer number.")
            continue
        question_end_time = time.time()
        elapsed_time = question_end_time - question_start_time
        
        if elapsed_time <= time_limit:
            if answer.lower() == question["correct_answer"].lower():
                score += 1
                print("Correct!")
            else:
                print(f"Sorry, the correct answer is '{question['correct_answer']}'.")
        else:
            print("Time's up! You took too long to answer.")
    
    end_time = time.time()
    total_elapsed_time = end_time - start_time
    
    # Store the score in the database
    try:
        import datetime
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO scores (username, score, difficulty, date) VALUES (?, ?, ?, ?)", (username, score, difficulty, date))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error storing score: {e}")
    
    print(f"Quiz finished. Your final score is {score} out of {len(questions)}.")
    print(f"Time taken: {total_elapsed_time} seconds")

def view_scores():
    try:
        cursor.execute("SELECT username, score, difficulty, date FROM scores ORDER BY score DESC")
        scores = cursor.fetchall()
        if not scores:
            print("No scores to display.")
            return
        print("Leaderboard:")
        for score in scores:
            print(f"Username: {score[0]}, Score: {score[1]}, Difficulty: {score[2]}, Date: {score[3]}")
    except sqlite3.Error as e:
        print(f"Error fetching scores: {e}")

def get_ai_assistance():
    print("AI Assistance:")
    print("1. Get hint for a question")
    print("2. Get explanation for a question")
    choice = input("Enter your choice: ")
    if choice == "1":
        question = input("Enter the question: ")
        print(get_hint(question))
    elif choice == "2":
        question = input("Enter the question: ")
        print(get_explanation(question))

def get_hint(question):
    try:
        tokens = nltk.word_tokenize(question)
        synonyms = []
        for token in tokens:
            synsets = wordnet.synsets(token)
            for synset in synsets:
                synonyms.extend(synset.lemmas())
        hint = "Think about " + ", ".join([synonym.name() for synonym in synonyms])
        return hint
    except Exception as e:
        return "Failed to generate hint."

def get_explanation(question):
    return "This question is testing your knowledge of a specific topic. Try to recall the relevant information and apply it to the question."

def review_questions(questions, answers):
    for i, question: enumerate(questions):
        print(f"Question {i+1}: {question['question']}")
        print(f"Your answer: {answers[i]}")
        print(f"Correct answer: {question['correct_answer']}")
        print()

def main():
    while True:
        print("Quiz Menu:")
        print("1. Start quiz")
        print("2. View scores")
        print("3. Get AI assistance")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter your username: ")
            while True:
                difficulty = input("Enter the difficulty level (easy, medium, or hard): ").lower()
                if difficulty in ["easy", "medium", "hard"]:
                    break
                print("Invalid difficulty level. Please try again.")
            questions = get_quiz_questions(difficulty)
            answers = []
            score = 0
            
            # Time limit for each question
            time_limits = {
                "easy": 15,
                "medium": 20,
                "hard": 30
            }
            time_limit = time_limits[difficulty]
            
            start_time = time.time()
            for question in questions:
                # Shuffle the answers
                answers_list = question["incorrect_answers"] + [question["correct_answer"]]
                random.shuffle(answers_list)
                
                question_start_time = time.time()
                print(f"Question: {question['question']}")
                for i, answer in enumerate(answers_list):
                    print(f"{i+1}. {answer}")
                answer_index = input("Enter the number of your answer: ")
                try:
                    answer_index = int(answer_index) - 1
                    if answer_index < 0 or answer_index >= len(answers_list):
                        print("Invalid answer number.")
                        answers.append("Invalid")
                        continue
                    answer = answers_list[answer_index]
                    answers.append(answer)
                except ValueError:
                    print("Invalid answer number.")
                    answers.append("Invalid")
                    continue
                question_end_time = time.time()
                elapsed_time = question_end_time - question_start_time
                
                if elapsed_time <= time_limit:
                    if answer.lower() == question["correct_answer"].lower():
                        score += 1
                        print("Correct!")
                    else:
                        print(f"Sorry, the correct answer is '{question['correct_answer']}'.")
                else:
                    print("Time's up! You took too long to answer.")
            
            end_time = time.time()
            total_elapsed_time = end_time - start_time
            
            # Store the score in the database
            try:
                import datetime
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO scores (username, score, difficulty, date) VALUES (?, ?, ?, ?)", (username, score, difficulty, date))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error storing score: {e}")
            
            print(f"Quiz finished. Your final score is {score} out of {len(questions)}.")
            print(f"Time taken: {total_elapsed_time} seconds")
            review_questions(questions, answers)
        elif choice == "2":
            view_scores()
        elif choice == "3":
            get_ai_assistance()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Run the unit tests
    #unittest.main(exit=False)
    # Start the quiz menu
    main()