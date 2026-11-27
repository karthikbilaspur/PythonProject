import tkinter as tk
from collections.abc import Callable
from sentiment import open_sentiment_window  # pyright: ignore[reportUnknownVariableType]
from summarizer import open_summarizer_window  # pyright: ignore[reportUnknownVariableType]
from analyser import open_analyser_window
from sheets import open_sheets_window  # pyright: ignore[reportUnknownVariableType]

def main():
    root = tk.Tk()
    root.title("Text Toolkit - 4 Tools in 1")
    root.geometry("420x420")
    tk.Label(root, text="Text Toolkit", font=("Arial", 18, "bold")).pack(pady=15)
    tk.Label(root, text="Pick a tool. Each opens in its own window.", fg="gray").pack(pady=5)
    buttons: list[tuple[str, Callable[[tk.Tk], None]]] = [
        ("1. Sentiment Analysis", open_sentiment_window),
        ("2. Text Summarizer", open_summarizer_window),
        ("3. Text File Analyser", open_analyser_window),
        ("4. Text to Sheets", open_sheets_window),
    ]
    for label, func in buttons:
        tk.Button(root, text=label, width=30, height=2, command=lambda f=func: f(root)).pack(pady=8)
    tk.Label(root, text="Run:  python app.py", fg="gray").pack(pady=15)
    root.mainloop()

if __name__ == "__main__":
    main()
