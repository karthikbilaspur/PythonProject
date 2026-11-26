import tkinter as tk
import nltk  # type: ignore

try:
    import requests
except ImportError:
    requests = None

LETTER_SCORES = {
    'a':1,'b':3,'c':3,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':8,'k':5,
    'l':1,'m':3,'n':1,'o':1,'p':3,'q':10,'r':1,'s':1,'t':1,'u':1,
    'v':4,'w':4,'x':8,'y':4,'z':10,
}
# Offline fallback so game works without NLTK / internet.
FALLBACK_WORDS = set("""cat dog run jump play game word score book tree house water sun moon star
love happy quick brown fox lazy apple banana orange python code book read write
friend family home school music dance sing light dark green blue red happy""".split())
ROUNDS = 5

def load_word_list():
    try:
        nltk.data.find("corpora/words")  # type: ignore[reportUnknownMemberType]
    except LookupError:
        try:
            nltk.download("words", quiet=True)  # type: ignore[reportUnknownMemberType]
        except Exception:
            return FALLBACK_WORDS
    try:
        from nltk.corpus import words as nltk_words  # type: ignore[reportMissingTypeStubs]
        word_list: list[str] = nltk_words.words()  # type: ignore[reportUnknownMemberType]
        return {w.lower() for w in word_list if w.isalpha()}
    except Exception:
        return FALLBACK_WORDS

WORD_LIST = load_word_list()

def fetch_definition(word: str) -> str:
    if requests is None:
        return "Definitions need `requests`: pip install requests"
    try:
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=8)
        if r.status_code != 200:
            return "No definition found."
        parts: list[str] = []
        for entry in r.json():
            for meaning in entry.get("meanings", []):
                for d in meaning.get("definitions", [])[:2]:
                    parts.append(f"({meaning.get('partOfSpeech','')}) {d.get('definition','')}")
        return "\n".join(parts) or "No definition found."
    except Exception as e:
        return f"Could not fetch definition (offline?): {e}"

