import random

class CodingGame:
    def __init__(self):
        self.questions = {
            "What is the print function in Python?": ["print()", "console.log()", "System.out.println()"],
            "What is the syntax for declaring a variable in JavaScript?": ["let x = 5;", "var x = 5;", "x = 5;"],
            "What is the purpose of the 'if' statement in programming?": ["To loop through a block of code", "To make decisions based on conditions", "To declare variables"],
        }
        self.answers = {
            "What is the print function in Python?": "print()",
            "What is the syntax for declaring a variable in JavaScript?": "let x = 5;",
            "What is the purpose of the 'if' statement in programming?": "To make decisions based on conditions",
        }

    def play(self):
        score = 0
        for question, options in self.questions.items():
            print(question)
            random.shuffle(options)
            for i, option in enumerate(options):
                print(f"{i+1}. {option}")
            answer = input("Enter the number of your answer: ")
            if options[int(answer) - 1] == self.answers[question]:
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect. The correct answer is {self.answers[question]}")
        print(f"Your final score is {score} out of {len(self.questions)}")

class AI:
    def __init__(self):
        self.knowledge = {}

    def learn(self, question, answer):
        self.knowledge[question] = answer

    def answer_question(self, question):
        if question in self.knowledge:
            return self.knowledge[question]
        else:
            return "I don't know the answer to this question."

def main():
    game = CodingGame()
    ai = AI()

    print("Welcome to the coding game!")
    print("You can play the game or teach the AI.")

    while True:
        print("1. Play the game")
        print("2. Teach the AI")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            game.play()
        elif choice == "2":
            question = input("Enter the question: ")
            answer = input("Enter the answer: ")
            ai.learn(question, answer)
            print("AI learned the answer!")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
