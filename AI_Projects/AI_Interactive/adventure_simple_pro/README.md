# Upgraded version of your minimal Node / Game class

Original vs Pro
Original Problem Pro Fix
["left", "right"] - player sees ugly IDs Option("Go left (blue glow)", "left") - nice label + ID
No inventory - key does nothing Inventory list + check: chest needs key
Both endings say "Game over!" 3 distinct endings with messages
No way to quit/save Menu with if-elif-else
Crashes on "abc" input Validation loop
Features Added (as you asked: if, if-else, elif)
python

Ending logic

if node.id == "open_chest":
    if "key" in self.inventory:
        self.current_id = "open_chest_with_key" # Gold Ending
    else:
        print("BAD ENDING - mimic eats you") # Bad Ending
elif node.is_ending:
    print(node.ending_message)

Menu logic

if m == "1": continue
elif m == "2": show_inventory()
elif m == "3": save_game()
elif m == "4": quit()
else: invalid
Endings Now
BAD ENDING: Go right -> Open chest without key -> Mimic eats you
GOLD ENDING: Left -> Take key -> Right -> Open chest with key -> Treasure!
SECRET ENDING: Left -> Take key -> Unlock secret door -> Keeper of Stories

How to Run
bash
python adventure_simple_pro.py
=== ADVENTURE SIMPLE PRO ===

[Location: start | Inventory: Empty | Steps: 0]
You are at the start. An ancient forest splits in two.

1. Go left (blue glow)

2. Go right (gold glow)

Enter your choice: 1
Place in your folder
AI_Based/ (rename to ai-based for pro look)
├── adventure_simple_pro.py  <- this file (simple version)
├── adventure_engine_pro.py  <- previous complex version with health/traits
├── chronicle_weaver.py
├── vault_of_genesis.py
├── echo_scribe.py
├── storyverse_unified.py
└── README.md
Use adventure_simple_pro.py for interviews where they want clean simple code.
Use adventure_engine_pro.py for portfolio where you want to show health, traits, save/load, damage system.

Pro Naming Used
File: adventure_simple_pro.py = snake_case (pro)
Class: AdventureEnginePro, Node, Option = PascalCase (pro)
Constant: SAVE_PATH would be UPPER_SNAKE if needed
No A_B or A-B anywhere
