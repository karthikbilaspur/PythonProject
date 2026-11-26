"""
Speed Story Challenge - BEST VERSION
Combines 3 projects:
  1. Slot Machine  -> fair random prompt picker (Character/Location/Object/Action/Adjective)
  2. Stopwatch     -> live timer + countdown pressure (30s default)
  3. Story Generator -> generates ITS version of same prompt to compare with yours

HOW TO PLAY:
  1. Pick time (15 / 30 / 60s) -> Press SPIN
  2. Slots animate -> you get a prompt, e.g. Alice + Tokyo + key + discovered + mysterious
  3. Timer starts automatically. Write your 1+ sentence story using the prompt words.
  4. Press FINISH (or time runs out) -> timer stops.
  5. Generator writes ITS story from same prompt.
  6. You get a score: Speed + Words + Prompt words used + Bonus.
  7. Next round! Best score + history saved to my_stories.txt

SCORING (transparent, shown after each round):
  Base        = words you wrote (max 50 pts, 1 pt/word)
  Speed Bonus = seconds left * 2 (finish fast = more)
  Prompt Bonus= +10 per prompt word you actually used (max 50)
  Length Bonus= +20 if 25+ words, +10 if 15+ words
  Total       = Base + Speed + Prompt + Length

Run: python index.py
Needs: ONLY Python standard library (tkinter) - no install!
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import random, time, re
from datetime import datetime
from typing import cast

# ---------- Data (expanded from originals) ----------
CHARACTERS = ["Alice", "Bob", "Charlie", "David", "Emily", "Zara", "Arjun", "Maya", "Leo", "Nina"]
LOCATIONS  = ["Paris", "New York", "Tokyo", "London", "Sydney", "Mumbai", "Cairo", "Berlin", "Toronto", "Seoul"]
OBJECTS    = ["book", "key", "phone", "wallet", "jacket", "map", "camera", "ring", "letter", "compass"]
ACTIONS    = ["found", "lost", "stole", "discovered", "hid", "bought", "dropped", "chased"]
ADJECTIVES = ["mysterious", "beautiful", "old", "shiny", "expensive", "glowing", "ancient", "tiny"]

# Slot symbols for flavour (from Slot Machine project)
SLOT_SYMBOLS = ["7", "BAR", "CHERRY", "LEMON", "ORANGE"]

# ---------- Story Generator (from original, upgraded) ----------
class StoryGenerator:
    """Generates a story from a GIVEN prompt (not random) so it's comparable to yours."""
    TEMPLATES = [
        "One day, {char} was walking through {loc} when they {act} a {adj} {obj}. It was so {adj} that {char} decided to keep it. But little did {char} know, this {obj} would change their life forever.",
        "It all started in {loc}. {char} had never believed in luck, until they {act} a {adj} {obj} on a quiet street. From that moment, nothing in {loc} felt ordinary again.",
        "Everyone in {loc} knew about the {adj} {obj}. But only {char} had the courage to {act} it. What happened next, no one in {loc} could have predicted.",
        "{char} arrived in {loc} with nothing but a backpack. Then, in one strange afternoon, they {act} a {adj} {obj} — and suddenly, {loc} became the start of a brand-new life.",
    ]
    def generate(self, prompt: dict[str, str]) -> str:
        t = random.choice(self.TEMPLATES)
        return t.format(char=prompt["character"], loc=prompt["location"],
                        obj=prompt["object"], act=prompt["action"], adj=prompt["adjective"])
    def generate_random(self) -> tuple[dict[str, str], str]:
        prompt = {
            "character": random.choice(CHARACTERS),
            "location": random.choice(LOCATIONS),
            "object": random.choice(OBJECTS),
            "action": random.choice(ACTIONS),
            "adjective": random.choice(ADJECTIVES),
        }
        return prompt, self.generate(prompt)

