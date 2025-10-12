import tkinter as tk
from tkinter import messagebox
import winsound
import random
import time
import threading

class MorseCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code App")
        self.morse_code = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
            'Y': '-.--', 'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
            '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
            ' ': '/'
        }
        self.reverse_mapping = {value: key for key, value in self.morse_code.items()}
        self.speed = 1
        self.create_widgets()

    def create_widgets(self):
        # Create notebook with tabs
        self.notebook = tk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.text_to_morse_frame = tk.Frame(self.notebook)
        self.notebook.add(self.text_to_morse_frame, text="Text to Morse")

        self.morse_to_text_frame = tk.Frame(self.notebook)
        self.notebook.add(self.morse_to_text_frame, text="Morse to Text")

        self.practice_frame = tk.Frame(self.notebook)
        self.notebook.add(self.practice_frame, text="Practice")

        self.quiz_frame = tk.Frame(self.notebook)
        self.notebook.add(self.quiz_frame, text="Quiz")

        self.stats_frame = tk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Stats")

        # Text to Morse tab
        tk.Label(self.text_to_morse_frame, text="Text:").pack()
        self.text_entry = tk.Text(self.text_to_morse_frame, height=10, width=40)
        self.text_entry.pack()
        tk.Button(self.text_to_morse_frame, text="Convert to Morse", command=self.text_to_morse).pack()
        tk.Label(self.text_to_morse_frame, text="Morse Code:").pack()
        self.morse_label = tk.Label(self.text_to_morse_frame, text="")
        self.morse_label.pack()
        tk.Button(self.text_to_morse_frame, text="Play Morse", command=self.play_morse).pack()

        # Morse to Text tab
        tk.Label(self.morse_to_text_frame, text="Morse Code:").pack()
        self.morse_entry = tk.Text(self.morse_to_text_frame, height=10, width=40)
        self.morse_entry.pack()
        tk.Button(self.morse_to_text_frame, text="Convert to Text", command=self.morse_to_text).pack()
        tk.Label(self.morse_to_text_frame, text="Text:").pack()
        self.text_label = tk.Label(self.morse_to_text_frame, text="")
        self.text_label.pack()

        # Practice tab
        tk.Button(self.practice_frame, text="Generate Random Morse Code", command=self.generate_random_morse).pack()
        self.practice_morse_label = tk.Label(self.practice_frame, text="")
        self.practice_morse_label.pack()
        tk.Button(self.practice_frame, text="Play Morse", command=self.play_practice_morse).pack()
        tk.Label(self.practice_frame, text="Enter Text:").pack()
        self.practice_entry = tk.Entry(self.practice_frame)
        self.practice_entry.pack()
        tk.Button(self.practice_frame, text="Check Answer", command=self.check_practice_answer).pack()
        self.practice_result_label = tk.Label(self.practice_frame, text="")
        self.practice_result_label.pack()

        # Quiz tab
        tk.Button(self.quiz_frame, text="Start Quiz", command=self.start_quiz).pack()
        self.quiz_morse_label = tk.Label(self.quiz_frame, text="")
        self.quiz_morse_label.pack()
        tk.Label(self.quiz_frame, text="Enter Text:").pack()
        self.quiz_entry = tk.Entry(self.quiz_frame)
        self.quiz_entry.pack()
        tk.Button(self.quiz_frame, text="Submit", command=self.submit_quiz_answer).pack()
        self.quiz_result_label = tk.Label(self.quiz_frame, text="")
        self.quiz_result_label.pack()
        self.quiz_score = 0
        self.quiz_total = 0

        # Stats tab
        self.stats_label = tk.Label(self.stats_frame, text="Stats:")
        self.stats_label.pack()
        self.practice_score = 0
        self.practice_total = 0
        self.practice_stats_label = tk.Label(self.stats_frame, text=f"Practice Score: {self.practice_score}/{self.practice_total}")
        self.practice_stats_label.pack()
        self.quiz_stats_label = tk.Label(self.stats_frame, text=f"Quiz Score: {self.quiz_score}/{self.quiz_total}")
        self.quiz_stats_label.pack()

        # Speed control
        tk.Label(self.text_to_morse_frame, text="Speed:").pack()
        self.speed_var = tk.StringVar(self.text_to_morse_frame)
        self.speed_var.set("1")
        speed_option = tk.OptionMenu(self.text_to_morse_frame, self.speed_var, "0.5", "1", "2", "5")
        speed_option.pack()
        tk.Button(self.text_to_morse_frame, text="Set Speed", command=self.set_speed).pack()

    def set_speed(self):
        self.speed = float(self.speed_var.get())

    # ... rest of the code remains the same ...

    def check_practice_answer(self):
        try:
            morse = self.practice_morse_label.cget("text")
            morse_chars = morse.split(' ')
            text = ''
            for char in morse_chars:
                if char in self.reverse_mapping:
                    text += self.reverse_mapping[char]
            user_answer = self.practice_entry.get()
            if user_answer.upper() == text:
                self.practice_result_label.config(text="Correct!", fg="green")
                self.practice_score += 1
            else:
                self.practice_result_label.config(text=f"Sorry, the correct answer was {text}", fg="red")
            self.practice_total += 1
            self.practice_stats_label.config(text=f"Practice Score: {self.practice_score}/{self.practice_total}")
        except Exception as e:
            self.practice_result_label.config(text="Error occurred", fg="red")

    def submit_quiz_answer(self):
        try:
            user_answer = self.quiz_entry.get()
            if user_answer.upper() == self.quiz_answer:
                self.quiz_score += 1
                self.quiz_result_label.config(text=f"Correct! Your score is {self.quiz_score}/{self.quiz_total}", fg="green")
            else:
                self.quiz_result_label.config(text=f"Sorry, the correct answer was {self.quiz_answer}. Your score is {self.quiz_score}/{self.quiz_total}", fg="red")
            self.quiz_total += 1
            self.quiz_stats_label.config(text=f"Quiz Score: {self.quiz_score}/{self.quiz_total}")
            self.next_quiz_question()
        except Exception as e:
            self.quiz_result_label.config(text="Error occurred", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = MorseCodeApp(root)
    root.mainloop()