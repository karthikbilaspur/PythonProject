# storyverse_unified.py - The Ultimate Merge
# Combines: 1) chronicle_weaver + 2) vault_of_genesis + 3) echo_scribe
# Features: Profile save, ratings, inventory, branching + freeform, export, memory

import json, random, torch
from pathlib import Path
from datetime import datetime
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict

from transformers import T5ForConditionalGeneration, T5Tokenizer

# --- CONFIG ---
CONFIG = {
    "model_name": "t5-base", # change to "microsoft/Phi-3-mini-4k-instruct" for 10x better stories
    "db_path": "storyverse_db.json",
    "max_history": 2500,
    "export_path": "my_chronicles.md"
}

@dataclass
class Player:
    name: str = "Explorer"
    stories_created: int = 0
    inventory: List[str] = field(default_factory=list)
    flags: Dict[str, bool] = field(default_factory=dict)
    favorite_genre: str = ""

class StoryVerseEngine:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[+] Loading {CONFIG['model_name']} on {self.device}...")
        self.tokenizer = T5Tokenizer.from_pretrained(CONFIG['model_name'])
        self.model = T5ForConditionalGeneration.from_pretrained(CONFIG['model_name']).to(self.device)

        self.db = self._load_db()
        self.memory = deque(maxlen=6) # For Echo Scribe mode
        self.genres = ["adventure", "romance", "sci-fi", "fantasy", "mystery", "horror", "cyberpunk", "mythology", "noir"]
        self.player: Player = None

    def _load_db(self):
        p = Path(CONFIG['db_path'])
        return json.loads(p.read_text()) if p.exists() else {}

    def _save_db(self):
        Path(CONFIG['db_path']).write_text(json.dumps(self.db, indent=2))

    def _generate(self, prompt: str, history: str = "", max_len: int = 380) -> str:
        # Upgraded generation with all controls
        full_prompt = f"write a compelling story: {history[-800:]} {prompt}" if history else f"write a compelling story: {prompt}"
        input_ids = self.tokenizer.encode(full_prompt, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        output = self.model.generate(
            input_ids,
            max_length=max_len,
            do_sample=True,
            temperature=0.9,
            top_p=0.92,
            top_k=60,
            repetition_penalty=1.18,
            no_repeat_ngram_size=3
        )
        story = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return story

    # ================= MODE 1: CHRONICLE WEAVER (Your File 1 Upgraded) =================
    def mode_chronicle_weaver(self):
        print("\n--- MODE 1: CHRONICLE WEAVER (Freeform + Profile) ---")
        history = ""
        while True:
            prompt = input("\n[Weaver] Enter prompt (random/profile/back): ").strip()

            if prompt.lower() == "back":
                break
            elif prompt.lower() == "profile":
                self.show_profile()
                continue
            elif prompt.lower() == "random":
                prompt = random.choice(self.genres)
                print(f" -> Rolled genre: {prompt}")
            elif prompt == "":
                print("Enter a valid prompt.")
                continue

            story = self._generate(prompt, history)
            history = (history + " " + story)[-CONFIG['max_history']:]
            self.memory.append(story)

            print(f"\n{'-'*40}\n{story}\n{'-'*40}")

            # if-else for continuation (as you requested)
            cont = input("Continue this story? (yes/no): ").lower()
            if cont == "yes":
                direction = input("Direction: ")
                if direction:
                    story2 = self._generate(direction, history)
                    print(f"\n{story2}")
                    history += " " + story2
                    story += "\n\n" + story2
            elif cont == "no":
                print("Got it, saving this chronicle...")
            else:
                print("Invalid choice, treating as 'no'.")

            # Rating system with if-elif-else
            rating = input("Rate 1-5 (or skip): ").strip()
            if rating in ["1","2","3","4","5"]:
                self.save_story(prompt, story, int(rating))
                print("Saved with rating!")
            elif rating == "skip" or rating == "":
                self.save_story(prompt, story, 0)
                print("Saved without rating.")
            else:
                print("Invalid rating, not saved.")

    # ================= MODE 2: VAULT OF GENESIS (Your File 2 Upgraded) =================
    def mode_vault_of_genesis(self):
        print("\n--- MODE 2: VAULT OF GENESIS (Branching RPG) ---")
        print("You arrive at a dead planet. A monolith pulses.")

        # if-elif-else loop for choices
        choice = input("\nDo you (A) Heed warning and leave or (B) Enter vault? > ").lower()

        if choice == "a":
            print("\nYou leave. Hostile scavengers appear!")
            choice2 = input("Do you (A) Fight or (B) Flee? > ").lower()
            if choice2 == "a":
                print("\nENDING: Defender - You win, but the planet is scarred.")
                self.player.inventory.append("Alien Tech")
            elif choice2 == "b":
                print("\nENDING: Survivor - You live to explore another day.")
            else:
                print("\nInvalid choice. You freeze and are captured. ENDING: Prisoner")

        elif choice == "b":
            print("\nYou enter. You find the Genesis Core - a device that rewrites reality.")
            self.player.inventory.append("Genesis Core Access")

            choice2 = input("Do you (A) Activate it or (B) Study it or (C) Use freeform prompt? > ").lower()

            if choice2 == "a":
                story = self._generate("I activated the ancient Genesis Core and became a god")
                print(f"\n{story}\nENDING: Catalyst")
            elif choice2 == "b":
                story = self._generate("I studied the Genesis Core and decided to hide its power forever")
                print(f"\n{story}\nENDING: Keeper")
            elif choice2 == "c":
                custom = input("What do you do with the Core? > ")
                story = self._generate(custom, history="Inside the vault with the Genesis Core")
                print(f"\n{story}\nENDING: Custom - {custom[:30]}")
            else:
                print("Invalid. The Core overloads while you hesitate. ENDING: Void")

        else:
            print("Invalid choice. The Guardian ejects you from the planet.")

    # ================= MODE 3: ECHO SCRIBE (Your File 3 Upgraded) =================
    def mode_echo_scribe(self):
        print("\n--- MODE 3: ECHO SCRIBE (Infinite Loop) ---")
        print("Type 'reset' to clear memory, 'history' to see memory, 'back' to exit")
        while True:
            prompt = input("\n[Echo] > ").strip()
            if prompt == "back":
                break
            elif prompt == "reset":
                self.memory.clear()
                print("Memory cleared.")
                continue
            elif prompt == "history":
                print("\n".join(list(self.memory)[-3:]) if self.memory else "No history yet.")
                continue
            elif prompt == "":
                continue

            story = self._generate(prompt, history=" ".join(self.memory))
            self.memory.append(story)
            print(f"\n{story}")

    # ================= MODE 4: HYBRID (NEW - Best of all 3) =================
    def mode_hybrid(self):
        print("\n--- MODE 4: HYBRID (Freeform + Auto Choices) ---")
        history = ""
        while True:
            prompt = input("\n[Hybrid] What do you do? (or 'back'): ").strip()
            if prompt == "back": break
            if not prompt: continue

            story = self._generate(prompt, history)
            history = (history + " " + story)[-CONFIG['max_history']:]
            print(f"\n{story}")

            # AI generates choices for you - if loop
            print("\nWhat next?")
            print(" A) Continue bravely")
            print(" B) Investigate closer")
            print(" C) Freeform action")
            print(" D) End story")

            next_step = input("Choose A/B/C/D: ").lower()

            if next_step == "a":
                story = self._generate("Continue bravely forward", history)
                print(story)
                history += " " + story
            elif next_step == "b":
                story = self._generate("Investigate closer with caution", history)
                print(story)
                history += " " + story
            elif next_step == "c":
                custom = input("Your custom action: ")
                story = self._generate(custom, history)
                print(story)
                history += " " + story
            elif next_step == "d":
                self.save_story(prompt, history, 5)
                print("Story ended and saved!")
                break
            else:
                print("Invalid choice, ending chapter.")

    def save_story(self, prompt, text, rating):
        if self.player.name not in self.db:
            self.db[self.player.name] = {"stories": []}
        self.db[self.player.name]["stories"].append({
            "prompt": prompt, "text": text, "rating": rating, "date": str(datetime.now())
        })
        self._save_db()
        self.player.stories_created += 1

    def show_profile(self):
        data = self.db.get(self.player.name, {})
        stories = data.get("stories", [])
        print(f"\n=== PROFILE: {self.player.name} ===")
        print(f"Stories: {len(stories)} | Inventory: {self.player.inventory}")
        for s in stories[-5:]:
            print(f" - [{s['rating']}/5] {s['prompt'][:30]}... ({s['date'][:10]})")

    def export_all(self):
        all_text = ""
        for user, data in self.db.items():
            all_text += f"\n# User: {user}\n"
            for s in data.get("stories", []):
                all_text += f"\n## Prompt: {s['prompt']}\nRating: {s['rating']}\n{s['text']}\n---\n"
        Path(CONFIG['export_path']).write_text(all_text)
        print(f"Exported to {CONFIG['export_path']}")

def main():
    engine = StoryVerseEngine()
    name = input("What's your writer name? ").strip() or "Kai"
    engine.player = Player(name=name)
    if name not in engine.db:
        engine.db[name] = {"stories": []}

    while True:
        print("\n" + "="*50)
        print("STORYVERSE UNIFIED - Choose your mode")
        print("="*50)
        print("1. Chronicle Weaver (Freeform + Ratings)")
        print("2. Vault of Genesis (Branching RPG)")
        print("3. Echo Scribe (Infinite Minimal)")
        print("4. Hybrid Mode (Best of all - Recommended)")
        print("5. View Profile")
        print("6. Export to Markdown")
        print("7. Quit")

        choice = input("\nEnter 1-7: ").strip()

        if choice == "1":
            engine.mode_chronicle_weaver()
        elif choice == "2":
            engine.mode_vault_of_genesis()
        elif choice == "3":
            engine.mode_echo_scribe()
        elif choice == "4":
            engine.mode_hybrid()
        elif choice == "5":
            engine.show_profile()
        elif choice == "6":
            engine.export_all()
        elif choice == "7":
            print(f"\nGoodbye, {engine.player.name}! Stories created: {engine.player.stories_created}")
            break
        else:
            print("Invalid choice! Please enter 1-7.")

if __name__ == "__main__":
    main()