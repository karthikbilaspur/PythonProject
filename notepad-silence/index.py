"""
Notepad + Spell Check Suite - Mixed from 3 files
  1. Notepad (Tkinter) - New / Open / Save / Cut / Copy / Paste / About
  2. ML Spell Checker (TF-IDF + Naive Bayes) - learns correct vs typo
  3. Edit-Distance Spell Checker (NLTK + Brown) - suggests corrections

NEW mixed features:
- Tools menu inside Notepad: Check Spelling, Suggestions, ML Check
- Unknown words highlighted in red, click suggestion to replace
- Status bar: words, chars, spelling errors
- Works WITHOUT ML libs: edit-distance checker is default
- ML checker is lazy: only trains when you click it

Run: python index.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os, re
import importlib
from collections import Counter
from typing import Any, Callable, Optional, cast

# ============================================================
# SPELL CHECK ENGINE 1 - Edit Distance (from File 3)
# Fast, no training, no sklearn needed. Default checker.
# ============================================================
class EditDistanceChecker:
    def __init__(self):
        self.english_words: set[str] = set()
        self.brown_freq: Counter[str] = Counter()
        self.loaded: bool = False

    def load(self):
        if self.loaded:
            return True
        try:
            nltk = cast(Any, importlib.import_module("nltk"))
            corpus = cast(Any, importlib.import_module("nltk.corpus"))
            words = corpus.words
            brown = corpus.brown
            try:
                nltk.download('words', quiet=True)
                nltk.download('brown', quiet=True)
            except Exception:
                pass
            word_list = cast(list[str], words.words())
            self.english_words = set(w.lower() for w in word_list)
            brown_words = cast(list[str], brown.words())
            self.brown_freq = Counter(w.lower() for w in brown_words)
            self.loaded = True
            return True
        except Exception as e:
            print(f"NLTK load failed: {e}")
            # Fallback: small built-in wordlist so app still works offline
            self.english_words = set("""
                the be to of and a in that it was for on are as with his they i at be this have from or one had by word
                hello world python code text file notepad spell check sample this is with some errors
                """.split())
            self.brown_freq = Counter({w: 1 for w in self.english_words})
            self.loaded = True
            return True

    def is_correct(self, word: str) -> bool:
        self.load()
        return word.lower() in self.english_words

    def suggest_corrections(self, word: str, max_dist: int = 2, top_n: int = 5) -> list[str]:
        """From File 3: edit_distance <= 2, ranked by Brown frequency."""
        self.load()
        word = word.lower()

        def edit_distance(first: str, second: str) -> int:
            previous = list(range(len(second) + 1))
            for i, first_char in enumerate(first, start=1):
                current = [i]
                for j, second_char in enumerate(second, start=1):
                    current.append(min(
                        current[-1] + 1,
                        previous[j] + 1,
                        previous[j - 1] + (first_char != second_char),
                    ))
                previous = current
            return previous[-1]

        candidates = [w for w in self.english_words if edit_distance(w, word) <= max_dist]
        ranked = sorted(candidates, key=lambda x: self.brown_freq.get(x, 0), reverse=True)
        return ranked[:top_n]

    def check_text(self, text: str) -> list[tuple[str, int, list[str]]]:
        """Returns list of (word, start_index_in_text, suggestions) for unknown words."""
        self.load()
        results: list[tuple[str, int, list[str]]] = []
        for m in re.finditer(r"\b\w+\b", text):
            w = m.group(0)
            if w.lower() not in self.english_words:
                results.append((w, m.start(), self.suggest_corrections(w)))
        return results


# ============================================================
# SPELL CHECK ENGINE 2 - ML (from File 2)
# TF-IDF + Naive Bayes, trained on correct words + synthetic typos.
# Lazy + sampled so it doesn't freeze Notepad on startup.
# ============================================================
class MLChecker:
    def __init__(self):
        self.vectorizer: Any = None
        self.clf: Any = None
        self.trained = False
        self.accuracy: Optional[float] = None

    def train(
        self,
        sample_size: int = 3000,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> bool:
        """Trains like File 2, but on a SAMPLE for speed. Call only on demand."""
        if self.trained:
            return True
        try:
            if progress_callback is not None:
                progress_callback("Preparing training data...")
            pd = cast(Any, importlib.import_module("pandas"))
            sklearn_vectorizers = cast(Any, importlib.import_module("sklearn.feature_extraction.text"))
            sklearn_model_selection = cast(Any, importlib.import_module("sklearn.model_selection"))
            sklearn_metrics = cast(Any, importlib.import_module("sklearn.metrics"))
            sklearn_bayes = cast(Any, importlib.import_module("sklearn.naive_bayes"))
            nltk = cast(Any, importlib.import_module("nltk"))
            corpus = cast(Any, importlib.import_module("nltk.corpus"))
            words = corpus.words
            import random
            nltk.download('words', quiet=True)
            english = list(set(w.lower() for w in cast(list[str], words.words())))
            random.shuffle(english)
            english = english[:sample_size]
            text_data: list[str] = []
            labels: list[int] = []
            for word in english:
                if random.random() < 0.5:
                    typo_type = random.choice(['insert', 'delete', 'replace'])
                    if typo_type == 'insert':
                        typo = word + random.choice('abcdefghijklmnopqrstuvwxyz')
                    elif typo_type == 'delete':
                        typo = word[:-1] if len(word) > 1 else word
                    else:
                        typo = word[:-1] + random.choice('abcdefghijklmnopqrstuvwxyz')
                    text_data.append(typo)
                    labels.append(0)
                text_data.append(word)
                labels.append(1)
            df = pd.DataFrame({'text': text_data, 'label': labels})
            split_data = sklearn_model_selection.train_test_split
            X_train, X_test, y_train, y_test = split_data(
                df['text'], df['label'], test_size=0.2, random_state=42)
            self.vectorizer = sklearn_vectorizers.TfidfVectorizer()
            X_train_tfidf = self.vectorizer.fit_transform(X_train)
            X_test_tfidf = self.vectorizer.transform(X_test)
            self.clf = sklearn_bayes.MultinomialNB()
            self.clf.fit(X_train_tfidf, y_train)
            self.accuracy = float(sklearn_metrics.accuracy_score(y_test, self.clf.predict(X_test_tfidf)))
            self.trained = True
            if progress_callback is not None:
                progress_callback("Training complete.")
            return True
        except ImportError as e:
            print(f"ML libs missing: {e}")
            return False

    def predict(self, word: str) -> Optional[int]:
        if not self.trained or self.vectorizer is None or self.clf is None:
            return None
        tfidf = self.vectorizer.transform([word])
        return int(self.clf.predict(tfidf)[0])  # 1=correct, 0=incorrect


# ============================================================
# NOTEPAD (from File 1) + Spell Check mixed in
# ============================================================
class Notepad:
    def __init__(self, **kwargs: int):
        self.__root = tk.Tk()
        self.__root.title("Untitled - Notepad + Spell Check")
        self.__file = None
        self.__thisWidth = kwargs.get('width', 600)
        self.__thisHeight = kwargs.get('height', 400)

        # Spell engines
        self.edit_checker = EditDistanceChecker()
        self.ml_checker = MLChecker()
        self.error_positions: list[tuple[str, str, str, list[str]]] = []

        self.__create_widgets()
        self.__configure_window()
        self.__create_menu_items()
        self.__create_status_bar()

    def __create_widgets(self):
        self.__thisTextArea = tk.Text(self.__root, wrap=tk.WORD, undo=True, font=("Consolas", 12))
        self.__thisScrollBar = tk.Scrollbar(self.__thisTextArea)
        self.__thisMenuBar = tk.Menu(self.__root)
        self.__thisFileMenu = tk.Menu(self.__thisMenuBar, tearoff=0)
        self.__thisEditMenu = tk.Menu(self.__thisMenuBar, tearoff=0)
        self.__thisToolsMenu = tk.Menu(self.__thisMenuBar, tearoff=0)
        self.__thisHelpMenu = tk.Menu(self.__thisMenuBar, tearoff=0)
        # Red highlight for misspelled words
        self.__thisTextArea.tag_config("misspelled", foreground="red", underline=True)

    def __configure_window(self):
        try:
            cast(Any, self.__root).wm_iconbitmap("Notepad.ico")
        except tk.TclError:
            pass
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        left = (sw / 2) - (self.__thisWidth / 2)
        top = (sh / 2) - (self.__thisHeight / 2)
        self.__root.geometry(f'{self.__thisWidth}x{self.__thisHeight}+{int(left)}+{int(top)}')
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__thisTextArea.grid(sticky="nsew")
        self.__thisScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__thisScrollBar.config(command=cast(Any, self.__thisTextArea).yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)
        # Live word count
        self.__thisTextArea.bind("<<Modified>>", self.__on_modified)
        self.__thisTextArea.bind("<KeyRelease>", self.__on_modified)

    def __create_status_bar(self):
        self.__status = tk.Label(self.__root, text="Words: 0 | Chars: 0 | Errors: 0",
                                 anchor=tk.W, relief=tk.SUNKEN)
        self.__status.grid(row=1, column=0, sticky="ew")

    def __on_modified(self, _event: Any = None) -> None:
        self.__thisTextArea.edit_modified(False)
        text = self.__thisTextArea.get('1.0', tk.END)
        words = len(re.findall(r"\b\w+\b", text))
        chars = len(text.strip())
        self.__status.config(text=f"Words: {words} | Chars: {chars} | Errors: {len(self.error_positions)}")

    def __create_menu_items(self):
        # File (original)
        self.__thisFileMenu.add_command(label="New", accelerator="Ctrl+N", command=self.__new_file)
        self.__thisFileMenu.add_command(label="Open", accelerator="Ctrl+O", command=self.__open_file)
        self.__thisFileMenu.add_command(label="Save", accelerator="Ctrl+S", command=self.__save_file)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quit_application)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)
        # Edit (original + Undo/Select All)
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)
        self.__thisEditMenu.add_separator()
        self.__thisEditMenu.add_command(label="Undo", command=lambda: self.__thisTextArea.event_generate("<<Undo>>"))
        self.__thisEditMenu.add_command(label="Select All", command=lambda: self.__thisTextArea.tag_add("sel", "1.0", tk.END))
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)
        # Tools - NEW mixed spell check menu
        self.__thisToolsMenu.add_command(label="Check Spelling (Edit-Distance)", accelerator="F7", command=self.__check_spelling)
        self.__thisToolsMenu.add_command(label="Check Single Word (ML Model)", command=self.__ml_check_word)
        self.__thisToolsMenu.add_command(label="Train ML Model (slow, ~30s)", command=self.__train_ml)
        self.__thisToolsMenu.add_command(label="Clear Highlights", command=self.__clear_highlights)
        self.__thisToolsMenu.add_command(label="Load Sample Text with Errors", command=self.__load_sample)
        self.__thisMenuBar.add_cascade(label="Tools / Spell Check", menu=self.__thisToolsMenu)
        # Help
        self.__thisHelpMenu.add_command(label="About Notepad", command=self.__show_about)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)
        self.__root.config(menu=self.__thisMenuBar)
        # Shortcuts
        self.__root.bind("<Control-n>", lambda e: self.__new_file())
        self.__root.bind("<Control-o>", lambda e: self.__open_file())
        self.__root.bind("<Control-s>", lambda e: self.__save_file())
        self.__root.bind("<F7>", lambda e: self.__check_spelling())

    # ---------- Original Notepad methods ----------
    def __quit_application(self):
        self.__root.destroy()
    def __show_about(self):
        messagebox.showinfo("Notepad", "Notepad + Spell Check Suite\nMixed from 3 projects:\nNotepad + ML Spell Checker + Edit-Distance Spell Checker")
    def __open_file(self):
        self.__file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete('1.0', tk.END)
            try:
                with open(self.__file, "r", encoding="utf-8") as f:
                    self.__thisTextArea.insert('1.0', f.read())
            except Exception as e:
                messagebox.showerror("Open Error", str(e))
            self.__clear_highlights()
    def __new_file(self):
        self.__root.title("Untitled - Notepad + Spell Check")
        self.__file = None
        self.__thisTextArea.delete('1.0', tk.END)
        self.__clear_highlights()
    def __save_file(self):
        if not self.__file:
            self.__file = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file:
            with open(self.__file, "w", encoding="utf-8") as f:
                f.write(self.__thisTextArea.get('1.0', tk.END))
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
    def __cut(self): self.__thisTextArea.event_generate("<<Cut>>")
    def __copy(self): self.__thisTextArea.event_generate("<<Copy>>")
    def __paste(self): self.__thisTextArea.event_generate("<<Paste>>")

    # ---------- NEW: Spell Check mixed in ----------
    def __clear_highlights(self):
        self.__thisTextArea.tag_remove("misspelled", "1.0", tk.END)
        self.error_positions = []
        self.__on_modified()

    def __check_spelling(self):
        """Highlights unknown words + popup with suggestions. Click suggestion to replace."""
        self.__clear_highlights()
        text = self.__thisTextArea.get('1.0', tk.END)
        self.__root.config(cursor="watch"); self.__root.update()
        errors = self.edit_checker.check_text(text)
        self.__root.config(cursor="")
        if not errors:
            messagebox.showinfo("Spell Check", "No spelling errors found! Great job.")
            return
        # Highlight each error (convert char offset -> Tk index)
        for word, char_pos, suggestions in errors:
            # char_pos counts chars from start; Tk index: 1.0 + chars
            start = self.__thisTextArea.index(f"1.0 + {char_pos} chars")
            end = self.__thisTextArea.index(f"{start} + {len(word)} chars")
            self.__thisTextArea.tag_add("misspelled", start, end)
            self.error_positions.append((start, end, word, suggestions))
        self.__on_modified()
        # Suggestion dialog for first error + list of all
        all_list = "\n".join([f"• {w} -> {', '.join(s) if s else 'no suggestion'}" for w, _, s in errors[:20]])
        first_word, _, first_sugg = errors[0]
        choice = None
        if first_sugg:
            choice = simpledialog.askstring(
                "Spell Check",
                f"Found {len(errors)} error(s).\n\nFirst: '{first_word}'\nSuggestions: {', '.join(first_sugg)}\n\nType a correction for '{first_word}' (or Cancel to see list):\n\nAll errors:\n{all_list}")
            if choice:
                self.__replace_word(first_word, choice)
        else:
            messagebox.showinfo("Spell Check", f"Found {len(errors)} error(s):\n\n{all_list}")

    def __replace_word(self, old: str, new: str) -> None:
        text = self.__thisTextArea.get('1.0', tk.END)
        # Replace first occurrence only (case-sensitive as typed)
        new_text = text.replace(old, new, 1)
        self.__thisTextArea.delete('1.0', tk.END)
        self.__thisTextArea.insert('1.0', new_text)
        self.__clear_highlights()

    def __ml_check_word(self):
        if not self.ml_checker.trained:
            ans = messagebox.askyesno("ML Not Trained",
                "ML model is not trained yet (takes ~30s).\nTrain now with 3000 sample words?")
            if not ans:
                return
            self.__train_ml()
            if not self.ml_checker.trained:
                return
        word = simpledialog.askstring("ML Spell Check", "Enter a word to check:")
        if not word:
            return
        pred = self.ml_checker.predict(word.strip().lower())
        edit_ok = self.edit_checker.is_correct(word.strip())
        msg = (f"Word: '{word}'\n"
               f"ML Model (TF-IDF + Naive Bayes): {'Likely CORRECT' if pred==1 else 'Likely INCORRECT'}\n"
               f"Dictionary (Edit-Distance): {'Found' if edit_ok else 'Not found'}\n"
               f"Model Accuracy (on test split): {self.ml_checker.accuracy:.2%}" if self.ml_checker.accuracy else "")
        messagebox.showinfo("ML Spell Check", msg)

    def __train_ml(self):
        self.__root.config(cursor="watch"); self.__root.update()
        ok = self.ml_checker.train(sample_size=3000)
        self.__root.config(cursor="")
        if ok:
            messagebox.showinfo("ML Trained", f"ML model trained!\nAccuracy: {self.ml_checker.accuracy:.2%}\nNow use Tools > Check Single Word (ML Model)")
        else:
            messagebox.showerror("ML Failed",
                "Need: pip install pandas numpy scikit-learn nltk\nSee requirements.txt")

    def __load_sample(self):
        self.__thisTextArea.delete('1.0', tk.END)
        self.__thisTextArea.insert('1.0', "Ths is a sampl text with som spelling errrs\nHelo wrld, this is Notepad with spell chek!")
        self.__clear_highlights()
        messagebox.showinfo("Sample Loaded", "Sample with errors loaded.\nPress F7 to Check Spelling!")

    def run(self):
        self.__root.mainloop()

if __name__ == "__main__":
    notepad = Notepad(width=700, height=500)
    notepad.run()
