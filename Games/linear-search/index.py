
"""
================================================================================
 LINEAR SEARCH: THE GAME - Big Single-File Edition
================================================================================
 A playable game built on top of the Linear Search Visualizer.

 HOW TO PLAY:
  1. Press START GAME / NEW ROUND - a hidden array is generated.
  2. You see the bars but NOT their values (mystery mode) OR you see values
     depending on difficulty.
  3. A KEY is shown. Guess WHERE it is (index) before the search runs.
  4. Watch the search animate left -> right. If your guess was right,
     you win big points. Closer guesses still earn points.
  5. Bonus modes: Time Attack, Streak, and Hardcore (no values at all).

 FEATURES:
  - 3 Difficulties: Easy / Medium / Hard / Hardcore
  - 3 Game Modes: Classic, Time Attack (60s), Survival (3 lives)
  - Scoring: accuracy + speed bonus + streak multiplier
  - Levels: array gets bigger + values get wider every level
  - Hint system (costs points)
  - Sound-free, but with flash animations, confetti, leaderboard
  - Stats panel, history log, pause / resume
  - Custom array mode - paste your own numbers
  - Practice mode (original visualizer, no scoring)

 Run:  python linear_search_game.py
 Requires: only stdlib (tkinter, random, time, json, os)
================================================================================
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import json
import os
import math
from typing import cast, TypedDict

# ------------------------------------------------------------------------------
# CONFIG / THEME
# ------------------------------------------------------------------------------
BG_MAIN = "#0f172a"
BG_PANEL = "#1e293b"
BG_CARD = "#334155"
ACCENT = "#22c55e"
ACCENT2 = "#38bdf8"
ACCENT3 = "#f59e0b"
DANGER = "#ef4444"
TEXT = "#f8fafc"
TEXT_DIM = "#94a3b8"
BAR_DEFAULT = "#64748b"
BAR_CHECKING = "#ffffff"
BAR_FOUND = "#22c55e"
BAR_WRONG_GUESS = "#ef4444"
BAR_GUESS = "#f59e0b"
BAR_HINT = "#a78bfa"

SAVE_FILE = "linear_search_highscores.json"


class DifficultyConfig(TypedDict):
    size: int
    min: int
    max: int
    show_values: bool
    time_bonus: int


DIFFICULTIES: dict[str, DifficultyConfig] = {
    "Easy":      {"size": 8,  "min": 1,  "max": 20,  "show_values": True,  "time_bonus": 100},
    "Medium":    {"size": 12, "min": 1,  "max": 50,  "show_values": True,  "time_bonus": 150},
    "Hard":      {"size": 16, "min": 1,  "max": 99,  "show_values": False, "time_bonus": 250},
    "Hardcore":  {"size": 20, "min": 1,  "max": 200, "show_values": False, "time_bonus": 400},
}

MODES = ["Classic", "Time Attack (60s)", "Survival (3 Lives)", "Practice (No Score)"]

# ------------------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------------------
def load_scores() -> list[dict[str, object]]:
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                scores: object = json.load(f)
                if not isinstance(scores, list):
                    return []

                valid_scores: list[dict[str, object]] = []
                for score in cast(list[object], scores):
                    if isinstance(score, dict):
                        valid_scores.append(cast(dict[str, object], score))
                return valid_scores
        except (OSError, json.JSONDecodeError):
            return []
    return []

def save_scores(scores: list[dict[str, object]]) -> None:
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(scores, f, indent=2)
    except:
        pass

def fmt_time(s: float) -> str:
    return f"{int(s//60):02d}:{int(s%60):02d}"

# ------------------------------------------------------------------------------
# MAIN GAME CLASS
# ------------------------------------------------------------------------------
class LinearSearchGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Linear Search: THE GAME  |  Guess the Index!")
        self.root.geometry("1080x760")
        self.root.config(bg=BG_MAIN)
        self.root.resizable(True, True)

        # ---- Game State ----
        self.array = []
        self.key = None
        self.actual_index = -1
        self.player_guess = None
        self.score = 0
        self.round = 0
        self.level = 1
        self.streak = 0
        self.best_streak = 0
        self.lives = 3
        self.hints_used = 0
        self.total_guesses = 0
        self.correct_guesses = 0
        self.game_active = False
        self.searching = False
        self.paused = False
        self.time_left = 60
        self.time_attack_end = 0
        self.round_start_time = 0
        self.history = []
        self.highscores = load_scores()
        self.difficulty = tk.StringVar(value="Medium")
        self.mode = tk.StringVar(value="Classic")
        self.show_values_var = tk.BooleanVar(value=True)

        self.build_ui()
        self.update_stats()
        self.new_round(auto=False)
        self.tick_timer()

    # ==========================================================================
    # UI BUILD
    # ==========================================================================
    def build_ui(self):
        # ----- TOP HEADER -----
        header = tk.Frame(self.root, bg=BG_MAIN)
        header.pack(fill="x", padx=16, pady=(14, 6))
        tk.Label(header, text="🔍  LINEAR SEARCH", font=("Segoe UI", 26, "bold"), bg=BG_MAIN, fg=TEXT).pack(side="left")
        tk.Label(header, text="THE GAME", font=("Segoe UI", 26, "bold"), bg=BG_MAIN, fg=ACCENT).pack(side="left", padx=(8, 0))
        tk.Label(header, text="Guess where the key hides before the search finds it!", font=("Segoe UI", 10), bg=BG_MAIN, fg=TEXT_DIM).pack(side="left", padx=(16, 0))

        # ----- STATS BAR -----
        stats = tk.Frame(self.root, bg=BG_PANEL)
        stats.pack(fill="x", padx=16, pady=6)
        self.stat_labels: dict[str, tk.Label] = {}
        for i, (key, label) in enumerate([
            ("score", "⭐ SCORE"), ("round", "🎯 ROUND"), ("level", "📈 LEVEL"),
            ("streak", "🔥 STREAK"), ("lives", "❤️ LIVES"), ("timer", "⏱️ TIME"),
            ("accuracy", "🎯 ACCURACY"),
        ]):
            f = tk.Frame(stats, bg=BG_PANEL)
            f.grid(row=0, column=i, padx=12, pady=8, sticky="w")
            tk.Label(f, text=label, font=("Segoe UI", 8, "bold"), bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w")
            lbl = tk.Label(f, text="0", font=("Segoe UI", 16, "bold"), bg=BG_PANEL, fg=TEXT)
            lbl.pack(anchor="w")
            self.stat_labels[key] = lbl

        # ----- CANVAS -----
        canvas_frame = tk.Frame(self.root, bg=BG_MAIN)
        canvas_frame.pack(fill="x", padx=16, pady=6)
        self.canvas = tk.Canvas(canvas_frame, width=1040, height=360, bg="#0b1220", highlightthickness=2, highlightbackground=BG_CARD)
        self.canvas.pack(fill="x")
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Key display + message
        mid = tk.Frame(self.root, bg=BG_MAIN)
        mid.pack(fill="x", padx=16, pady=4)
        self.key_label = tk.Label(mid, text="Press START GAME to begin", font=("Segoe UI", 18, "bold"), bg=BG_MAIN, fg=ACCENT2)
        self.key_label.pack(side="left")
        self.msg_label = tk.Label(mid, text="Click a bar to guess its index!", font=("Segoe UI", 11), bg=BG_MAIN, fg=TEXT_DIM)
        self.msg_label.pack(side="left", padx=(18, 0))

        # ----- CONTROLS -----
        ctrl = tk.Frame(self.root, bg=BG_PANEL)
        ctrl.pack(fill="x", padx=16, pady=8)

        # Row 1: Difficulty + Mode + toggles
        tk.Label(ctrl, text="Difficulty:", bg=BG_PANEL, fg=TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=6, pady=8, sticky="e")
        tk.OptionMenu(ctrl, self.difficulty, *DIFFICULTIES.keys()).grid(row=0, column=1, padx=4, sticky="w")
        tk.Label(ctrl, text="Mode:", bg=BG_PANEL, fg=TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=6, sticky="e")
        tk.OptionMenu(ctrl, self.mode, *MODES).grid(row=0, column=3, padx=4, sticky="w")
        tk.Checkbutton(ctrl, text="Show values", variable=self.show_values_var, bg=BG_PANEL, fg=TEXT, selectcolor=BG_CARD, command=self.redraw).grid(row=0, column=4, padx=10)
        tk.Button(ctrl, text="📊 Leaderboard", bg=ACCENT2, fg="white", font=("Segoe UI", 10, "bold"), command=self.show_leaderboard).grid(row=0, column=5, padx=6)
        tk.Button(ctrl, text="❓ How to Play", bg=BG_CARD, fg=TEXT, font=("Segoe UI", 10, "bold"), command=self.show_help).grid(row=0, column=6, padx=6)

        # Row 2: Main actions
        tk.Button(ctrl, text="▶ START GAME", bg=ACCENT, fg="white", font=("Segoe UI", 12, "bold"), padx=18, pady=6, command=self.start_game).grid(row=1, column=0, columnspan=2, padx=6, pady=6)
        tk.Button(ctrl, text="🎲 New Round", bg=ACCENT3, fg="black", font=("Segoe UI", 11, "bold"), padx=14, command=lambda: self.new_round()).grid(row=1, column=2, padx=6)
        tk.Button(ctrl, text="🔍 REVEAL SEARCH", bg="#8b5cf6", fg="white", font=("Segoe UI", 11, "bold"), padx=14, command=self.search).grid(row=1, column=3, padx=6)
        tk.Button(ctrl, text="💡 Hint (-25 pts)", bg=BG_CARD, fg=TEXT, font=("Segoe UI", 11, "bold"), command=self.use_hint).grid(row=1, column=4, padx=6)
        tk.Button(ctrl, text="⏸ Pause", bg=BG_CARD, fg=TEXT, font=("Segoe UI", 11, "bold"), command=self.toggle_pause).grid(row=1, column=5, padx=6)
        tk.Button(ctrl, text="🔄 Reset", bg=DANGER, fg="white", font=("Segoe UI", 11, "bold"), command=self.reset_game).grid(row=1, column=6, padx=6)

        # Row 3: Guess entry + custom array
        guess_frame = tk.Frame(self.root, bg=BG_MAIN)
        guess_frame.pack(fill="x", padx=16, pady=4)
        tk.Label(guess_frame, text="Your Guess (index 0 - n):", bg=BG_MAIN, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(side="left")
        self.guess_entry = tk.Entry(guess_frame, width=8, font=("Segoe UI", 12))
        self.guess_entry.pack(side="left", padx=8)
        tk.Button(guess_frame, text="Lock Guess ✓", bg=ACCENT2, fg="white", font=("Segoe UI", 11, "bold"), command=self.lock_guess_from_entry).pack(side="left", padx=4)
        tk.Label(guess_frame, text="  |  Custom array (comma separated):", bg=BG_MAIN, fg=TEXT_DIM, font=("Segoe UI", 10)).pack(side="left", padx=(12, 4))
        self.custom_entry = tk.Entry(guess_frame, width=28, font=("Segoe UI", 11))
        self.custom_entry.pack(side="left", padx=4)
        tk.Button(guess_frame, text="Use Custom", bg=BG_CARD, fg=TEXT, command=self.use_custom_array).pack(side="left", padx=4)

        # ----- HISTORY / LOG -----
        log_frame = tk.Frame(self.root, bg=BG_MAIN)
        log_frame.pack(fill="both", expand=True, padx=16, pady=(4, 12))
        tk.Label(log_frame, text="📜 Round History  (click a bar OR type an index, then press REVEAL SEARCH)", bg=BG_MAIN, fg=TEXT_DIM, font=("Segoe UI", 9)).pack(anchor="w")
        self.log_text = tk.Text(log_frame, height=6, bg=BG_PANEL, fg=TEXT, font=("Consolas", 10), wrap="word")
        self.log_text.pack(fill="both", expand=True)
        self.log("Welcome! Choose difficulty + mode, press START GAME, then guess the index of the key.")

    # ==========================================================================
    # GAME LOGIC
    # ==========================================================================
    def log(self, msg: str):
        self.log_text.insert("end", f"• {msg}\n")
        self.log_text.see("end")

    def update_stats(self):
        acc = f"{(self.correct_guesses/max(1,self.total_guesses)*100):.0f}%" if self.total_guesses else "—"
        self.stat_labels["score"].config(text=str(self.score))
        self.stat_labels["round"].config(text=str(self.round))
        self.stat_labels["level"].config(text=str(self.level))
        self.stat_labels["streak"].config(text=f"{self.streak} (best {self.best_streak})")
        self.stat_labels["lives"].config(text="♥" * max(0, self.lives) if "Survival" in self.mode.get() else "∞")
        self.stat_labels["timer"].config(text=fmt_time(self.time_left) if "Time Attack" in self.mode.get() else "—")
        self.stat_labels["accuracy"].config(text=acc)

    def start_game(self):
        self.score = 0; self.round = 0; self.level = 1; self.streak = 0
        self.best_streak = 0; self.lives = 3; self.hints_used = 0
        self.total_guesses = 0; self.correct_guesses = 0
        self.time_left = 60; self.game_active = True; self.searching = False
        self.log_text.delete("1.0", "end")
        self.log(f"=== NEW GAME: {self.difficulty.get()} / {self.mode.get()} ===")
        self.new_round()
        self.update_stats()

    def reset_game(self):
        self.game_active = False
        self.start_game()

    def generate_array(self):
        d = DIFFICULTIES[self.difficulty.get()]
        # Level scaling: +2 size per level, capped at 30
        size = min(30, d["size"] + (self.level - 1) * 2)
        arr = [random.randint(d["min"], d["max"]) for _ in range(size)]
        # 75% chance key is IN the array, 25% not in array (trick round!)
        if random.random() < 0.75:
            self.key = random.choice(arr)
            self.actual_index = arr.index(self.key)
        else:
            # pick a key NOT in array
            while True:
                k = random.randint(d["min"], d["max"])
                if k not in arr:
                    self.key = k; self.actual_index = -1; break
        return arr

    def new_round(self, auto: bool = True):
        if not self.game_active and auto:
            # practice / preview round
            pass
        self.round += 1
        # Level up every 3 rounds
        self.level = 1 + (self.round - 1) // 3
        self.array = self.generate_array()
        self.player_guess = None
        self.searching = False
        self.round_start_time = time.time()
        self.guess_entry.delete(0, "end")
        self.key_label.config(text=f"🔑 KEY TO FIND:  {self.key}   |   Array size: {len(self.array)}   |   Guess its index!")
        self.msg_label.config(text="Click a bar to guess — or type an index and Lock Guess.", fg=TEXT_DIM)
        self.draw_rectangles(self.array, [BAR_DEFAULT]*len(self.array))
        self.update_stats()
        self.log(f"Round {self.round} (Lv {self.level}): Key={self.key}, Size={len(self.array)} — make your guess!")

    def use_custom_array(self):
        raw = self.custom_entry.get().strip()
        try:
            arr = [int(x.strip()) for x in raw.split(",") if x.strip() != ""]
            if len(arr) < 3:
                raise ValueError
            self.array = arr
            self.key = random.choice(arr)
            self.actual_index = arr.index(self.key)
            self.player_guess = None
            self.key_label.config(text=f"🔑 KEY TO FIND:  {self.key}   |   Custom array size: {len(arr)}")
            self.draw_rectangles(self.array, [BAR_DEFAULT]*len(self.array))
            self.log(f"Custom array loaded: {arr}, Key={self.key}")
        except:
            messagebox.showerror("Error", "Enter comma-separated numbers, e.g. 5, 12, 7, 20, 3")

    def on_canvas_click(self, event: tk.Event):
        if not self.array or self.searching:
            return
        bar_w = 1040 / len(self.array)
        idx = int(event.x // bar_w)
        if 0 <= idx < len(self.array):
            self.player_guess = idx
            self.highlight_guess()
            self.msg_label.config(text=f"Your guess: index {idx}  (value {self.array[idx] if self.show_values_var.get() else '???'}) — press REVEAL SEARCH!", fg=ACCENT3)
            self.guess_entry.delete(0, "end"); self.guess_entry.insert(0, str(idx))

    def lock_guess_from_entry(self):
        try:
            idx = int(self.guess_entry.get())
            if not (0 <= idx < len(self.array)):
                raise ValueError
            self.player_guess = idx
            self.highlight_guess()
            self.msg_label.config(text=f"Guess locked: index {idx} — press REVEAL SEARCH!", fg=ACCENT3)
        except:
            messagebox.showerror("Error", f"Enter an index between 0 and {len(self.array)-1}")

    def highlight_guess(self):
        colors = [BAR_DEFAULT]*len(self.array)
        if self.player_guess is not None:
            colors[self.player_guess] = BAR_GUESS
        self.draw_rectangles(self.array, colors)

    def redraw(self) -> None:
        """Redraw the array after display or state changes."""
        if self.player_guess is not None:
            self.highlight_guess()
        else:
            self.draw_rectangles(self.array, [BAR_DEFAULT] * len(self.array))

    def use_hint(self):
        if not self.array or self.searching:
            return
        if self.score < 25:
            messagebox.showinfo("Hint", "You need at least 25 points for a hint!")
            return
        self.score -= 25; self.hints_used += 1
        # Hint: narrow to a window around actual index, or say "not in array"
        if self.actual_index == -1:
            self.msg_label.config(text="💡 HINT: The key is NOT in this array!", fg=BAR_HINT)
        else:
            lo = max(0, self.actual_index - 2); hi = min(len(self.array)-1, self.actual_index + 2)
            colors = [BAR_DEFAULT]*len(self.array)
            for i in range(lo, hi+1):
                colors[i] = BAR_HINT
            self.draw_rectangles(self.array, colors)
            self.msg_label.config(text=f"💡 HINT: Key is somewhere between index {lo} and {hi} (purple zone). -25 pts", fg=BAR_HINT)
        self.update_stats()

    def toggle_pause(self):
        self.paused = not self.paused
        self.msg_label.config(text="⏸ Paused — press Pause again to resume." if self.paused else "Resumed!", fg=TEXT_DIM)

    # ----- THE SEARCH ANIMATION (core from original, now gamified) -----
    def search(self):
        if not self.array:
            messagebox.showwarning("Wait", "Generate / start a game first!")
            return
        if self.searching:
            return
        if self.player_guess is None:
            if not messagebox.askyesno("No Guess?", "You haven't guessed yet! Reveal anyway for 0 points?"):
                return
        self.searching = True
        self.total_guesses += 1
        colors = [BAR_DEFAULT]*len(self.array)
        found_idx = -1
        for i in range(len(self.array)):
            while self.paused:
                self.root.update(); time.sleep(0.1)
            colors[i] = BAR_CHECKING
            # keep guess highlighted
            if self.player_guess is not None and self.player_guess != i:
                colors[self.player_guess] = BAR_GUESS
            self.draw_rectangles(self.array, colors)
            self.root.update_idletasks(); self.root.update()
            time.sleep(0.18)
            if self.array[i] == self.key:
                found_idx = i
                colors[i] = BAR_FOUND
                self.draw_rectangles(self.array, colors)
                break
            else:
                colors[i] = BAR_DEFAULT
                if self.player_guess is not None and self.player_guess != i:
                    colors[self.player_guess] = BAR_GUESS
                self.draw_rectangles(self.array, colors)
                self.root.update_idletasks(); self.root.update()
                time.sleep(0.08)
        self.finish_round(found_idx)
        self.searching = False

    def finish_round(self, found_idx: int):
        elapsed = time.time() - self.round_start_time
        guess = self.player_guess
        is_exact = (guess is not None and guess == found_idx and found_idx != -1)
        # Case: key not in array, and player guessed "not in array" by leaving guess empty is handled above.
        # If key not found and player guessed nothing, that's a win only if they explicitly said so — keep simple:
        if found_idx == -1:
            # Key not in array — trick round
            if guess is None:
                pts = 200; self.correct_guesses += 1; self.streak += 1
                self.msg_label.config(text=f"🎉 Trick round! Key {self.key} was NOT in the array. +{pts} pts!", fg=ACCENT)
                self.score += pts
                self.log(f"Round {self.round}: TRICK - key not present. +{pts} (no guess)")
                messagebox.showinfo("Result", f"Trick round! Key {self.key} was NOT in the array.\nYou correctly didn't guess. +{pts} pts!")
            else:
                self.streak = 0; self.lives -= 1 if "Survival" in self.mode.get() else 0
                self.msg_label.config(text=f"❌ Key {self.key} was NOT in the array. Your guess {guess} was wrong.", fg=DANGER)
                self.log(f"Round {self.round}: Key NOT present, guessed {guess}. Wrong.")
                messagebox.showinfo("Result", f"Key {self.key} was NOT in the array!\nYour guess was wrong.")
                if "Survival" in self.mode.get() and self.lives <= 0:
                    self.game_over(); return
        elif is_exact:
            # Score: base 100 + speed bonus + streak multiplier + difficulty bonus
            d = DIFFICULTIES[self.difficulty.get()]
            speed_bonus = max(0, int(d["time_bonus"] - elapsed * 5))
            streak_mult = 1 + (self.streak * 0.25)
            pts = int((100 + speed_bonus) * streak_mult)
            self.score += pts; self.correct_guesses += 1; self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            self.msg_label.config(text=f"🎉 PERFECT! Found at index {found_idx} in {elapsed:.1f}s. +{pts} pts! Streak x{self.streak}", fg=ACCENT)
            self.log(f"Round {self.round}: PERFECT guess {guess} == {found_idx}. +{pts} pts (speed {speed_bonus})")
            self.celebrate()
            messagebox.showinfo("PERFECT! 🎉", f"You guessed EXACTLY right!\nKey {self.key} at index {found_idx}\n+{pts} points  |  Streak: {self.streak}")
        else:
            # Close guess = partial points
            if guess is not None:
                dist = abs(guess - found_idx)
                pts = max(0, 50 - dist * 10)
                self.score += pts
                self.log(f"Round {self.round}: Guessed {guess}, actual {found_idx}, distance {dist}. +{pts} pts")
                self.msg_label.config(text=f"Close! You guessed {guess}, actual was {found_idx} (off by {dist}). +{pts} pts", fg=ACCENT3)
                msg = f"Key {self.key} was at index {found_idx}.\nYou guessed {guess} (off by {dist}).\n+{pts} points for being close."
            else:
                pts = 0; dist = 999
                self.log(f"Round {self.round}: No guess, actual {found_idx}. +0")
                msg = f"Key {self.key} was at index {found_idx}.\nYou didn't guess. +0 points."
            self.streak = 0
            if "Survival" in self.mode.get():
                self.lives -= 1
                if self.lives <= 0:
                    self.update_stats(); self.game_over(); return
            messagebox.showinfo("Result", msg)

        self.update_stats()
        # Auto next round after short delay
        self.root.after(600, lambda: self.new_round() if self.game_active else None)

    def celebrate(self):
        # Simple confetti flash on canvas
        for _ in range(30):
            x = random.randint(0, 1040); y = random.randint(0, 120)
            c = random.choice([ACCENT, ACCENT2, ACCENT3, "#f472b6", "#a78bfa"])
            self.canvas.create_oval(x, y, x+10, y+10, fill=c, outline="")
        self.root.update()

    def game_over(self):
        self.game_active = False
        self.msg_label.config(text="💀 GAME OVER — Survival lives exhausted!", fg=DANGER)
        self.log(f"GAME OVER. Final score: {self.score}")
        # Save highscore
        name = simpledialog.askstring("Game Over", f"Game Over!\nFinal Score: {self.score}\nEnter your name for leaderboard:", initialvalue="Player")
        if name:
            highscores = self.highscores
            highscores.append({"name": name, "score": self.score, "difficulty": self.difficulty.get(), "mode": self.mode.get(), "rounds": self.round})
            self.highscores = sorted(highscores, key=lambda x: cast(int, x["score"]), reverse=True)[:10]
            save_scores(self.highscores)
        messagebox.showinfo("Game Over", f"Final Score: {self.score}\nRounds: {self.round}\nBest Streak: {self.best_streak}")
        self.update_stats()

    def tick_timer(self):
        if self.game_active and "Time Attack" in self.mode.get() and not self.paused:
            self.time_left -= 0.1
            if self.time_left <= 0:
                self.time_left = 0
                self.game_active = False
                self.log(f"TIME UP! Final score: {self.score}")
                name = simpledialog.askstring("Time Up!", f"Time's up!\nFinal Score: {self.score}\nEnter name:", initialvalue="Player")
                if name:
                    highscores = self.highscores
                    highscores.append({"name": name, "score": self.score, "difficulty": self.difficulty.get(), "mode": self.mode.get(), "rounds": self.round})
                    self.highscores = sorted(highscores, key=lambda x: cast(int, x["score"]), reverse=True)[:10]
                    save_scores(self.highscores)
                messagebox.showinfo("Time Up!", f"Final Score: {self.score}")
            self.update_stats()
        self.root.after(100, self.tick_timer)

    # ----- DRAWING (from original, improved) -----
    def draw_rectangles(self, array: list[int], colors: list[str]) -> None:
        self.canvas.delete("all")
        if not array:
            return
        W, H = 1040, 360
        bar_w = W / len(array)
        mx = max(array) if max(array) != 0 else 1
        mn = min(array) if min(array) != 0 else 0
        for i, val in enumerate(array):
            # Normalize height so small values still visible
            h_ratio = (val - mn + 5) / (mx - mn + 10)
            h = 40 + h_ratio * (H - 80)
            x0 = i * bar_w + 2; x1 = (i+1) * bar_w - 2
            y0 = H - h; y1 = H - 4
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline="#0f172a", width=1)
            # Index label at bottom
            self.canvas.create_text((x0+x1)/2, H-14, text=str(i), font=("Segoe UI", 8, "bold"), fill="#e2e8f0")
            # Value label (if enabled or if found/guess)
            show = self.show_values_var.get()
            if show or colors[i] in (BAR_FOUND, BAR_CHECKING, BAR_GUESS):
                self.canvas.create_text((x0+x1)/2, y0-12, text=str(val), font=("Segoe UI", 10, "bold"), fill=TEXT)
        # Guess marker
        if self.player_guess is not None and 0 <= self.player_guess < len(array):
            x = self.player_guess * bar_w + bar_w/2
            self.canvas.create_text(x, 18, text="▼ YOUR GUESS", font=("Segoe UI", 9, "bold"), fill=ACCENT3)

    # ----- DIALOGS -----
    def show_help(self):
        messagebox.showinfo("How to Play", 
            "LINEAR SEARCH: THE GAME\n\n"
            "1. A secret array is made + a KEY is chosen.\n"
            "2. Guess which INDEX the key is at.\n"
            "   Click a bar OR type index + Lock Guess.\n"
            "3. Press REVEAL SEARCH - watch it scan left to right.\n"
            "4. Exact guess = BIG points + streak bonus.\n"
            "   Close guess = small points.\n"
            "   Wrong in Survival = lose a life.\n"
            "5. Trick rounds: 25% of rounds the key is NOT in the array!\n"
            "   If you suspect that, DON'T guess and press Reveal.\n\n"
            "Modes:\n"
            "• Classic - endless, just score\n"
            "• Time Attack - 60 seconds, score as much as you can\n"
            "• Survival - 3 lives, wrong = -1 life\n"
            "• Practice - original visualizer, no score\n\n"
            "Tip: On Hard/Hardcore values are hidden - use bar HEIGHTS to guess!"
        )

    def show_leaderboard(self):
        if not self.highscores:
            messagebox.showinfo("Leaderboard", "No scores yet. Play a game first!")
            return
        txt = "🏆 TOP 10 LEADERBOARD 🏆\n\n"
        for i, s in enumerate(self.highscores, 1):
            txt += f"{i}. {s['name']} - {s['score']} pts  ({s['difficulty']} / {s['mode']} / {s['rounds']} rounds)\n"
        messagebox.showinfo("Leaderboard", txt)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = LinearSearchGame()
    game.run()