# ---------- Scoring ----------
def score_story(user_text: str, prompt: dict[str, str], seconds_left: float, time_limit: int) -> dict[str, int | str | list[str]]:
    words = re.findall(r"\b[\w']+\b", user_text)
    word_count = len(words)
    lower = user_text.lower()
    # Prompt words used (character/location/object/action/adjective)
    used: list[str] = []
    for key in ["character", "location", "object", "action", "adjective"]:
        if prompt[key].lower() in lower:
            used.append(prompt[key])
    base = min(word_count, 50)
    speed = max(0, min(int(seconds_left), time_limit) * 2)
    prompt_bonus = len(used) * 10
    length_bonus = 20 if word_count >= 25 else (10 if word_count >= 15 else 0)
    total = base + speed + prompt_bonus + length_bonus
    grade = "🏆 MASTER STORYTELLER" if total >= 120 else ("⭐ GREAT!" if total >= 80 else ("👍 GOOD!" if total >= 40 else "✍️ KEEP GOING!"))
    return {"words": word_count, "used": used, "base": base, "speed": speed,
            "prompt_bonus": prompt_bonus, "length_bonus": length_bonus,
            "total": total, "grade": grade}

# ---------- GUI ----------
class SpeedStoryChallenge:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("⏱️ Speed Story Challenge - Slot + Stopwatch + Story Generator")
        self.root.geometry("950x750")
        self.root.minsize(850, 650)
        self.generator = StoryGenerator()
        self.prompt = None
        self.time_limit = 30
        self.time_left = 30
        self.start_time = None
        self.timer_running = False
        self.timer_job = None
        self.round_no = 0
        self.total_score = 0
        self.best_score = 0
        self.history: list[dict[str, object]] = []
        self.spin_job = None
        self._build_ui()

    # ----- UI -----
    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1f2937"); header.pack(fill=tk.X)
        tk.Label(header, text="⏱️  SPEED STORY CHALLENGE", font=("Helvetica", 18, "bold"), bg="#1f2937", fg="white").pack(side=tk.LEFT, padx=12, pady=10)
        tk.Label(header, text="Spin → Write fast → Beat the Generator!", bg="#1f2937", fg="#fbbf24", font=("Helvetica", 11)).pack(side=tk.RIGHT, padx=12)

        # Controls row
        ctrl = tk.Frame(self.root); ctrl.pack(fill=tk.X, padx=12, pady=8)
        tk.Label(ctrl, text="Time:").pack(side=tk.LEFT)
        self.time_var = tk.StringVar(value="30s")
        for label in ["15s", "30s", "60s"]:
            tk.Radiobutton(ctrl, text=label, variable=self.time_var, value=label, command=self._set_time).pack(side=tk.LEFT, padx=3)
        self.spin_btn = tk.Button(ctrl, text="🎰  SPIN & START", font=("Helvetica", 12, "bold"), bg="#22c55e", fg="white", command=self.spin)
        self.spin_btn.pack(side=tk.LEFT, padx=12)
        self.finish_btn = tk.Button(ctrl, text="✅ FINISH", font=("Helvetica", 12, "bold"), bg="#2563eb", fg="white", command=self.finish, state=tk.DISABLED)
        self.finish_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="💾 Save Stories", command=self.save_stories).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="🔄 New Round", command=self.new_round).pack(side=tk.LEFT, padx=5)

        # Timer + Score
        info = tk.Frame(self.root); info.pack(fill=tk.X, padx=12)
        self.timer_label = tk.Label(info, text="⏱  30.0s  |  Round 0  |  Total: 0  |  Best: 0", font=("Helvetica", 14, "bold"), fg="#dc2626")
        self.timer_label.pack(side=tk.LEFT)
        self.word_label = tk.Label(info, text="Words: 0", font=("Helvetica", 12)); self.word_label.pack(side=tk.RIGHT)

        # Slot reels (5 slots)
        slot_frame = tk.LabelFrame(self.root, text="🎰  SLOT PROMPT  (spin to get your story ingredients)", font=("Helvetica", 11, "bold"))
        slot_frame.pack(fill=tk.X, padx=12, pady=8)
        self.reel_labels: list[tk.Label] = []
        titles = ["Character", "Location", "Object", "Action", "Adjective"]
        for title in titles:
            col = tk.Frame(slot_frame); col.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4, pady=6)
            tk.Label(col, text=title, font=("Helvetica", 10, "bold"), fg="#555").pack()
            lbl = tk.Label(col, text="❓", font=("Helvetica", 16, "bold"), bg="#fef3c7", relief=tk.RIDGE, padx=8, pady=8)
            lbl.pack(fill=tk.X)
            self.reel_labels.append(lbl)

        # Prompt line
        self.prompt_label = tk.Label(self.root, text="Press SPIN to get your prompt!", font=("Helvetica", 12, "italic"), fg="#6b7280", wraplength=900, justify=tk.LEFT)
        self.prompt_label.pack(fill=tk.X, padx=12)

        # Your story
        tk.Label(self.root, text="✍️  YOUR STORY (use all 5 prompt words for max bonus):", font=("Helvetica", 11, "bold")).pack(anchor=tk.W, padx=12, pady=(8,0))
        self.story_text = tk.Text(self.root, height=6, font=("Helvetica", 12), wrap=tk.WORD)
        self.story_text.pack(fill=tk.X, padx=12, pady=4)
        self.story_text.bind("<KeyRelease>", self._on_type)
        self.story_text.config(state=tk.DISABLED)

        # Result area: Your score + Generator story
        result_frame = tk.LabelFrame(self.root, text="🏁  RESULT  —  You vs Generator (same prompt)", font=("Helvetica", 11, "bold"))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        self.result_text = tk.Text(result_frame, height=10, font=("Helvetica", 11), wrap=tk.WORD, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    def _set_time(self):
        self.time_limit = int(self.time_var.get().replace("s",""))
        self.time_left = self.time_limit
        self._update_timer_label()

    def _update_timer_label(self):
        color = "#dc2626" if self.time_left <= 10 else "#111827"
        self.timer_label.config(text=f"⏱  {self.time_left:.1f}s  |  Round {self.round_no}  |  Total: {int(self.total_score)}  |  Best: {self.best_score}", fg=color)

    def _on_type(self, event: tk.Event[tk.Text] | None = None) -> None:
        text = self.story_text.get("1.0", tk.END)
        words = len(re.findall(r"\b[\w']+\b", text))
        self.word_label.config(text=f"Words: {words}")

    # ----- Game flow -----
    def spin(self):
        # Reset round
        self.time_limit = int(self.time_var.get().replace("s",""))
        self.time_left = float(self.time_limit)
        self.round_no += 1
        self.prompt = None
        self.story_text.config(state=tk.NORMAL); self.story_text.delete("1.0", tk.END)
        self._set_result("")
        self.spin_btn.config(state=tk.DISABLED); self.finish_btn.config(state=tk.DISABLED)
        self._update_timer_label()
        # Slot animation: cycle random values, stop reels one by one
        self.spin_step = 0
        self.final_prompt = {
            "character": random.choice(CHARACTERS), "location": random.choice(LOCATIONS),
            "object": random.choice(OBJECTS), "action": random.choice(ACTIONS),
            "adjective": random.choice(ADJECTIVES),
        }
        self._animate_spin()

    def _animate_spin(self):
        # 25 steps, each reel locks after 5 steps more than previous
        lists = [CHARACTERS, LOCATIONS, OBJECTS, ACTIONS, ADJECTIVES]
        keys = ["character","location","object","action","adjective"]
        for i, lst in enumerate(lists):
            if self.spin_step < 5 + i*4:
                self.reel_labels[i].config(text=random.choice(lst))
            else:
                self.reel_labels[i].config(text=self.final_prompt[keys[i]])
        self.spin_step += 1
        if self.spin_step < 25:
            self.spin_job = self.root.after(80, self._animate_spin)
        else:
            self.prompt = self.final_prompt
            self.prompt_label.config(text=f"Your prompt →  {self.prompt['character']}  •  {self.prompt['location']}  •  {self.prompt['object']}  •  {self.prompt['action']}  •  {self.prompt['adjective']}", fg="#111827")
            self.story_text.config(state=tk.NORMAL); self.story_text.focus()
            self.finish_btn.config(state=tk.NORMAL)
            self.start_time = time.time()
            self.timer_running = True
            self._tick()

    def _tick(self):
        if not self.timer_running: return
        if self.start_time is None: return
        elapsed = time.time() - self.start_time
        self.time_left = max(0.0, self.time_limit - elapsed)
        self._update_timer_label()
        if self.time_left <= 0:
            self.finish(timeout=True); return
        self.timer_job = self.root.after(100, self._tick)

    def finish(self, timeout: bool = False):
        if not self.timer_running and not timeout: return
        self.timer_running = False
        if self.timer_job: self.root.after_cancel(self.timer_job)
        user_text = self.story_text.get("1.0", tk.END).strip()
        if not user_text:
            messagebox.showinfo("No story", "You wrote nothing! Try again - spin and write at least one sentence.")
            self.spin_btn.config(state=tk.NORMAL); return
        # Score
        prompt = self.prompt
        if prompt is None: return
        result = score_story(user_text, prompt, self.time_left, self.time_limit)
        round_score = cast(int, result["total"])
        self.total_score += round_score; self.best_score = max(self.best_score, round_score)
        gen_story = self.generator.generate(prompt)
        # Save history
        entry: dict[str, object] = {"round": self.round_no, "prompt": dict(prompt), "you": user_text,
                 "generator": gen_story, "score": result["total"], "time_left": round(self.time_left,1),
                 "at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.history.append(entry)
        # Show result
        used_words = result["used"] if isinstance(result["used"], list) else []
        used_str = ", ".join(used_words) if used_words else "none - you missed prompt words!"
        text = (f"Round {self.round_no} - {result['grade']}\n"
                f"{'TIME UP!' if timeout else 'Finished!'}  Time left: {self.time_left:.1f}s\n\n"
                f"YOUR SCORE: {result['total']} pts  (Words {result['base']} + Speed {result['speed']} + Prompt {result['prompt_bonus']} + Length {result['length_bonus']})\n"
                f"Words: {result['words']}  |  Prompt words used ({len(used_words)}/5): {used_str}\n\n"
                f"--- YOUR STORY ---\n{user_text}\n\n"
                f"--- GENERATOR'S STORY (same prompt) ---\n{gen_story}\n\n"
                f"Who won? If your story used more prompt words / is more creative, YOU win! Generator wins on speed.\n"
                f"Total: {self.total_score}  |  Best: {self.best_score}")
        self._set_result(text)
        self.story_text.config(state=tk.DISABLED)
        self.finish_btn.config(state=tk.DISABLED); self.spin_btn.config(state=tk.NORMAL)
        self._update_timer_label()

    def _set_result(self, text: str) -> None:
        self.result_text.config(state=tk.NORMAL); self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text); self.result_text.config(state=tk.DISABLED)

    def new_round(self):
        self.timer_running = False
        if self.timer_job: 
            try: self.root.after_cancel(self.timer_job)
            except: pass
        self.story_text.config(state=tk.NORMAL); self.story_text.delete("1.0", tk.END)
        self._set_result(""); self.prompt_label.config(text="Press SPIN to get your prompt!", fg="#6b7280")
        for lbl in self.reel_labels: lbl.config(text="❓")
        self.spin_btn.config(state=tk.NORMAL); self.finish_btn.config(state=tk.DISABLED)
        self.time_left = float(self.time_limit); self._update_timer_label()

    def save_stories(self):
        if not self.history:
            messagebox.showinfo("Nothing to save", "Play at least one round first!"); return
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="my_stories.txt",
                                            filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if not path: return
        lines = ["SPEED STORY CHALLENGE - My Stories\n" + "="*50 + "\n"]
        for h in self.history:
            lines.append(f"\nRound {h['round']} | Score {h['score']} | Time left {h['time_left']}s | {h['at']}")
            p = cast(dict[str, str], h["prompt"]); lines.append(f"Prompt: {p['character']} / {p['location']} / {p['object']} / {p['action']} / {p['adjective']}")
            lines.append(f"YOU: {h['you']}")
            lines.append(f"GENERATOR: {h['generator']}\n")
        with open(path, "w", encoding="utf-8") as f: f.write("\n".join(lines))
        messagebox.showinfo("Saved", f"Saved {len(self.history)} stories to:\n{path}")

def main():
    root = tk.Tk()
    app = SpeedStoryChallenge(root)
    root.mainloop()

if __name__ == "__main__":
    main()
