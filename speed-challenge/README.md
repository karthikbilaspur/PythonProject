# index ⏱️ Speed Story Challenge

Option 2, built with the best code possible - Slot Machine + Stopwatch + Story Generator in ONE game.

indexindex Files

- `index.py` - main game (run this, GUI)
- `README.md` - this file

indexindex How to Run
indexbash
python speed_story_challenge.py
index
No install needed - only Python standard library (`tkinter`).

indexindex How to Play (30 seconds per round)

1. indexPick time:index 15s / 30s / 60s
2. indexPress 🎰 SPIN & STARTindex - 5 slot reels animate and lock one by one
3. indexYou get a prompt:index e.g. `Alice • Tokyo • key • discovered • mysterious`
4. indexTimer starts automaticallyindex - write your story in the box, using the prompt words
5. indexPress ✅ FINISHindex (or time runs out)
6. indexSee your score + Generator's storyindex from the SAME prompt, side by side
7. indexNext round!index Total + Best score tracked. Save all stories with 💾 Save Stories

indexindex The 3 Originals, Merged

| Original | Where It Lives Now |

|---|---|
| Slot Machine | 5 reels: Character / Location / Object / Action / Adjective. Animation locks reels one by one, like a real slot machine. Fair random picker - no cheating. |
| Stopwatch | Live countdown timer (0.1s precision), turns red under 10s, auto-finishes at 0. Also tracks time-left for scoring. |
| Story Generator | Generates ITS story from YOUR exact prompt (not a new random one), so you can fairly compare. 4 templates, not just 1. |

indexindex Scoring (transparent, shown every round)
index
Base         = words you wrote (max 50, 1 pt/word)
Speed Bonus  = seconds left × 2 (finish fast = more)
Prompt Bonus = +10 per prompt word you actually used (max 50)
Length Bonus = +20 if 25+ words, +10 if 15+ words
Total        = Base + Speed + Prompt + Length
index

Example:

- You write 20 words, finish with 12s left, use 4/5 prompt words
- = 20 + 24 + 40 + 10 = index94 pts → ⭐ GREAT!index

Grades: 120+ 🏆 MASTER, 80+ ⭐ GREAT, 40+ 👍 GOOD, else ✍️ KEEP GOING
