import random

def quiz_mode(words):
    print("Quiz Mode")
    print("---------")
    print("Available categories:")
    for category in words['words']:
        print(category)
    category = input("Enter category (or leave blank for random category): ")
    
    score = 0
    total_questions = 5
    
    if category:
        if category in words['words']:
            questions = random.sample(words['words'][category], min(total_questions, len(words['words'][category])))
        else:
            print("Invalid category.")
            return
    else:
        questions = []
        for cat in words['words']:
            questions.extend(words['words'][cat])
        questions = random.sample(questions, min(total_questions, len(questions)))
    
    for question in questions:
        answer = input(f"What is the meaning of '{question['word']}'? ")
        if answer.lower() == question['meaning'].lower():
            score += 1
            print("Correct!")
        else:
            print(f"Sorry, the correct answer is '{question['meaning']}'.")
    
    print(f"Quiz finished. Your final score is {score} out of {len(questions)}.")

def advanced_quiz_mode(words):
    print("Advanced Quiz Mode")
    print("------------------")
    print("Available categories:")
    for category in words['words']:
        print(category)
    category = input("Enter category (or leave blank for random category): ")
    
    score = 0
    total_questions = 5
    
    if category:
        if category in words['words']:
            questions = random.sample(words['words'][category], min(total_questions, len(words['words'][category])))
        else:
            print("Invalid category.")
            return
    else:
        questions = []
        for cat in words['words']:
            questions.extend(words['words'][cat])
        questions = random.sample(questions, min(total_questions, len(questions)))
    
    for question in questions:
        print(f"What is the meaning of '{question['word']}'?")
        print("A) " + question['meaning'])
        options = [question['meaning']]
        while len(options) < 4:
            random_question = random.choice(random.choice(list(words['words'].values())))
            if random_question['meaning'] not in options:
                options.append(random_question['meaning'])
        random.shuffle(options)
        for i, option in enumerate(options):
            print(f"{chr(65 + i)}) {option}")
        answer = input("Enter the letter of your answer: ")
        if options[ord(answer.upper()) - 65] == question['meaning']:
            score += 1
            print("Correct!")
        else:
            print(f"Sorry, the correct answer is '{question['meaning']}'.")
    
    print(f"Quiz finished. Your final score is {score} out of {len(questions)}.")

def quiz_menu(words):
    while True:
        print("\nQuiz Menu:")
        print("1. Quiz Mode")
        print("2. Advanced Quiz Mode")
        print("3. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            quiz_mode(words)
        elif choice == "2":
            advanced_quiz_mode(words)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")