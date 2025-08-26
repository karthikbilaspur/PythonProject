# Importing libraries
import requests
import tkinter as tk
from tkinter import messagebox

class RandomAdvisorApplication:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Random Advisor Application")
        self.advice_text = tk.StringVar()
        self.create_widgets()
        self.fetch_advice()

    def fetch_advice(self):
        try:
            res = requests.get("https://api.adviceslip.com/advice", timeout=5).json()
            advice = res["slip"]["advice"]
            self.advice_text.set(advice)
            self.save_advice_to_history(advice)
        except requests.exceptions.RequestException as e:
            messagebox.showerror(
                "Error", f"Failed to fetch advice. Error: {str(e)}")

    def create_widgets(self):
        advice_label = tk.Label(self.root, textvariable=self.advice_text,
                                wraplength=400, font=("Arial", 14))
        get_advice_button = tk.Button(self.root, text="Get Advice", command=self.fetch_advice)
        refresh_button = tk.Button(self.root, text="Refresh", command=self.fetch_advice)
        history_button = tk.Button(self.root, text="Advice History", command=self.display_advice_history)

        advice_label.pack(pady=20)
        get_advice_button.pack(pady=10)
        refresh_button.pack(pady=5)
        history_button.pack(pady=5)

        # Add a footer label
        footer_label = tk.Label(self.root, text="Powered by Advice Slip API", font=("Arial", 10))
        footer_label.pack(pady=10, side=tk.BOTTOM)

        self.advice_history: list[str] = []

    def save_advice_to_history(self, advice: str) -> None:
        self.advice_history.append(advice)
        if len(self.advice_history) > 10:
            self.advice_history.pop(0)

    def display_advice_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Advice History")
        history_text = tk.Text(history_window, width=50, height=10)
        history_text.pack(pady=10)
        for i, advice in enumerate(self.advice_history):
            history_text.insert(tk.END, f"{i+1}. {advice}\n\n")

def main():
    root = tk.Tk()
    RandomAdvisorApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()