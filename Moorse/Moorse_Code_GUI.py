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

        # Speed control
        tk.Label(self.text_to_morse_frame, text="Speed:").pack()
        self.speed_var = tk.StringVar(self.text_to_morse_frame)
        self.speed_var.set("1")
        speed_option = tk.OptionMenu(self.text_to_morse_frame, self.speed_var, "0.5", "1", "2", "5")
        speed_option.pack()
        tk.Button(self.text_to_morse_frame, text="Set Speed", command=self.set_speed).pack()

    def set_speed(self):
        self.speed = float(self.speed_var.get())

    def text_to_morse(self):
        text = self.text_entry.get("1.0", "end-1c")
        morse = ''
        for char in text.upper():
            if char in self.morse_code:
                morse += self.morse_code[char] + ' '
        self.morse_label.config(text=morse)

    def morse_to_text(self):
        morse = self.morse_entry.get("1.0", "end-1c")
        text = ''
        morse_chars = morse.split(' ')
        for char in morse_chars:
            if char in self.reverse_mapping:
                text += self.reverse_mapping[char]
        self.text_label.config(text=text)

    def play_morse(self):
        morse = self.morse_label.cget("text")
        threading.Thread(target=self.play_morse_code, args=(morse,)).start()

    def play_morse_code(self, morse):
        for char in morse:
            if char == '.':
                winsound.Beep(1000, int(100 / self.speed))
                time.sleep(0.1 / self.speed)
            elif char == '-':
                winsound.Beep(1000, int(300 / self.speed))
                time.sleep(0.3 / self.speed)
            elif char == ' ':
                time.sleep(0.2 / self.speed)
            elif char == '/':
                time.sleep(0.5 / self.speed)

    def generate_random_morse(self):
        text = ''.join(random.choice(list(self.morse_code.keys())) for _ in range(10))
        morse = ''
        for char in text.upper():
            if char in self.morse_code:
                morse += self.morse_code[char] + ' '
        self.practice_morse_label.config(text=morse)

    def play_practice_morse(self):
        morse = self.practice_morse_label.cget("text")
        threading.Thread(target=self.play_morse_code, args=(morse,)).start()

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
               self.practice_result_label.config(text="Correct!")
           else:
               self.practice_result_label.config(text=f"Sorry, the correct answer was {text}")

def start_quiz(self):
    try:
       self.quiz_score = 0
       self.quiz_total = 0
       self.next_quiz_question()

def next_quiz_question(self):
    try: 
       self.quiz_total += 1
    text = ''.join(random.choice(list(self.morse_code.keys())) for _ in range(5))
    morse = ''
    for char in text.upper():
        if char in self.morse_code:
            morse += self.morse_code[char] + ' '
    self.quiz_morse_label.config(text=morse)
    self.quiz_answer = text
    self.quiz_entry.delete(0, tk.END)

def submit_quiz_answer(self):
    user_answer = self.quiz_entry.get()
    if user_answer.upper() == self.quiz_answer:
        self.quiz_score += 1
        self.quiz_result_label.config(text=f"Correct! Your score is {self.quiz_score}/{self.quiz_total}")
    else:
        self.quiz_result_label.config(text=f"Sorry, the correct answer was {self.quiz_answer}. Your score is {self.quiz_score}/{self.quiz_total}")
    self.next_quiz_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = MorseCodeApp(root)
    root.mainloop()