class ScrabbleGame:
    def __init__(self):
        self.players = {}          # name -> score
        self.player_order = []
        self.current_player = 0
        self.rounds_played = {}    # name -> rounds completed
        self.used_words: set[str] = set()
        self.game_over = False

        self.root = tk.Tk()
        self.root.title("Scrabble Game")
        self.root.geometry("460x560")
        self._build_setup()

    # ---------- setup screens ----------
    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _status(self, msg: str, color: str = "black") -> None:
        self.status_label.config(text=msg, fg=color)

    def _build_setup(self):
        self._clear()
        tk.Label(self.root, text="Scrabble Game", font=("Helvetica", 16, "bold")).pack(pady=12)
        tk.Label(self.root, text=f"Enter number of players (2-6). {ROUNDS} rounds each.").pack()
        self.player_count_entry = tk.Entry(self.root); self.player_count_entry.pack(pady=6)
        tk.Button(self.root, text="Submit", command=self.get_player_count).pack()
        self.status_label = tk.Label(self.root, text="", wraplength=400); self.status_label.pack(pady=8)

    def get_player_count(self):
        try:
            count = int(self.player_count_entry.get())
            if not 2 <= count <= 6:
                raise ValueError
        except ValueError:
            self._status("Enter a number from 2 to 6.", "red"); return
        self._player_count = count
        self._build_name_entry(0, [])

    def _build_name_entry(self, idx: int, names: list[str]) -> None:
        self._clear()
        tk.Label(self.root, text=f"Player {idx+1} name:").pack(pady=10)
        e = tk.Entry(self.root); e.pack(); e.focus()
        self.status_label = tk.Label(self.root, text="", wraplength=400); self.status_label.pack(pady=8)
        def submit():
            name = e.get().strip()
            if not name:
                self._status("Name cannot be empty.", "red"); return
            if name.lower() in [n.lower() for n in names]:
                self._status("Names must be unique.", "red"); return
            names.append(name)
            if len(names) < self._player_count:
                self._build_name_entry(len(names), names)
            else:
                self.start_game(names)
        tk.Button(self.root, text="Submit", command=submit).pack()
        e.bind("<Return>", lambda _: submit())

    # ---------- game ----------
    def start_game(self, names: list[str]) -> None:
        self.player_order = names
        self.players = {n: 0 for n in names}
        self.rounds_played = {n: 0 for n in names}
        self._clear()
        self.player_name_label = tk.Label(self.root, text="", font=("Helvetica", 13, "bold")); self.player_name_label.pack(pady=6)
        tk.Label(self.root, text="Enter a word:").pack()
        self.word_entry = tk.Entry(self.root, width=30); self.word_entry.pack(pady=4); self.word_entry.focus()
        tk.Button(self.root, text="Submit word", command=self.get_word).pack(pady=3)
        tk.Button(self.root, text="View definition", command=self.view_definition).pack(pady=3)
        tk.Label(self.root, text="Scores:").pack(pady=(10, 0))
        self.score_text = tk.Text(self.root, height=8, width=38); self.score_text.pack()
        self.status_label = tk.Label(self.root, text="", wraplength=400); self.status_label.pack(pady=8)
        self.word_entry.bind("<Return>", lambda _: self.get_word())
        self._refresh_turn()

    def _refresh_turn(self):
        name = self.player_order[self.current_player]
        rnd = self.rounds_played[name] + 1
        self.player_name_label.config(text=f"{name}'s turn  (Round {rnd}/{ROUNDS})")
        self.update_scores()

    def valid(self, word: str) -> bool:
        return word.lower() in WORD_LIST

    def compute_score(self, word: str) -> int:
        word = word.lower()
        if not word.isalpha():
            raise ValueError("Word should only contain letters (a-z).")
        if word in self.used_words:
            raise ValueError(f"'{word}' was already played.")
        if not self.valid(word):
            raise ValueError(f"'{word}' is not in the word list.")
        return sum(LETTER_SCORES[c] for c in word)

    def get_word(self):
        if self.game_over:
            return
        word = self.word_entry.get().strip()
        if not word:
            self._status("Enter a word first.", "red"); return
        try:
            score = self.compute_score(word)
        except ValueError as e:
            self._status(str(e), "red"); return
        name = self.player_order[self.current_player]
        self.players[name] += score
        self.used_words.add(word.lower())
        self.rounds_played[name] += 1
        self._status(f"{name} scored {score} with '{word}'!", "green")
        self.word_entry.delete(0, tk.END)
        # Game over when everyone finished ROUNDS rounds
        if all(v >= ROUNDS for v in self.rounds_played.values()):
            self._end_game(); return
        self.current_player = (self.current_player + 1) % len(self.player_order)
        self._refresh_turn()

    def view_definition(self):
        word = self.word_entry.get().strip()
        if not word:
            self._status("Enter a word to look up.", "red"); return
        win = tk.Toplevel(self.root); win.title(f"Definition of {word}")
        t = tk.Text(win, height=10, width=50, wrap="word"); t.pack(padx=10, pady=10)
        t.insert(tk.END, fetch_definition(word.lower())); t.config(state="disabled")

    def update_scores(self):
        self.score_text.delete("1.0", tk.END)
        for p, s in sorted(self.players.items(), key=lambda x: -x[1]):
            self.score_text.insert(tk.END, f"{p}: {s}  ({self.rounds_played[p]}/{ROUNDS} rounds)\n")

    def _end_game(self):
        self.game_over = True
        self.update_scores()
        best = max(self.players.values())
        winners = [p for p, s in self.players.items() if s == best]
        title = f"Game Over! Winner: {winners[0]} ({best} pts)" if len(winners) == 1 else f"Game Over! Tie: {', '.join(winners)} ({best} pts)"
        self.player_name_label.config(text=title)
        self._status("Thanks for playing!", "green")
        tk.Button(self.root, text="Play Again", command=self._build_setup).pack(pady=8)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ScrabbleGame().run()
