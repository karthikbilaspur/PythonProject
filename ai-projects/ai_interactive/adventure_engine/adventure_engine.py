# adventure_engine_pro.py - Pro Version of your Node Game
# Fixed: Infinite loops, effect system, inventory, save/load, health, traits

import json
import random
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

# --- DATA MODELS (Pro: dataclass + type hints) ---

@dataclass
class Option:
    text: str           # What player sees: "Open the ancient door"
    next_node: str      # ID: "open_door"
    requires_item: Optional[str] = None  # e.g., "key"

@dataclass
class Node:
    id: str
    text: str
    options: List[Option] = field(default_factory=list)
    effects: Dict[str, any] = field(default_factory=dict)  # e.g., {"add_item": "key", "heal": 20}
    is_ending: bool = False

@dataclass
class Character:
    name: str
    health: int = 100
    inventory: List[str] = field(default_factory=list)
    traits: Dict[str, int] = field(default_factory=dict)  # e.g., {"bravery": 5}
    flags: Dict[str, bool] = field(default_factory=dict) # e.g., {"found_treasure": True}

# --- GAME ENGINE ---

class GameEngine:
    def __init__(self, save_file="savegame.json"):
        self.save_file = Path(save_file)
        self.nodes = self._build_world()
        self.character = Character(name="Player", traits={"bravery": 0, "curiosity": 0})
        self.current_node_id = "start"
        self.game_over = False

    def _build_world(self) -> Dict[str, Node]:
        # Your original world, but now with Option objects + proper effects
        return {
            "start": Node(
                id="start",
                text="You stand at a crossroads in a dark forest. Ancient whispers. Left path glows blue, right path glows gold.",
                options=[
                    Option("Go left towards the blue glow", "left"),
                    Option("Go right towards the gold glow", "right"),
                    Option("Check your inventory", "inventory_check")
                ]
            ),
            "left": Node(
                id="left",
                text="You went left. A stone door covered in runes blocks you.",
                options=[
                    Option("Open the door", "open_door"),
                    Option("Go back to crossroads", "go_back")
                ]
            ),
            "right": Node(
                id="right",
                text="You went right. A locked treasure chest sits on a pedestal.",
                options=[
                    Option("Open the chest (needs key)", "open_chest", requires_item="key"),
                    Option("Try to force it open (lose 20 HP)", "force_chest"),
                    Option("Go back to crossroads", "go_back")
                ]
            ),
            "open_door": Node(
                id="open_door",
                text="The door creaks open. Inside, a single silver key floats.",
                options=[
                    Option("Take the key", "take_key"),
                    Option("Leave it and go back", "leave_key")
                ]
            ),
            "take_key": Node(
                id="take_key",
                text="You took the silver key. It hums. A secret door appears on the far wall.",
                effects={"add_item": "key", "trait_curiosity": 1},
                options=[
                    Option("Unlock secret door with key", "unlock_door", requires_item="key"),
                    Option("Go back to crossroads", "go_back")
                ]
            ),
            "leave_key": Node(
                id="leave_key",
                text="You leave the key. The room feels colder.",
                options=[Option("Go back", "go_back")]
            ),
            "open_chest": Node(
                id="open_chest",
                text="The key fits! The chest opens - 1000 gold and the Crown of Echoes!",
                effects={"add_item": "crown", "flag": "found_treasure"},
                is_ending=True
            ),
            "force_chest": Node(
                id="force_chest",
                text="You smash it! It opens but a trap cuts you.",
                effects={"damage": 20, "add_item": "broken_gold", "trait_bravery": 1},
                is_ending=False,
                options=[Option("Go back, wounded", "go_back")]
            ),
            "unlock_door": Node(
                id="unlock_door",
                text="Secret door opens to a library of infinite stories. You are now the Keeper!",
                effects={"flag": "secret_keeper"},
                is_ending=True
            ),
            "go_back": Node(
                id="go_back",
                text="You return to the crossroads. The forest shifts.",
                options=[
                    Option("Go left", "left"),
                    Option("Go right", "right")
                ]
            ),
            "inventory_check": Node(
                id="inventory_check",
                text="Checking inventory...",
                options=[Option("Return to crossroads", "start")]
            ),
        }

    # --- Core Logic with if-elif-else as you wanted ---
    def apply_effects(self, effects: Dict):
        for key, value in effects.items():
            if key == "add_item":
                if value not in self.character.inventory:
                    self.character.inventory.append(value)
                    print(f" >> [INVENTORY] Added: {value}")
            elif key == "remove_item":
                if value in self.character.inventory:
                    self.character.inventory.remove(value)
                    print(f" >> [INVENTORY] Removed: {value}")
            elif key == "damage":
                self.character.health -= value
                print(f" >> [HEALTH] -{value} HP! Current: {self.character.health}")
                if self.character.health <= 0:
                    self.game_over = True
                    print(" >> You have fallen...")
            elif key == "heal":
                self.character.health = min(100, self.character.health + value)
                print(f" >> [HEALTH] +{value} HP! Current: {self.character.health}")
            elif key == "flag":
                self.character.flags[value] = True
                print(f" >> [FLAG] {value} = True")
            elif key.startswith("trait_"):
                trait = key.replace("trait_", "")
                self.character.traits[trait] = self.character.traits.get(trait, 0) + value
                print(f" >> [TRAIT] {trait} +{value}")

    def display_character_info(self):
        print("\n" + "="*40)
        print(f"Name: {self.character.name}")
        print(f"Health: {self.character.health}/100")
        print(f"Inventory: {', '.join(self.character.inventory) if self.character.inventory else 'Empty'}")
        print(f"Traits: {self.character.traits}")
        print(f"Flags: {self.character.flags}")
        print("="*40 + "\n")

    def save_game(self):
        data = {
            "character": self.character.__dict__,
            "current_node": self.current_node_id,
            "date": str(datetime.now())
        }
        self.save_file.write_text(json.dumps(data, indent=2))
        print(f"Game saved to {self.save_file}")

    def load_game(self):
        if not self.save_file.exists():
            print("No save file found.")
            return False
        data = json.loads(self.save_file.read_text())
        self.character = Character(**data["character"])
        self.current_node_id = data["current_node"]
        print(f"Loaded save from {data['date']}")
        return True

    def play(self):
        self.character.name = input("Enter your name: ").strip() or "Player"
        print(f"\nWelcome, {self.character.name}! Type number to choose.\n")

        while not self.game_over:
            node = self.nodes[self.current_node_id]

            # Special handling for inventory check
            if node.id == "inventory_check":
                self.display_character_info()
                self.current_node_id = "start"
                continue

            print(f"\n--- {node.id.upper()} ---")
            print(node.text)

            # Apply effects on entry (your old code only applied on next node - fixed)
            if node.effects:
                self.apply_effects(node.effects)

            # Check ending - if-elif-else structure
            if node.is_ending:
                if "found_treasure" in self.character.flags:
                    print("\n*** VICTORY! You won with treasure! ***")
                elif "secret_keeper" in self.character.flags:
                    print("\n*** SECRET ENDING: You became the Keeper of Stories! ***")
                else:
                    print("\n*** Game Over - Ending reached ***")
                self.display_character_info()
                break
            elif self.character.health <= 0:
                print("\n*** Game Over - You died ***")
                break

            # Show options with requirement check
            valid_options = []
            for i, opt in enumerate(node.options):
                # if-else for item requirement
                if opt.requires_item:
                    if opt.requires_item in self.character.inventory:
                        print(f"{i+1}. {opt.text} [Requires {opt.requires_item} - OK]")
                        valid_options.append(opt)
                    else:
                        print(f"{i+1}. {opt.text} [Requires {opt.requires_item} - LOCKED]")
                else:
                    print(f"{i+1}. {opt.text}")
                    valid_options.append(opt)

            # Input loop with validation
            while True:
                choice = input("\nEnter choice (number) or 'menu': ").strip().lower()
                
                if choice == "menu":
                    if not self.game_menu():
                        return  # quit from menu
                    break  # continue game after menu

                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(node.options):
                        selected = node.options[idx]
                        # Check requirement again
                        if selected.requires_item and selected.requires_item not in self.character.inventory:
                            print(f"You need {selected.requires_item}!")
                            continue
                        self.current_node_id = selected.next_node
                        break
                    else:
                        print("Invalid number. Try again.")
                except ValueError:
                    print("Please enter a number or 'menu'.")

    def game_menu(self) -> bool:
        # Returns True to continue, False to quit
        while True:
            print("\n--- GAME MENU ---")
            print("1. Continue playing")
            print("2. Display character info")
            print("3. Save game")
            print("4. Load game")
            print("5. Quit game")
            c = input("Choice: ").strip()

            if c == "1":
                return True
            elif c == "2":
                self.display_character_info()
            elif c == "3":
                self.save_game()
            elif c == "4":
                self.load_game()
            elif c == "5":
                print("Goodbye!")
                return False
            else:
                print("Invalid choice. Use 1-5.")

# --- MAIN ---
if __name__ == "__main__":
    game = GameEngine()
    game.play()
