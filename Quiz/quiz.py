import tkinter as tk
from tkinter import ttk
from question_api import QuestionAPI
from utils import destroy_widgets

class QuizApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Time")
        self.root.geometry("900x300+200+200")
        self.question_api = QuestionAPI()
        self.score = [0] * 10
        self.current_question = 0
        self.questions = []
        self.options = []
        self.correct_answers = []

    def run(self):
        self.welcome_window()

    def welcome_window(self):
        # Welcome message
        self.label_1 = tk.Label(self.root, text="Welcome to the Quiz!", width=30, font=("bold", 15))
        self.label_1.pack(padx=10, pady=30)

        # Start Quiz button
        self.btn_1 = ttk.Button(self.root, text="Start Quiz", command=lambda: destroy_widgets(self.root) or self.choices())
        self.btn_1.pack()

    def choices(self):
        # user's category and difficulty level preference are taken here
        self.category_choice = ttk.Combobox(self.root, values=["Random Category", "General Knowledge", "Books", "Movies", "Music", "Television", "Video Games",
                                                              "Science and Nature", "Computers", "Mathematics", "Mythology", "Sports",
                                                              "Geography", "History", "Animals", "Celebrities", "Anime and Manga",
                                                              "Cartoons and Animations", "Comics"])
        self.category_choice.current(0)
        self.category_choice.pack()

        self.difficulty_choice = ttk.Combobox(self.root, values=["Easy", "Medium", "Hard"])
        self.difficulty_choice.current(1)
        self.difficulty_choice.pack()

        self.btn_1 = ttk.Button(self.root, text="Go", command=lambda: destroy_widgets(self.root) or self.get_questions())
        self.btn_1.pack()

    def get_questions(self):
        # Chosen Category and Difficulty level are displayed here for confirmation
        # The user is also allowed to go back and change their preference
        self.category = self.category_choice.get()
        self.difficulty = self.difficulty_choice.get()
        self.questions_api(self.category, self.difficulty)
        self.print_question(0)

    def print_question(self, index):
        # function is recursively called to print each question
        # there are a total of 10 questions
        if index < 10:
            # label to display question number
            self.label_1 = tk.Label(self.root, text="Question "+str(index+1), font=('bold', 11))
            self.label_1.pack()

            # a label to display the question text
            # wraplength used to make sure the text doesn't flow out of the screen
            self.label_2 = tk.Label(self.root, text=self.questions[index], font=('bold', 11), wraplength=700, justify=tk.CENTER)
            self.label_2.pack()

            # buttons to display options
            for i, option in enumerate(self.options[index]):
                btn = tk.Button(self.root, text=option, command=lambda index=index, option=option: self.score_updater(index, option))
                btn.pack()

            # button to navigate to previous question
            if index > 0:
                self.btn_2 = ttk.Button(self.root, text="Go to Previous Question",
                                        command=lambda: destroy_widgets(self.root) or self.print_question(index-1))
                self.btn_2.pack()

        else:
            # once 10 questions have been printed we move onto here
            # a buffer window before we print the score
            self.get_score()

    def score_updater(self, question, option):
        # function is called every time the user answers a question
        if option == self.correct_answers[question]:
            self.score[question] = 1
        else:
            self.score[question] = 0
        destroy_widgets(self.root)
        self.print_question(question + 1)

    def get_score(self):
        # window to display score
        score = sum(self.score)
        self.label_1 = tk.Label(self.root, text="Your Score is: " + str(score), font=("bold", 12))
        self.label_1.pack()

    def questions_api(self, category, difficulty):
        # questions for the quiz are retrieved using an api
        # api link https://opentdb.com/api_config.php
        self.questions, self.options, self.correct_answers = self.question_api.get_questions(category, difficulty)