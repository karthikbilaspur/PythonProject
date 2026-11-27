import tkinter as tk
from tkinter import messagebox
import random
import time
import difflib

TEXTS = {
    "Easy": [
        "The quick brown fox jumps over the lazy dog",
        "Python is a popular programming language",
        "The sun rises in the east and sets in the west",
        "I love to read books on a rainy day",
        "The cat sits on the mat and watches the birds",
        "She made a cup of tea and sat by the window",
        "We went to the park to play football",
        "The dog barked at the postman this morning",
        "My friend lives in a small house near the river",
        "The stars shine bright on a clear night",
        "He likes to ride his bike to school every day",
        "The baby smiled when she saw her mother",
        "We eat lunch together at noon every day",
        "The flowers in the garden smell very sweet",
        "It is a good day to go for a long walk",
    ],
    "Medium": [
        "The sun was shining brightly in the clear blue sky",
        "The cat purrs contentedly on my lap",
        "She decided to learn a new language this year",
        "The old library had books on every possible subject",
        "After the rain, the streets looked clean and fresh",
        "He practised the piano for two hours every evening",
        "The train arrived late because of heavy fog",
        "They planned a trip to the mountains for the weekend",
        "The museum displayed paintings from many centuries",
        "Her voice was calm even when everyone else panicked",
        "The chef tasted the soup and added a pinch of salt",
        "We watched the sunset from the top of the hill",
        "The river flowed quietly through the green valley",
        "He wrote a letter to his friend who lives abroad",
        "The children built a tall tower out of wooden blocks",
    ],
    "Hard": [
        "The complexity of the human brain is still not fully understood",
        "The universe is a vast and mysterious place",
        "Despite numerous obstacles, she persevered and eventually succeeded",
        "The philosopher argued that knowledge begins with curiosity",
        "Economic uncertainty has affected markets around the world",
        "The archaeologists discovered artefacts buried beneath the ancient city",
        "Technological advancement continues to reshape how we communicate",
        "The committee deliberated for hours before reaching a consensus",
        "His autobiography reveals the struggles behind his remarkable success",
        "The ecosystem depends on a delicate balance between species",
        "She hypothesised that the results would vary with temperature",
        "The novel explores themes of identity, memory, and belonging",
        "Researchers concluded that sleep plays a crucial role in learning",
        "The orchestra performed a symphony that captivated the audience",
        "Understanding history helps us make sense of the present",
    ],
}

TIMER_SECONDS = {"1 minute": 60, "2 minutes": 120, "3 minutes": 180}


class TypingSpeedTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")
        self.root.geometry("720x620")
        self.root.minsize(680, 560)

        self.difficulty = tk.StringVar(value="Easy")
        self.timer_choice = tk.StringVar(value="1 minute")
        self.mode = tk.StringVar(value="Test")  # Test / Practice

        self.text_to_type = ""
        self.start_time = None
        self.time_left = 0
        self.timer_id = None
        self.finished = False
        self.best: dict[str, float] = {"speed": 0.0, "accuracy": 0.0}

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        top = tk.Frame(self.root, padx=16, pady=12)
        top.pack(fill="x")
        tk.Label(top, text="Typing Speed Test", font=("Arial", 22, "bold")).pack()

        controls = tk.Frame(self.root, padx=16)
        controls.pack(fill="x")
        tk.Label(controls, text="Difficulty:").pack(side="left")
        tk.OptionMenu(controls, self.difficulty, *TEXTS.keys()).pack(side="left", padx=(4, 16))
        tk.Label(controls, text="Timer:").pack(side="left")
        tk.OptionMenu(controls, self.timer_choice, *TIMER_SECONDS.keys()).pack(side="left", padx=(4, 16))
        tk.Label(controls, text="Mode:").pack(side="left")
        tk.OptionMenu(controls, self.mode, "Test", "Practice").pack(side="left", padx=(4, 16))

        btns = tk.Frame(self.root, padx=16, pady=8)
        btns.pack(fill="x")
        tk.Button(btns, text="Start Test", command=self.start_test, bg="#4CAF50", fg="white",
                  font=("Arial", 11, "bold"), padx=12).pack(side="left", padx=4)
        tk.Button(btns, text="Submit", command=self.finish).pack(side="left", padx=4)
        tk.Button(btns, text="Reset", command=self.reset).pack(side="left", padx=4)

        # Live stats
        stats = tk.Frame(self.root, padx=16)
        stats.pack(fill="x")
        self.time_var = tk.StringVar(value="Time left: --:--")
        self.live_wpm_var = tk.StringVar(value="Live WPM: 0")
        self.live_acc_var = tk.StringVar(value="Live Accuracy: 100%")
        tk.Label(stats, textvariable=self.time_var, font=("Arial", 13, "bold"), fg="#1565C0").pack(side="left", padx=(0, 24))
        tk.Label(stats, textvariable=self.live_wpm_var, font=("Arial", 11)).pack(side="left", padx=(0, 24))
        tk.Label(stats, textvariable=self.live_acc_var, font=("Arial", 11)).pack(side="left")

        # Target text - with per-char tags
        tk.Label(self.root, text="Type this:", padx=16, anchor="w").pack(fill="x", pady=(10, 2))
        self.target = tk.Text(self.root, height=4, wrap="word", font=("Arial", 15),
                              padx=10, pady=8, state="disabled", bg="#f5f5f5")
        self.target.pack(fill="x", padx=16)
        self.target.tag_config("correct", foreground="#2e7d32")
        self.target.tag_config("wrong", foreground="#c62828", background="#ffebee")
        self.target.tag_config("current", background="#fff9c4")
        self.target.tag_config("pending", foreground="#555")

        tk.Label(self.root, text="Your typing:", padx=16, anchor="w").pack(fill="x", pady=(10, 2))
        self.entry = tk.Text(self.root, height=5, wrap="word", font=("Arial", 15), padx=10, pady=8)
        self.entry.pack(fill="x", padx=16)
        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.bind("<Key>", self._ensure_started)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14), pady=10, justify="left")
        self.result_label.pack(fill="x", padx=16)
        self.best_label = tk.Label(self.root, text="Best (Test mode): —", font=("Arial", 11), fg="gray")
        self.best_label.pack()

    # ---------- Flow ----------
    def start_test(self):
        self._cancel_timer()
        self.text_to_type = random.choice(TEXTS[self.difficulty.get()])
        self._show_target()
        self.entry.config(state="normal")
        self.entry.delete("1.0", tk.END)
        self.entry.focus()
        self.start_time = None  # starts on first keystroke, not on Start click
        self.finished = False
        self.time_left = TIMER_SECONDS[self.timer_choice.get()]
        self.time_var.set(f"Time left: {self.time_left // 60}:{self.time_left % 60:02d}")
        self.live_wpm_var.set("Live WPM: 0")
        self.live_acc_var.set("Live Accuracy: 100%")
        mode_note = "Practice mode — no score saved." if self.mode.get() == "Practice" else "Test started — type to begin timer."
        self.result_label.config(text=mode_note, fg="#333")

    def _ensure_started(self, event: tk.Event[tk.Text] | None = None) -> None:
        # Timer starts on first real character, not on Start button
        if self.start_time is None and not self.finished and self.text_to_type:
            if event and len(event.char) == 1:  # ignore Shift/Ctrl etc.
                self.start_time = time.time()
                if self.mode.get() == "Test":
                    self._tick()

    def _tick(self):
        if self.finished or self.start_time is None:
            return
        elapsed = time.time() - self.start_time
        self.time_left = max(0, TIMER_SECONDS[self.timer_choice.get()] - int(elapsed))
        self.time_var.set(f"Time left: {self.time_left // 60}:{self.time_left % 60:02d}")
        if self.time_left <= 10:
            self.time_var.set(f"Time left: {self.time_left // 60}:{self.time_left % 60:02d}  ⏰ Hurry!")
        if self.time_left <= 0:
            self.finish(auto=True)
            return
        self.timer_id = self.root.after(500, self._tick)

    def _on_key(self, event: tk.Event[tk.Text] | None = None) -> None:
        if not self.text_to_type or self.finished:
            return
        typed = self.entry.get("1.0", "end-1c")
        self._highlight(typed)
        self._update_live_stats(typed)
        # Auto-finish if user completes the text
        if len(typed) >= len(self.text_to_type):
            self.finish()

    def finish(self, auto: bool = False):
        if not self.text_to_type:
            messagebox.showinfo("Typing Test", "Press Start Test first.")
            return
        if self.finished:
            return
        self.finished = True
        self._cancel_timer()
        self.entry.config(state="disabled")

        typed = self.entry.get("1.0", "end-1c")
        elapsed = 0 if self.start_time is None else max(0.1, time.time() - self.start_time)
        # Guard: instant Submit -> elapsed ~0, use 0.1s floor so no ZeroDivisionError
        correct, _ = self._score_chars(typed)
        accuracy = (correct / max(len(typed), len(self.text_to_type))) * 100 if max(len(typed), len(self.text_to_type)) else 0
        # Net WPM: correct chars / 5 per minute (standard formula)
        net_wpm = (correct / 5) / (elapsed / 60)
        gross_wpm = (len(typed.split()) / elapsed) * 60 if typed.strip() else 0

        prefix = "⏰ Time's up! " if auto else ""
        if self.mode.get() == "Practice":
            result = (f"{prefix}Practice complete.\n"
                      f"Accuracy: {accuracy:.1f}%  |  Net WPM: {net_wpm:.1f}  |  Gross WPM: {gross_wpm:.1f}\n"
                      f"(Practice scores are not saved)")
            self.result_label.config(text=result, fg="#333")
            return

        if net_wpm > self.best["speed"]:
            self.best = {"speed": net_wpm, "accuracy": accuracy}
            self.best_label.config(text=f"Best (Test mode): {net_wpm:.1f} WPM, {accuracy:.1f}% accuracy")

        result = (f"{prefix}Accuracy: {accuracy:.1f}%\n"
                  f"Net Speed: {net_wpm:.1f} WPM  (Gross: {gross_wpm:.1f} WPM)\n"
                  f"Correct chars: {correct}/{len(self.text_to_type)}  |  Time: {elapsed:.1f}s")
        self.result_label.config(text=result, fg="#1565C0")

    def reset(self):
        self._cancel_timer()
        self.text_to_type = ""
        self.start_time = None
        self.finished = False
        self._show_target()
        self.entry.config(state="normal")
        self.entry.delete("1.0", tk.END)
        self.time_var.set("Time left: --:--")
        self.live_wpm_var.set("Live WPM: 0")
        self.live_acc_var.set("Live Accuracy: 100%")
        self.result_label.config(text="")

    # ---------- Scoring ----------
    def _score_chars(self, typed: str) -> tuple[int, int]:
        """Count correct chars with alignment (difflib) so one insertion doesn't ruin everything."""
        matcher = difflib.SequenceMatcher(None, typed, self.text_to_type, autojunk=False)
        correct = sum(block.size for block in matcher.get_matching_blocks())
        return correct, len(self.text_to_type)

    def _highlight(self, typed: str) -> None:
        self.target.config(state="normal")
        self.target.delete("1.0", tk.END)
        self.target.insert("1.0", self.text_to_type)
        # Clear tags
        for tag in ("correct", "wrong", "current", "pending"):
            self.target.tag_remove(tag, "1.0", "end")
        # Align typed vs target for fair highlighting
        matcher = difflib.SequenceMatcher(None, typed, self.text_to_type, autojunk=False)
        correct_positions: set[int] = set()
        for block in matcher.get_matching_blocks():
            for i in range(block.size):
                correct_positions.add(block.b + i)
        for i in range(len(self.text_to_type)):
            pos = f"1.{i}"
            end = f"1.{i+1}"
            if i < len(typed):
                self.target.tag_add("correct" if i in correct_positions else "wrong", pos, end)
            elif i == len(typed):
                self.target.tag_add("current", pos, end)
            else:
                self.target.tag_add("pending", pos, end)
        self.target.config(state="disabled")

    def _update_live_stats(self, typed: str) -> None:
        if self.start_time is None:
            return
        elapsed = max(0.1, time.time() - self.start_time)
        correct, _ = self._score_chars(typed)
        net_wpm = (correct / 5) / (elapsed / 60)
        accuracy = (correct / max(len(typed), 1)) * 100 if typed else 100
        # Use max(len) for accuracy so extra chars penalise, same as final score
        accuracy = (correct / max(len(typed), len(self.text_to_type))) * 100 if typed else 100
        self.live_wpm_var.set(f"Live WPM: {net_wpm:.1f}")
        self.live_acc_var.set(f"Live Accuracy: {accuracy:.1f}%")

    def _show_target(self):
        self.target.config(state="normal")
        self.target.delete("1.0", tk.END)
        self.target.insert("1.0", self.text_to_type or "Press Start Test to begin…")
        self.target.config(state="disabled")

    def _cancel_timer(self):
        if self.timer_id is not None:
            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TypingSpeedTest().run()