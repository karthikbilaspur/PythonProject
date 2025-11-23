import tkinter as tk
import random
import time

class TypingSpeedTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")
        self.difficulty_level = tk.StringVar(self.root)
        self.difficulty_level.set("Easy")
        self.timer = tk.StringVar(self.root)
        self.timer.set("1 minute")
        self.score = {"speed": 0, "accuracy": 0}
        self.text_to_type = ""
        self.start_time = 0
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Typing Speed Test", font=("Arial", 24)).pack()
        tk.Label(self.root, text="Difficulty Level:").pack()
        tk.OptionMenu(self.root, self.difficulty_level, "Easy", "Medium", "Hard").pack()
        tk.Label(self.root, text="Timer:").pack()
        tk.OptionMenu(self.root, self.timer, "1 minute", "2 minutes", "3 minutes").pack()
        tk.Button(self.root, text="Start", command=self.start_test).pack()
        self.text_label = tk.Label(self.root, text="", wraplength=400, font=("Arial", 18))
        self.text_label.pack()
        self.entry = tk.Text(self.root, height=10, width=50, font=("Arial", 18))
        self.entry.pack()
        tk.Button(self.root, text="Submit", command=self.check_typing_speed).pack()
        self.result_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.result_label.pack()
        tk.Button(self.root, text="Practice Mode", command=self.practice_mode).pack()
        tk.Button(self.root, text="View Score", command=self.view_score).pack()

    def start_test(self):
        self.text_to_type = self.generate_text()
        self.text_label.config(text=self.text_to_type)
        self.start_time = time.time()
        self.entry.delete("1.0", tk.END)

    def generate_text(self):
        texts = {
            "Easy": ["The quick brown fox jumps over the lazy dog", "Python is a popular programming language"],
            "Medium": ["The sun was shining brightly in the clear blue sky", "The cat purrs contentedly on my lap"],
            "Hard": ["The complexity of the human brain is still not fully understood", "The universe is a vast and mysterious place"]
        }
        return random.choice(texts[self.difficulty_level.get()])

    def check_typing_speed(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        typed_text = self.entry.get("1.0", tk.END).strip()
        accuracy = self.calculate_accuracy(typed_text)
        speed = self.calculate_speed(typed_text, elapsed_time)
        self.score["speed"] = speed
        self.score["accuracy"] = accuracy
        result = f"Accuracy: {accuracy:.2f}%\nSpeed: {speed:.2f} words per minute"
        self.result_label.config(text=result)

    def calculate_accuracy(self, typed_text):
        correct_chars = sum(1 for a, b in zip(typed_text, self.text_to_type) if a == b)
        accuracy = (correct_chars / len(self.text_to_type)) * 100
        return accuracy

    def calculate_speed(self, typed_text, elapsed_time):
        num_words = len(typed_text.split())
        speed = (num_words / elapsed_time) * 60
        return speed

    def practice_mode(self):
        self.text_to_type = self.generate_text()
        self.text_label.config(text=self.text_to_type)
        self.entry.delete("1.0", tk.END)

    def view_score(self):
        result = f"Accuracy: {self.score['accuracy']:.2f}%\nSpeed: {self.score['speed']:.2f} words per minute"
        self.result_label.config(text=result)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    typing_speed_test = TypingSpeedTest()
    typing_speed_test.run()