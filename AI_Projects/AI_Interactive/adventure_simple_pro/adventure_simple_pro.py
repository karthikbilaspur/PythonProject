# adventure_simple_pro.py - Pro Upgrade of your simple Node Game
# Upgraded with: dataclass, type hints, proper if-elif-else, endings, inventory

from dataclasses import dataclass, field
from typing import Dict, List
import json
from pathlib import Path
from datetime import datetime

@dataclass
class Option:
    label: str  # What player sees
    next_id: str # Where it goes

@dataclass
class Node:
    id: str
    text: str
    options: List[Option] = field(default_factory=list)
    is_ending: bool = False
    ending_message: str = ""

class AdventureEnginePro:
    def __init__(self):
        self.nodes = self._build_world()
        self.current_id = "start"
        self.inventory: List[str] = []
        self.history: List[str] = []
        self.save_path = Path("simple_save.json")

    def _build_world(self) -> Dict[str, Node]:
        # Pro: Options now have nice labels, not raw IDs
        return {
            "start": Node(
                id="start",
                text="You are at the start. An ancient forest splits in two.",
                options=[
                    Option("Go left (blue glow)", "left"),
                    Option("Go right (gold glow)", "right"),
                ]
            ),
            "left": Node(
                id="left",
                text="You went left. You see a stone door covered in moss.",
                options=[
                    Option("Open the door", "open_door"),
                    Option("Go back to start", "go_back"),
                ]
            ),
            "right": Node(
                id="right",
                text="You went right. A treasure chest sits on a pedestal, locked.",
                options=[
                    Option("Try to open the chest", "open_chest"),
                    Option("Go back to start", "go_back"),
                ]
            ),
            "open_door": Node(
                id="open_door",
                text="You opened the door. A room with a silver key on a table.",
                options=[
                    Option("Take the key", "take_key"),
                    Option("Leave the key", "leave_key"),
                ]
            ),
            "open_chest": Node(
                id="open_chest",
                text="You opened the chest.",
                options=[],  # Will be resolved in play() with if-elif
                is_ending=True,
                ending_message="No key! The chest is a mimic and eats you. BAD ENDING."
            ),
            "go_back": Node(
                id="go_back",
                text="You went back to the start. The forest seems to shift.",
                options=[
                    Option("Go left", "left"),
                    Option("Go right", "right"),
                ]
            ),
            "take_key": Node(
                id="take_key",
                text="You took the key. It hums. A secret door appears!",
                options=[
                    Option("Unlock secret door with key", "unlock_door"),
                    Option("Go back to start", "go_back"),
                ]
            ),
            "leave_key": Node(
                id="leave_key",
                text="You left the key. The room goes dark.",
                options=[Option("Go back to start", "go_back")]
            ),
            "unlock_door": Node(
                id="unlock_door",
                text="You unlocked the door. A hidden library of infinite stories awaits!",
                is_ending=True,
                ending_message="SECRET ENDING: You became Keeper of Stories! You win with knowledge."
            ),
            # Special chest ending if you have key - handled dynamically
            "open_chest_with_key": Node(
                id="open_chest_with_key",
                text="Your key glows! The chest opens - 1000 gold and Crown of Echoes!",
                is_ending=True,
                ending_message="GOLD ENDING: Treasure! Congratulations!"
            ),
        }

    def display_status(self):
        print(f"\n[Location: {self.current_id} | Inventory: {self.inventory if self.inventory else 'Empty'} | Steps: {len(self.history)}]")

    def save_game(self):
        data = {"current": self.current_id, "inventory": self.inventory, "history": self.history, "date": str(datetime.now())}
        self.save_path.write_text(json.dumps(data, indent=2))
        print(f">> Saved to {self.save_path}")

    def play(self):
        print("=== ADVENTURE SIMPLE PRO ===\nType number to choose, or 'menu'\n")

        while True:
            node = self.nodes[self.current_id]
            self.display_status()
            print(f"\n{node.text}")

            # --- Pro Logic: if-elif-else for special conditions ---
            # Handle chest logic based on inventory
            if node.id == "open_chest":
                if "key" in self.inventory:
                    print("But you have the key!")
                    self.current_id = "open_chest_with_key"
                    continue
                else:
                    # No key - ending
                    print(f"\n{node.ending_message}")
                    print("Game Over!")
                    break

            if node.id == "take_key" and "key" not in self.inventory:
                self.inventory.append("key")
                print(">> Added key to inventory!")

            # Check if ending node
            if node.is_ending:
                print(f"\n{node.ending_message}")
                print("Game Over!")
                break

            # Show options - if-else loop for menu
            if node.options:
                for i, opt in enumerate(node.options, 1):
                    print(f"{i}. {opt.label}")

                # Input validation loop
                while True:
                    raw = input("\nEnter your choice (number) or 'menu': ").strip().lower()

                    if raw == "menu":
                        # if-elif-else menu as you wanted
                        print("\n--- MENU ---")
                        print("1. Continue")
                        print("2. Show inventory & history")
                        print("3. Save game")
                        print("4. Quit")
                        m = input("Choice: ").strip()
                        if m == "1":
                            break  # back to game loop
                        elif m == "2":
                            print(f"Inventory: {self.inventory}")
                            print(f"Path: {' -> '.join(self.history[-5:])}")
                        elif m == "3":
                            self.save_game()
                        elif m == "4":
                            print("Goodbye!")
                            return
                        else:
                            print("Invalid menu choice.")
                        continue

                    try:
                        choice_idx = int(raw) - 1
                        if 0 <= choice_idx < len(node.options):
                            self.history.append(self.current_id)
                            self.current_id = node.options[choice_idx].next_id
                            break
                        else:
                            print(f"Invalid. Enter 1-{len(node.options)}")
                    except ValueError:
                        print("Invalid input. Enter a number or 'menu'.")
            else:
                print("No options left.")
                break

if __name__ == "__main__":
    game = AdventureEnginePro()
    game.play()
