
"""
Lyric Game + Finder + Downloader
Combines:
  1. lyricsgenius bulk downloader (your first snippet)
  2. lyrics.ovh finder GUI (your second snippet)
  + NEW: Playable Lyric Game (Finish the Lyrics / Guess the Song)

Run: python lyric_game_app.py
No Genius token needed for Finder + Game (uses lyrics.ovh).
Genius token only needed for Bulk Download tab.
"""
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import requests, random, re, threading

# ---------------- Helpers ----------------
def clean_lyrics(text: str | None) -> list[str]:
    if not text:
        return []
    # remove [Chorus] etc, Genius footers
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\d+Embed.*', '', text, flags=re.S)
    lines = [l.strip() for l in text.splitlines() if l.strip() and len(l.strip()) > 3]
    return lines

def fetch_lyrics_ovh(artist: str, title: str) -> str:
    url = f'https://api.lyrics.ovh/v1/{artist}/{title}'
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json().get('lyrics', '')

# Starter songs so game works instantly without typing
STARTER_SONGS = [
    ("Ed Sheeran", "Perfect"),
    ("Ed Sheeran", "Shape of You"),
    ("Taylor Swift", "Love Story"),
    ("Taylor Swift", "Blank Space"),
    ("Adele", "Someone Like You"),
    ("Adele", "Hello"),
    ("Coldplay", "Yellow"),
    ("Coldplay", "Viva La Vida"),
    ("Justin Bieber", "Love Yourself"),
    ("Justin Bieber", "Sorry"),
    ("Bruno Mars", "Just The Way You Are"),
    ("Bruno Mars", "Locked Out Of Heaven"),
    ("Arijit Singh", "Tum Hi Ho"),
    ("Arijit Singh", "Channa Mereya"),
    ("Shawn Mendes", "Stitches"),
    ("Dua Lipa", "Levitating"),
    ("The Weeknd", "Blinding Lights"),
    ("Imagine Dragons", "Believer"),
]

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Lyric Game 🎤 - Finder + Game + Downloader")
        self.root.geometry("850x680")
        self.root.configure(bg="#111")

        self.score = 0
        self.round = 0
        self.streak = 0
        self.current_song = None
        self.current_lines = []
        self.current_answer = ""
        self.current_mode = tk.StringVar(value="finish")  # finish | guess
        self.hint_level = 0

        # Header
        header = tk.Frame(root, bg="#111")
        header.pack(fill="x", pady=10)
        tk.Label(header, text="🎤  LYRIC GAME", font=("Arial", 22, "bold"), bg="#111", fg="white").pack()
        tk.Label(header, text="Find lyrics • Play Finish The Lyrics • Download bulk lyrics", bg="#111", fg="#aaa", font=("Arial", 10)).pack()

        # Score bar
        score_frame = tk.Frame(root, bg="#222")
        score_frame.pack(fill="x", padx=16)
        self.score_label = tk.Label(score_frame, text="Score: 0  •  Round: 0  •  Streak: 0", bg="#222", fg="white", font=("Arial", 11, "bold"))
        self.score_label.pack(pady=6)

        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=10)

        self.game_tab = tk.Frame(self.notebook, bg="white")
        self.finder_tab = tk.Frame(self.notebook, bg="white")
        self.bulk_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.game_tab, text="  🎮  Play Game  ")
        self.notebook.add(self.finder_tab, text="  🔍  Lyric Finder  ")
        self.notebook.add(self.bulk_tab, text="  📥  Bulk Download (Genius)  ")

        self.build_game_tab()
        self.build_finder_tab()
        self.build_bulk_tab()

    # ============ GAME TAB ============
    def build_game_tab(self):
        f = self.game_tab
        tk.Label(f, text="Choose Mode:", font=("Arial", 11, "bold"), bg="white").pack(pady=(12,2))
        mode_frame = tk.Frame(f, bg="white")
        mode_frame.pack()
        tk.Radiobutton(mode_frame, text="Finish The Lyrics", variable=self.current_mode, value="finish", bg="white", font=("Arial", 11)).pack(side="left", padx=10)
        tk.Radiobutton(mode_frame, text="Guess The Song", variable=self.current_mode, value="guess", bg="white", font=("Arial", 11)).pack(side="left", padx=10)

        tk.Label(f, text="Or play a custom song:", bg="white", font=("Arial", 10)).pack(pady=(10,0))
        custom = tk.Frame(f, bg="white")
        custom.pack()
        self.game_artist = tk.Entry(custom, width=22, font=("Arial", 11))
        self.game_artist.insert(0, "Ed Sheeran")
        self.game_artist.pack(side="left", padx=4)
        self.game_title = tk.Entry(custom, width=22, font=("Arial", 11))
        self.game_title.insert(0, "Perfect")
        self.game_title.pack(side="left", padx=4)

        btn_frame = tk.Frame(f, bg="white")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="▶  New Random Round", command=lambda: self.new_round(), bg="#1DB954", fg="white", font=("Arial", 11, "bold"), padx=14, pady=6).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Play Custom Song", command=lambda: self.new_round(custom=True), bg="#222", fg="white", font=("Arial", 11), padx=14, pady=6).pack(side="left", padx=5)
        tk.Button(btn_frame, text="💡 Hint", command=self.show_hint, bg="#FFC107", font=("Arial", 11, "bold"), padx=12).pack(side="left", padx=5)

        self.lyric_display = tk.Label(f, text="Press 'New Random Round' to start!\n\nExample:\n\"I found a love for me...\"", font=("Arial", 14, "italic"), bg="#f7f7f7", wraplength=650, justify="center", relief="solid", borderwidth=1, padx=20, pady=20)
        self.lyric_display.pack(fill="x", padx=20, pady=8)

        tk.Label(f, text="Your Answer:", bg="white", font=("Arial", 11, "bold")).pack()
        self.answer_entry = tk.Entry(f, width=55, font=("Arial", 13))
        self.answer_entry.pack(pady=4)
        self.answer_entry.bind("<Return>", lambda e: self.check_answer())

        tk.Button(f, text="Check Answer", command=self.check_answer, bg="#111", fg="white", font=("Arial", 12, "bold"), padx=20, pady=6).pack(pady=6)
        self.feedback = tk.Label(f, text="", bg="white", font=("Arial", 12, "bold"), wraplength=650)
        self.feedback.pack(pady=4)
        self.reveal_label = tk.Label(f, text="", bg="white", font=("Arial", 10), fg="#555", wraplength=650)
        self.reveal_label.pack()

    def new_round(self, custom: bool = False):
        if custom:
            artist = self.game_artist.get().strip()
            title = self.game_title.get().strip()
            if not artist or not title:
                messagebox.showwarning("Missing", "Enter artist + title for custom song")
                return
            song = (artist, title)
        else:
            song = random.choice(STARTER_SONGS)
        self.feedback.config(text="Loading lyrics...", fg="black")
        self.reveal_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        threading.Thread(target=self._load_round, args=(song,), daemon=True).start()

    def _load_round(self, song: tuple[str, str]):
        artist, title = song
        try:
            raw = fetch_lyrics_ovh(artist, title)
            lines = clean_lyrics(raw)
            if len(lines) < 4:
                raise ValueError("Not enough lyrics")
            self.root.after(0, lambda: self._setup_round(song, lines))
        except Exception as e:
            self.root.after(0, lambda: self.feedback.config(text=f"Couldn't load {artist} - {title}. Try another. ({e})", fg="red"))

    def _setup_round(self, song: tuple[str, str], lines: list[str]):
        self.current_song = song
        self.current_lines = lines
        self.round += 1
        self.hint_level = 0
        mode = self.current_mode.get()
        # pick a random chunk
        idx = random.randint(1, len(lines)-2)
        if mode == "finish":
            # Show 2 lines, ask to finish next line
            prompt = "\n".join(lines[idx-1:idx+1])
            self.current_answer = lines[idx+1]
            self.lyric_display.config(text=f"Finish this lyric:\n\n\"{prompt}\n... ?\"\n\n({song[0]} - ???)")
        else:
            # Guess mode: show 2 lines, ask song title
            prompt = "\n".join(lines[idx:idx+2])
            self.current_answer = song[1]  # title
            self.lyric_display.config(text=f"Guess the SONG from these lyrics:\n\n\"{prompt}\"\n\nArtist: {song[0]}")
        self.feedback.config(text=f"Round {self.round} • {song[0]} • Mode: {mode}", fg="#333")
        self.update_score_label()

    def show_hint(self):
        if not self.current_song:
            return
        self.hint_level += 1
        ans = self.current_answer
        if self.current_mode.get() == "finish":
            # reveal first letters
            words = ans.split()
            shown = " ".join([w[:self.hint_level] + "___" if len(w) > self.hint_level else w for w in words])
            self.reveal_label.config(text=f"Hint: {shown}")
        else:
            self.reveal_label.config(text=f"Hint: Title starts with '{ans[:self.hint_level]}' • {len(ans)} letters • Artist: {self.current_song[0]}")

    def check_answer(self):
        if not self.current_song:
            return
        user = self.answer_entry.get().strip().lower()
        correct = self.current_answer.strip().lower()
        # fuzzy: allow if user typed 70% of words or title contained
        def normalize(s: str) -> str:
            return re.sub(r'[^a-z0-9 ]', '', s)
        u, c = normalize(user), normalize(correct)
        # For guess mode, also accept if title words overlap strongly
        is_correct = False
        if u == c:
            is_correct = True
        elif self.current_mode.get() == "guess" and u and u in c:
            is_correct = True
        elif self.current_mode.get() == "finish":
            # check word overlap
            uw = set(u.split()); cw = set(c.split())
            if uw and len(uw & cw) / max(1, len(cw)) >= 0.6:
                is_correct = True

        if is_correct:
            points = 100 - (self.hint_level * 20)
            points = max(20, points)
            self.score += points
            self.streak += 1
            self.feedback.config(text=f"✅ CORRECT! +{points} points!  🎉", fg="green")
            self.reveal_label.config(text=f"Answer was: \"{self.current_answer}\" — {self.current_song[0]} - {self.current_song[1]}")
        else:
            self.streak = 0
            self.feedback.config(text=f"❌ Nope! Try again or press Hint / New Round", fg="red")
            self.reveal_label.config(text=f"Correct answer was: \"{self.current_answer}\" — {self.current_song[0]} - {self.current_song[1]}")
        self.update_score_label()

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}  •  Round: {self.round}  •  Streak: {self.streak} 🔥")

    # ============ FINDER TAB (your 2nd snippet, upgraded) ============
    def build_finder_tab(self):
        f = self.finder_tab
        tk.Label(f, text="Artist Name:", font=("Arial", 11, "bold"), bg="white").pack(pady=(15,0))
        self.f_artist = tk.Entry(f, width=50, font=("Arial", 12))
        self.f_artist.pack()
        tk.Label(f, text="Song Title:", font=("Arial", 11, "bold"), bg="white").pack(pady=(8,0))
        self.f_title = tk.Entry(f, width=50, font=("Arial", 12))
        self.f_title.pack()
        btns = tk.Frame(f, bg="white")
        btns.pack(pady=10)
        tk.Button(btns, text="Find Lyrics", command=self.find_lyrics, bg="#1DB954", fg="white", font=("Arial", 11, "bold"), padx=16).pack(side="left", padx=5)
        tk.Button(btns, text="Play This As A Game Round →", command=self.play_finder_song, bg="#222", fg="white", font=("Arial", 11), padx=12).pack(side="left", padx=5)
        tk.Button(btns, text="Copy", command=self.copy_lyrics, font=("Arial", 11)).pack(side="left", padx=5)
        tk.Button(btns, text="Save .txt", command=self.save_finder_lyrics, font=("Arial", 11)).pack(side="left", padx=5)

        self.finder_text = tk.Text(f, height=20, width=80, font=("Arial", 11), wrap="word")
        self.finder_text.pack(padx=15, pady=5, fill="both", expand=True)

    def find_lyrics(self):
        artist = self.f_artist.get().strip()
        title = self.f_title.get().strip()
        if not artist or not title:
            messagebox.showerror("Error", "Please enter both artist and title")
            return
        self.finder_text.delete(1.0, tk.END)
        self.finder_text.insert(tk.END, "Loading...")
        threading.Thread(target=self._do_find, args=(artist, title), daemon=True).start()

    def _do_find(self, artist: str, title: str) -> None:
        try:
            lyrics = fetch_lyrics_ovh(artist, title)
            if not lyrics:
                raise ValueError("Not found")
            self.root.after(0, lambda: self._show_lyrics(artist, title, lyrics))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Lyrics not found.\nTry exact spelling.\n({e})"))
            self.root.after(0, lambda: self.finder_text.delete(1.0, tk.END))

    def _show_lyrics(self, artist: str, title: str, lyrics: str) -> None:
        self.finder_text.delete(1.0, tk.END)
        self.finder_text.insert(tk.END, f"{title} - {artist}\n\n{lyrics}")

    def play_finder_song(self):
        a = self.f_artist.get().strip(); t = self.f_title.get().strip()
        if not a or not t:
            messagebox.showwarning("Missing", "Enter artist + title first")
            return
        self.game_artist.delete(0, tk.END); self.game_artist.insert(0, a)
        self.game_title.delete(0, tk.END); self.game_title.insert(0, t)
        self.notebook.select(self.game_tab)
        self.new_round(custom=True)

    def copy_lyrics(self):
        txt = self.finder_text.get(1.0, tk.END).strip()
        self.root.clipboard_clear(); self.root.clipboard_append(txt)
        messagebox.showinfo("Copied", "Lyrics copied!")

    def save_finder_lyrics(self):
        txt = self.finder_text.get(1.0, tk.END).strip()
        if not txt:
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if path:
            open(path, 'w', encoding='utf-8').write(txt)
            messagebox.showinfo("Saved", f"Saved to {path}")

    # ============ BULK TAB (your 1st snippet, with GUI) ============
    def build_bulk_tab(self):
        f = self.bulk_tab
        tk.Label(f, text="Bulk Download with Genius (needs token)", font=("Arial", 12, "bold"), bg="white").pack(pady=(15,5))
        tk.Label(f, text="Get token free at genius.com/api-clients", bg="white", fg="#555", font=("Arial", 10)).pack()
        tk.Label(f, text="Genius Access Token:", bg="white", font=("Arial", 11, "bold")).pack(pady=(12,0))
        self.token_entry = tk.Entry(f, width=60, font=("Arial", 11), show="*")
        self.token_entry.pack()
        tk.Label(f, text="Artists (separated by commas): e.g. Taylor Swift, Ed Sheeran, Arijit Singh", bg="white", font=("Arial", 11, "bold")).pack(pady=(12,0))
        self.bulk_artists = tk.Entry(f, width=60, font=("Arial", 11))
        self.bulk_artists.insert(0, "Taylor Swift, Ed Sheeran")
        self.bulk_artists.pack()
        tk.Label(f, text="Max songs per artist:", bg="white", font=("Arial", 11, "bold")).pack(pady=(8,0))
        self.bulk_max_value = tk.StringVar(value="3")
        self.bulk_max = tk.Spinbox(f, from_=1, to=20, width=8, font=("Arial", 11), textvariable=self.bulk_max_value)
        self.bulk_max.pack()
        tk.Button(f, text="📥  Download & Save as .txt", command=self.bulk_download, bg="#111", fg="white", font=("Arial", 12, "bold"), padx=18, pady=7).pack(pady=14)
        self.bulk_log = tk.Text(f, height=12, width=80, font=("Arial", 10))
        self.bulk_log.pack(padx=15, pady=5, fill="both", expand=True)
        self.bulk_log.insert(tk.END, "This is your original lyricsgenius code, but with a GUI.\nIt will save like:\n# Taylor Swift\n<lyrics>\n\n# Ed Sheeran\n<lyrics>\n")

    def bulk_download(self):
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showerror("Need Token", "Paste your Genius Client Access Token.\nGet it at genius.com/api-clients (free)")
            return
        artists = [a.strip() for a in self.bulk_artists.get().split(",") if a.strip()]
        if not artists:
            messagebox.showerror("Need Artists", "Enter at least one artist")
            return
        try:
            max_songs = int(self.bulk_max.get())
        except:
            max_songs = 3
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")], initialfile="Lyrics.txt")
        if not path:
            return
        self.bulk_log.delete(1.0, tk.END)
        self.bulk_log.insert(tk.END, "Downloading...\n")
        threading.Thread(target=self._do_bulk, args=(token, artists, max_songs, path), daemon=True).start()

    def _do_bulk(self, token: str, artists: list[str], max_songs: int, path: str) -> None:
        try:
            import lyricsgenius as lg  # type: ignore[import-untyped]
        except ImportError:
            self.root.after(0, lambda: messagebox.showerror("Missing", "Run: pip install lyricsgenius"))
            return
        try:
            genius = lg.Genius(token)
            genius.skip_non_songs = True
            genius.excluded_terms = ["(Remix)", "(Live)"]
            genius.remove_section_headers = True
            with open(path, 'w', encoding='utf-8') as file:
                for artist in artists:
                    self.root.after(0, lambda a=artist: self.bulk_log.insert(tk.END, f"Fetching {a}...\n"))
                    try:
                        artist_result = genius.search_artist(artist, max_songs=max_songs, sort='popularity')
                        songs = artist_result.songs if artist_result is not None else []
                        file.write(f"# {artist}\n")
                        for song in songs:
                            file.write((song.lyrics or "") + "\n\n")
                        file.write("\n")
                        self.root.after(0, lambda a=artist, n=len(songs): self.bulk_log.insert(tk.END, f"✓ {a}: {n} songs saved\n"))
                    except Exception as e:
                        self.root.after(0, lambda a=artist, e=e: self.bulk_log.insert(tk.END, f"✗ Error {a}: {e}\n"))
            self.root.after(0, lambda: messagebox.showinfo("Done", f"Lyrics saved to {path}"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
