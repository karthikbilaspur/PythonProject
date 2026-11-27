import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from collections import Counter
from collections.abc import Callable
from typing import Any, cast

def _ensure_nltk():
    import nltk  # type: ignore[import-untyped]
    nltk_api = cast(Any, nltk)
    for pkg, path in [("punkt", "tokenizers/punkt"), ("punkt_tab", "tokenizers/punkt_tab"), ("stopwords", "corpora/stopwords")]:
        try:
            cast(Callable[[str], object], nltk_api.data.find)(path)
        except LookupError:
            try:
                cast(Callable[..., object], nltk_api.download)(pkg, quiet=True)
            except Exception:
                pass

def summarize_text_logic(text: str, max_sentences: int = 5) -> str:
    _ensure_nltk()
    from nltk.corpus import stopwords  # type: ignore[import-untyped]
    from nltk.tokenize import sent_tokenize, word_tokenize  # type: ignore[import-untyped]

    stopwords_api = cast(Any, stopwords)
    tokenize_sentences = cast(Callable[[str], list[str]], sent_tokenize)
    tokenize_words = cast(Callable[[str], list[str]], word_tokenize)
    text = text.strip()
    if not text:
        return ""
    sentences = tokenize_sentences(text)
    if len(sentences) <= max_sentences:
        return text
    get_stopwords = cast(Callable[[str], list[str]], stopwords_api.words)
    stop_words = set(get_stopwords("english"))
    words = [w for w in tokenize_words(text.lower()) if w.isalnum() and w not in stop_words]
    if not words:
        return " ".join(sentences[:max_sentences])
    freq = Counter(words)
    scores: dict[str, float] = {}
    for sent in sentences:
        sentence_words = tokenize_words(sent.lower())
        score = sum(freq.get(w, 0) for w in sentence_words)
        scores[sent] = score / (len(sentence_words) ** 0.5)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
    picked = [s for s in sentences if s in dict(ranked)]
    return " ".join(picked)

def open_summarizer_window(parent: tk.Misc) -> None:
    win = tk.Toplevel(parent)
    win.title("Text Summarizer")
    win.geometry("600x550")
    tk.Label(win, text="Enter text:").pack(pady=5)
    input_text = scrolledtext.ScrolledText(win, height=10, width=65)
    input_text.pack(padx=10)
    tk.Label(win, text="Summary:").pack(pady=5)
    summary_text = scrolledtext.ScrolledText(win, height=7, width=65)
    summary_text.pack(padx=10)

    def do_summarize():
        text = input_text.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Empty", "Please enter some text first.")
            return
        summary = summarize_text_logic(text, max_sentences=5)
        summary_text.delete("1.0", tk.END)
        summary_text.insert("1.0", summary)

    def load_file():
        p = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])
        if p:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                input_text.delete("1.0", tk.END)
                input_text.insert("1.0", f.read())

    def save_summary():
        summary = summary_text.get("1.0", "end-1c").strip()
        if not summary:
            messagebox.showerror("Error", "No summary to save!")
            return
        p = filedialog.asksaveasfilename(title="Save Summary", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if p:
            with open(p, "w", encoding="utf-8") as f:
                f.write(summary)
            messagebox.showinfo("Success", "Summary saved successfully!")

    tk.Button(win, text="Summarize Text", command=do_summarize).pack(pady=3)
    tk.Button(win, text="Load Text File", command=load_file).pack(pady=3)
    tk.Button(win, text="Save Summary", command=save_summary).pack(pady=3)
