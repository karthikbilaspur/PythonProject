import random

def level1():
    print("Level 1: Guess the Number")
    number_to_guess = random.randint(1, 10)
    guess = None
    attempts = 0
    while guess != number_to_guess:
        guess = int(input("Guess a number between 1 and 10: "))
        attempts += 1
        if guess < number_to_guess:
            print("Too low!")
        elif guess > number_to_guess:
            print("Too high!")
    print(f"Congratulations! You guessed the number in {attempts} attempts.")
    return attempts

def level2():
    print("Level 2: Word Scramble")
    words = ["apple", "banana", "cherry"]
    word_to_unscramble = random.choice(words)
    scrambled_word = "".join(random.sample(word_to_unscramble, len(word_to_unscramble)))
    print(f"Unscramble the word: {scrambled_word}")
    answer = input("Enter your answer: ")
    if answer.lower() == word_to_unscramble:
        print("Correct!")
        return True
    else:
        print(f"Sorry, the correct answer was {word_to_unscramble}.")
        return False

def level3():
    print("Level 3: Math Problem")
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(["+", "-", "*"])
    if operator == "+":
        answer = num1 + num2
    elif operator == "-":
        answer = num1 - num2
    else:
        answer = num1 * num2
    print(f"What is {num1} {operator} {num2}?")
    user_answer = int(input("Enter your answer: "))
    if user_answer == answer:
        print("Correct!")
        return True
    else:
        print(f"Sorry, the correct answer was {answer}.")
        return False

def level4():
    print("Level 4: Logic Puzzle")
    print("There are three switches, but they are not labelled. Each switch corresponds to one of three light bulbs in a room. Each light bulb is either on or off. You can turn the lights on and off as many times as you want, but you can only enter the room one time. How do you figure out which switch corresponds to which light bulb?")
    answer = input("Enter your answer: ")
    if "turn two switches on" in answer.lower() or "turn two of the switches on" in answer.lower():
        print("Correct!")
        return True
    else:
        print("Sorry, that's not correct. One possible solution is to turn two switches on for 5 minutes, then turn one of them off. Then, go into the room. The bulb that is on corresponds to one of the switches that was left on. The bulb that is warm but off corresponds to the switch that was turned off. The bulb that is cold and off corresponds to the switch that was never turned on.")
        return False

def level5():
    print("Level 5: Trivia Question")
    questions = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
        {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"}
    ]
    question = random.choice(questions)
    print(question["question"])
    answer = input("Enter your answer: ")
    if answer.lower() == question["answer"].lower():
        print("Correct!")
        return True
    else:
        print(f"Sorry, the correct answer was {question['answer']}.")
        return False

def main():
    score = 0
    levels = [level1, level2, level3, level4, level5]
    for i, level in enumerate(levels):
        print(f"\nLevel {i+1}:")
        result = level()
        if result is True:
            score += 10
        elif isinstance(result, int):
            score += 10 - result
    print(f"\nGame Over! Your final score is {score}.")

if __name__ == "__main__":
    main()