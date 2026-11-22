"""
Audiobook Time Saver Calculator - Medium Level
Features: input validation, multiple books, session total, save history to CSV,
speed presets, human-readable formatting, no recursion.
"""
import csv
from datetime import datetime
from pathlib import Path

SPEED_PRESETS = {"slow": 0.75, "normal": 1.0, "fast": 1.25, "faster": 1.5, "2x": 2.0}
HISTORY_FILE = Path("audiobook_history.csv")

def parse_duration(text: str) -> int:
    """Accept HH:MM:SS or MM:SS or minutes as number. Returns total seconds."""
    text = text.strip()
    if not text:
        raise ValueError("Empty duration")
    parts = text.split(":")
    try:
        nums = [float(p) for p in parts]
    except ValueError:
        raise ValueError("Use format HH:MM:SS, e.g. 12:34:56")
    if any(n < 0 for n in nums):
        raise ValueError("Duration cannot be negative")
    if len(nums) == 1:
        return int(nums[0] * 60)  # plain number = minutes
    if len(nums) == 2:
        m, s = nums
        if s >= 60: raise ValueError("Seconds must be < 60")
        return int(m * 60 + s)
    if len(nums) == 3:
        h, m, s = nums
        if m >= 60 or s >= 60: raise ValueError("Minutes/seconds must be < 60")
        return int(h * 3600 + m * 60 + s)
    raise ValueError("Too many ':' parts")

def parse_speed(text: str) -> float:
    text = text.strip().lower()
    if text in SPEED_PRESETS:
        return SPEED_PRESETS[text]
    try:
        speed = float(text)
    except ValueError:
        raise ValueError("Speed must be a number or preset: " + ", ".join(SPEED_PRESETS))
    if not 0.25 <= speed <= 4.0:
        raise ValueError("Speed must be between 0.25x and 4.0x")
    return speed

def fmt(total_seconds: float) -> str:
    total_seconds = int(round(total_seconds))
    h, rem = divmod(total_seconds, 3600)
    m, s = divmod(rem, 60)
    if h: return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"

def save_history(title: str, orig: int, speed: float, adjusted: float, saved: float) -> None:
    exists = HISTORY_FILE.exists()
    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists: w.writerow(["date","title","original_seconds","speed","adjusted_seconds","saved_seconds"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), title, orig, speed, int(adjusted), int(saved)])

def main():
    print("=== Audiobook Time Saver Calculator ===")
    print("Presets:", ", ".join(f"{k}={v}x" for k,v in SPEED_PRESETS.items()))
    session_orig = session_saved = 0
    while True:
        title = input("\nBook title (or 'quit'): ").strip()
        if title.lower() in ("quit","q","exit"): break
        if not title: title = "Untitled"
        try:
            orig = parse_duration(input("Duration [HH:MM:SS or minutes]: "))
            speed = parse_speed(input("Speed [e.g. 1.5 / fast]: "))
        except ValueError as e:
            print(f"Error: {e}"); continue
        adjusted = orig / speed
        saved = orig - adjusted
        pct = (saved / orig * 100) if orig else 0
        session_orig += orig; session_saved += saved
        print(f"\nOriginal : {fmt(orig)}")
        print(f"At {speed}x  : {fmt(adjusted)}")
        print(f"Saved    : {fmt(saved)} ({pct:.1f}%)")
        print(f"Session total saved: {fmt(session_saved)}")
        if input("Save to history? (y/n): ").strip().lower() == "y":
            save_history(title, orig, speed, adjusted, saved)
            print(f"Saved to {HISTORY_FILE}")
    print(f"\nDone. Session: {fmt(session_orig)} -> saved {fmt(session_saved)}")

if __name__ == "__main__":
    main()
