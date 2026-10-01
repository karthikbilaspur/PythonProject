# Echo Quest - Adventure Node Engine Pro

Upgraded version of your original Node / Character / Game code.
Fixed all interview-level bugs and made it recruiter-ready.

What was wrong in your original?
Effect bug: self.current_node.effects was checked AFTER moving to next node, so add_item never worked on the node you were on.
Infinite outer loop: while True: game.play() -> game_menu() called exit() inside, hard kill.
Hardcoded effects: add_item always added "key" even if effect was different.
No requirement system: Could open chest without key.
No health/traits use: health existed but never changed.
All fixed in pro version.

What’s upgraded?
Code Quality (Pro Naming: a_b, A_B, PascalCase)
Node, Option, Character now @dataclass with type hints
GameEngine class - single responsibility
File: adventure_engine_pro.py (snake_case = pro)
Constants: SAVE_FILE = "savegame.json" (UPPER_SNAKE)
No more A_B mixing

New Features
Option system: Each option has text, next_node, requires_item (e.g., chest needs key)
Effect engine: add_item, remove_item, damage, heal, flag, trait_X
Character system: health 100, inventory[], traits{bravery, curiosity}, flags{found_treasure}
Save/Load: Saves to savegame.json with timestamp
Two Endings: found_treasure (Gold ending) and secret_keeper (Secret Library ending)
Menu: Uses if-elif-else as you wanted: 1 Continue, 2 Info, 3 Save, 4 Load, 5 Quit
Input validation: No crash on "abc" input, shows LOCKED options
Folder Structure
Place this file inside your AI_Based folder (rename to ai-based for pro):

ai-based/
├── chronicle_weaver.py
├── vault_of_genesis.py
├── echo_scribe.py
├── storyverse_unified.py
├── adventure_engine_pro.py  <- NEW (this file)
├── README.md
├── requirements.txt
└── savegame.json (auto-created)
How to Run

bash
pip install -r requirements.txt
python adventure_engine_pro.py
Gameplay:

Enter your name: Karthik 

--- START ---
You stand at a crossroads...

1. Go left towards the blue glow
2. Go right towards the gold glow
3. Check your inventory

Enter choice (number) or 'menu': 1

--- LEFT ---
...
Commands:

Number: choose option
menu: opens Game Menu
World Map
start -> left -> open_door -> take_key (get key) -> unlock_door [SECRET ENDING]
      -> right -> open_chest (needs key) -> [GOLD ENDING]
               -> force_chest (lose 20 HP) -> go_back
      -> go_back -> loops to start
If-Else Logic You Asked For
python

In apply_effects

if key == "add_item": ...
elif key == "damage": ...
elif key == "flag": ...

In menu
if c == "1": continue
elif c == "2": show_info()
elif c == "3": save()
elif c == "5": quit
else: invalid

Next Pro Steps
Add color with rich: pip install rich -> from rich import print
Add more nodes from JSON file instead of hardcoded
Turn inventory check into a real node with options
Add combat: if character.traits["bravery"] > 3: win
License
MIT - Add to your portfolio as "Node-Based RPG Engine in Python
