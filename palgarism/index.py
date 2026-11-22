import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from difflib import SequenceMatcher
from typing import Any

import nltk  # type: ignore[reportMissingTypeStubs]
from nltk.corpus import stopwords  # type: ignore[reportMissingTypeStubs]
from nltk.tokenize import word_tokenize  # type: ignore[reportMissingTypeStubs]
from nltk.stem import PorterStemmer  # type: ignore[reportMissingTypeStubs]
import requests
import docx  # type: ignore[reportMissingImports]

# PyPDF2 is deprecated -> use maintained fork pypdf (same API).
# Falls back to PyPDF2 if pypdf is not installed.
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

# BeautifulSoup is optional: used only to strip HTML from URLs.
try:
    from bs4 import BeautifulSoup
    has_bs4 = True
except ImportError:
    has_bs4 = False


# --- Download NLTK data only if missing (don't re-download every run) ---
# NLTK 3.9+ : word_tokenize() needs punkt_tab, not just punkt.
for _resource, _path in [
    ("punkt", "tokenizers/punkt"),
    ("punkt_tab", "tokenizers/punkt_tab"),
    ("stopwords", "corpora/stopwords"),
]:
    try:
        nltk.data.find(_path)  # type: ignore[reportUnknownMemberType]
    except LookupError:
        nltk.download(_resource)  # type: ignore[reportUnknownMemberType]

