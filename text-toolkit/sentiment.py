import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from typing import Any, cast

import matplotlib.pyplot as plt
from wordcloud import WordCloud as _WordCloud  # pyright: ignore[reportMissingTypeStubs]
import pandas as pd

WordCloud: Any = cast(Any, _WordCloud)
_plt: Any = cast(Any, plt)
_sia = None


def get_analyzer() -> Any:
    global _sia
    if _sia is None:
        import nltk as _nltk  # pyright: ignore[reportMissingTypeStubs]

        nltk: Any = cast(Any, _nltk)
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            nltk.download("vader_lexicon", quiet=True)
        from nltk.sentiment.vader import SentimentIntensityAnalyzer  # pyright: ignore[reportMissingTypeStubs]

        _sia = SentimentIntensityAnalyzer()
    return _sia

def open_sentiment_window(parent: tk.Misc) -> None:
    win = tk.Toplevel(parent)
    win.title("Sentiment Analysis")
    win.geometry("600x550")
    tk.Label(win, text="Enter text:").pack(pady=5)
    input_text = scrolledtext.ScrolledText(win, height=10, width=65)
    input_text.pack(padx=10)
    result_label = tk.Label(win, text="", justify="left", font=("Arial", 11))
    result_label.pack(pady=10)
    state: dict[str, dict[str, str | float] | None] = {"result": None}

    def analyze():
        text = input_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Empty", "Please enter some text first.")
            return
        sia = get_analyzer()
        s = sia.polarity_scores(text)
        label = "Positive" if s["compound"] >= 0.05 else "Negative" if s["compound"] <= -0.05 else "Neutral"
        state["result"] = {"Sentiment": label, "Positive": round(s["pos"], 2), "Negative": round(s["neg"], 2), "Neutral": round(s["neu"], 2), "Compound": round(s["compound"], 2)}
        result_label.config(text=f"Sentiment: {label}\nPositive: {s['pos']:.2f}  Negative: {s['neg']:.2f}  Neutral: {s['neu']:.2f}  Compound: {s['compound']:.2f}")

    def load_file():
        p = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])
        if p:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                input_text.delete("1.0", tk.END)
                input_text.insert("1.0", f.read())

    def save_result():
        if not state["result"]:
            messagebox.showerror("Error", "No analysis result available! Analyze first.")
            return
        p = filedialog.asksaveasfilename(title="Save Analysis Result", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if p:
            pd.DataFrame([state["result"]]).to_csv(p, index=False)
            messagebox.showinfo("Success", "Analysis result saved successfully!")

    def wordcloud():
        text = input_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Empty", "Please enter some text first.")
            return
        wc = WordCloud(width=800, height=400, background_color="white").generate(text)
        _plt.figure(figsize=(10, 5))
        _plt.imshow(wc, interpolation="bilinear")
        _plt.axis("off")
        _plt.show()

    tk.Button(win, text="Analyze Sentiment", command=analyze).pack(pady=3)
    tk.Button(win, text="Load Text File", command=load_file).pack(pady=3)
    tk.Button(win, text="Save Analysis Result", command=save_result).pack(pady=3)
    tk.Button(win, text="Generate Word Cloud", command=wordcloud).pack(pady=3)