class PlagiarismChecker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Plagiarism Checker - Merged (Fixed)")
        self.window.geometry("700x750")

        # Cache stopwords + stemmer once instead of rebuilding per call.
        self._stop_words = set(stopwords.words("english"))  # type: ignore[reportUnknownMemberType]
        self._stemmer = PorterStemmer()

        # ---------- Source 1: Manual Text ----------
        tk.Label(self.window, text="Text 1 - Enter Text Manually:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.text_entry = scrolledtext.ScrolledText(self.window, height=7, width=75)
        self.text_entry.pack(padx=10)

        # ---------- Source 1: File ----------
        file_frame = tk.Frame(self.window)
        file_frame.pack(pady=5)
        tk.Button(file_frame, text="Load Text 1 from File (.txt/.docx/.pdf)", command=self.load_file1).pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="Load Text 1 from URL", command=self.load_url1).pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="Clear Text 1", command=self.clear_text1).pack(side=tk.LEFT, padx=5)
        self.file1_label = tk.Label(self.window, text="No file loaded for Text 1", fg="gray")
        self.file1_label.pack()

        # ---------- Source 2 ----------
        tk.Label(self.window, text="Text 2 - Comparison Text:", font=("Arial", 10, "bold")).pack(pady=(15, 0))
        self.text2_entry = scrolledtext.ScrolledText(self.window, height=7, width=75)
        self.text2_entry.pack(padx=10)

        file2_frame = tk.Frame(self.window)
        file2_frame.pack(pady=5)
        tk.Button(file2_frame, text="Load Text 2 from File (.txt/.docx/.pdf)", command=self.load_file2).pack(side=tk.LEFT, padx=5)
        tk.Button(file2_frame, text="Load Text 2 from URL", command=self.load_url2).pack(side=tk.LEFT, padx=5)
        tk.Button(file2_frame, text="Clear Text 2", command=self.clear_text2).pack(side=tk.LEFT, padx=5)
        self.file2_label = tk.Label(self.window, text="No file loaded for Text 2", fg="gray")
        self.file2_label.pack()

        # ---------- Options ----------
        opt_frame = tk.Frame(self.window)
        opt_frame.pack(pady=10)
        self.ignore_stop_words = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Ignore stop words", variable=self.ignore_stop_words).pack(side=tk.LEFT, padx=10)
        self.use_stemming = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Use stemming", variable=self.use_stemming).pack(side=tk.LEFT, padx=10)
        self.ignore_case = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Ignore case", variable=self.ignore_case).pack(side=tk.LEFT, padx=10)

        # ---------- Check Button ----------
        tk.Button(self.window, text="CHECK PLAGIARISM", font=("Arial", 11, "bold"),
                  bg="#4CAF50", fg="white", padx=20, pady=5,
                  command=self.check_plagiarism).pack(pady=10)

        # ---------- Result ----------
        tk.Label(self.window, text="Result:", font=("Arial", 10, "bold")).pack()
        self.result_text = scrolledtext.ScrolledText(self.window, height=10, width=75)
        self.result_text.pack(padx=10, pady=(0, 10))

    # ---------- Clear helpers (also reset labels) ----------
    def clear_text1(self):
        self.text_entry.delete("1.0", tk.END)
        self.file1_label.config(text="No file loaded for Text 1")

    def clear_text2(self):
        self.text2_entry.delete("1.0", tk.END)
        self.file2_label.config(text="No file loaded for Text 2")

    # ---------- File / URL Loading ----------
    def read_file(self, file_path: str) -> str:
        # FIX: case-insensitive extension check (.PDF / .DOCX / .TXT)
        lower = file_path.lower()
        if lower.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        elif lower.endswith(".docx"):
            docx_module: Any = docx
            doc: Any = docx_module.Document(file_path)
            return "\n".join(str(paragraph.text) for paragraph in doc.paragraphs)
        elif lower.endswith(".pdf"):
            reader = PdfReader(file_path)
            # FIX: encrypted PDFs used to crash here.
            if getattr(reader, "is_encrypted", False):
                try:
                    reader.decrypt("")
                except Exception:
                    raise ValueError("PDF is encrypted and cannot be read.")
                if getattr(reader, "is_encrypted", False):
                    raise ValueError("PDF is encrypted and cannot be read.")
            texts: list[str] = []
            for page in reader.pages:
                # extract_text() returns None for scanned/image PDFs - skip those.
                t = page.extract_text()
                if t:
                    texts.append(t)
            text = "\n".join(texts)
            if not text.strip():
                raise ValueError("No extractable text found in PDF (it may be scanned/image-based).")
            return text
        else:
            raise ValueError("Unsupported file format. Use .txt, .docx, or .pdf")

    def load_file1(self):
        path = filedialog.askopenfilename(filetypes=[("Supported", "*.txt *.docx *.pdf"), ("All files", "*.*")])
        if path:
            try:
                text = self.read_file(path)
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert(tk.END, text)
                # FIX: show basename only, full path overflows the window.
                self.file1_label.config(text=f"Loaded: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_file2(self):
        path = filedialog.askopenfilename(filetypes=[("Supported", "*.txt *.docx *.pdf"), ("All files", "*.*")])
        if path:
            try:
                text = self.read_file(path)
                self.text2_entry.delete("1.0", tk.END)
                self.text2_entry.insert(tk.END, text)
                self.file2_label.config(text=f"Loaded: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _fetch_url_text(self, url: str) -> str:
        """Fetch a URL and return visible text, not raw HTML."""
        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (PlagiarismChecker)"},
        )
        resp.raise_for_status()
        html = resp.text
        if has_bs4:
            soup = BeautifulSoup(html, "html.parser")
            # Drop non-visible elements that would pollute similarity.
            for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
                tag.decompose()
            return soup.get_text(separator="\n")
        # Fallback if beautifulsoup4 is not installed: crude tag strip.
        text = re.sub(r"<script.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def load_url1(self):
        url = self.ask_for_url("Enter URL for Text 1")
        if url:
            try:
                text = self._fetch_url_text(url)
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert(tk.END, text)
                self.file1_label.config(text=f"Loaded from URL: {url}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_url2(self):
        url = self.ask_for_url("Enter URL for Text 2")
        if url:
            try:
                text = self._fetch_url_text(url)
                self.text2_entry.delete("1.0", tk.END)
                self.text2_entry.insert(tk.END, text)
                self.file2_label.config(text=f"Loaded from URL: {url}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def ask_for_url(self, title: str):
        """FIXED version of V1's get_comparison_url - actually returns the value"""
        result: dict[str, str | None] = {"url": None}
        popup = tk.Toplevel(self.window)
        popup.title(title)
        popup.geometry("400x120")
        popup.grab_set()

        tk.Label(popup, text="Enter URL:").pack(pady=5)
        entry = tk.Entry(popup, width=50)
        entry.pack(pady=5)
        entry.focus()

        def on_ok():
            result["url"] = entry.get().strip()
            popup.destroy()

        tk.Button(popup, text="OK", command=on_ok).pack(pady=5)
        popup.bind("<Return>", lambda e: on_ok())
        self.window.wait_window(popup)
        return result["url"]

    # ---------- Core Logic ----------
    def preprocess(self, text: str) -> list[str]:
        if self.ignore_case.get():
            text = text.lower()

        words: list[str] = word_tokenize(text)
        words = [w for w in words if w.isalpha()]  # removes punctuation

        if self.ignore_stop_words.get():
            words = [w for w in words if w not in self._stop_words]
        if self.use_stemming.get():
            stemmer: Any = self._stemmer
            words = [str(stemmer.stem(w)) for w in words]
        return words

    def calculate_similarity(
        self, tokens1: list[str], tokens2: list[str]
    ) -> tuple[float, float, float]:
        """Return (combined, jaccard, sequence) so the UI can show the breakdown."""
        if not tokens1 and not tokens2:
            return 1.0, 1.0, 1.0
        if not tokens1 or not tokens2:
            return 0.0, 0.0, 0.0

        # Jaccard - catches copy-paste / same words
        set1, set2 = set(tokens1), set(tokens2)
        jaccard = len(set1 & set2) / len(set1 | set2) if (set1 | set2) else 0.0

        # SequenceMatcher on TOKENS (not characters) - catches order.
        # NOTE: this is O(N^2)-ish. For very long docs it will be slow -
        # see MAX_SEQ_TOKENS guard in check_plagiarism().
        seq = SequenceMatcher(None, tokens1, tokens2).ratio()

        return (jaccard + seq) / 2, jaccard, seq

    def check_plagiarism(self):
        text1 = self.text_entry.get("1.0", tk.END).strip()
        text2 = self.text2_entry.get("1.0", tk.END).strip()

        if not text1 or not text2:
            messagebox.showerror("Error", "Please provide both texts.\nPaste, load from file, or load from URL.")
            return

        try:
            tokens1 = self.preprocess(text1)
            tokens2 = self.preprocess(text2)

            # FIX: raw text non-empty but tokens empty (e.g. only stopwords)
            # used to report a false 100% similarity.
            if not tokens1 or not tokens2:
                messagebox.showwarning(
                    "Warning",
                    "No meaningful words left after preprocessing.\n"
                    "Try disabling 'Ignore stop words' or adding more text.",
                )
                return

            # Guard against SequenceMatcher hanging on huge documents.
            # Above this size, use Jaccard only (fast, order-insensitive).
            MAX_SEQ_TOKENS = 3000
            if len(tokens1) > MAX_SEQ_TOKENS or len(tokens2) > MAX_SEQ_TOKENS:
                set1, set2 = set(tokens1), set(tokens2)
                jaccard = len(set1 & set2) / len(set1 | set2) if (set1 | set2) else 0.0
                score, jaccard_score, seq_score = jaccard, jaccard, None
                seq_note = " (Sequence skipped: text too long)"
            else:
                combined, jaccard_score, seq_score = self.calculate_similarity(tokens1, tokens2)
                score = combined
                seq_note = ""

            score_pct = score * 100

            if score_pct > 70:
                verdict = "High similarity detected. Possible plagiarism."
            elif score_pct > 40:
                verdict = "Moderate similarity detected. Possible partial plagiarism."
            else:
                verdict = "Low similarity detected. No plagiarism detected."

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Similarity: {score_pct:.2f}%{seq_note}\n")
            if seq_score is None:
                self.result_text.insert(tk.END, f"  Jaccard: {jaccard_score * 100:.2f}% | Sequence: skipped\n")
            else:
                self.result_text.insert(tk.END, f"  Jaccard: {jaccard_score * 100:.2f}% | Sequence: {seq_score * 100:.2f}%\n")
            self.result_text.insert(tk.END, f"{verdict}\n\n")
            self.result_text.insert(tk.END, f"Text 1 words (after processing): {len(tokens1)} | Unique: {len(set(tokens1))}\n")
            self.result_text.insert(tk.END, f"Text 2 words (after processing): {len(tokens2)} | Unique: {len(set(tokens2))}\n")
            self.result_text.insert(tk.END, f"Common unique words: {len(set(tokens1) & set(tokens2))}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    checker = PlagiarismChecker()
    checker.run()