# vault_of_genesis.py - Branching Narrative Engine
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

try:
    from google.cloud import dialogflow_v2 as dialogflow
    DIALOGFLOW_AVAILABLE = True
except ImportError:
    DIALOGFLOW_AVAILABLE = False

class Node(Enum):
    ARRIVAL = "arrival"
    WARNING_FIGHT = "warning_fight"
    RUINS = "ruins"
    ACTIVATE = "activate"
    STUDY = "study"

@dataclass
class Player:
    name: str = "Explorer"
    hp: int = 100
    inventory: list = field(default_factory=list)
    flags: Dict[str, bool] = field(default_factory=dict)

class GenesisEngine:
    def __init__(self, project_id="your-project-id"):
        self.project_id = project_id
        self.session = f"session-{random.randint(1000,9999)}"
        self.player = Player()

    def ai_oracle(self, text: str) -> str:
        if not DIALOGFLOW_AVAILABLE:
            return random.choice([
                "The guardian's voice echoes: 'Your choice ripples across time...'",
                "'You were warned, child of Earth.'",
                "'The Core judges you.'"
            ])
        try:
            client = dialogflow.SessionsClient()
            session = client.session_path(self.project_id, self.session)
            text_input = dialogflow.TextInput(text=text, language_code="en-US")
            query = dialogflow.QueryInput(text=text_input)
            res = client.detect_intent(session=session, query_input=query)
            return res.query_result.fulfillment_text
        except Exception as e:
            return f"[Oracle Offline] {e}"

    def choice(self, q: str, options: dict) -> str:
        print(f"\n{q}")
        for k, v in options.items(): print(f" {k.upper()}) {v}")
        while True:
            c = input("> ").lower().strip()
            if c in options: return c
            print(f"Choose: {', '.join(options.keys())}")

    def run(self):
        print("\n=== VAULT OF GENESIS ===")
        self.player.name = input("Enter callsign: ") or "Explorer"

        # Chapter 1
        print("\nYou drop from orbit onto a dead world. A monolith pulses.")
        c = self.choice("The Guardian warns you to leave.", {"a": "Heed warning and leave", "b": "Ignore and enter vault"})

        if c == "a":
            print("\nScavengers warp in!")
            c2 = self.choice("They want the planet.", {"a": "Fight", "b": "Flee"})
            outcome = "You fought bravely. Planet secured." if c2 == "a" else "You fled. The planet is lost, but you live."
            print(self.ai_oracle(f"I chose to {outcome}"))
            print(f"\nENDING: {'Defender' if c2=='a' else 'Survivor'}")
            return

        # Ruins path
        print("\nInside: Zero-g ruins. A Genesis Core floats.")
        self.player.inventory.append("Core Key")
        c = self.choice("The Core is unstable.", {"a": "Activate now", "b": "Study first"})

        if c == "a":
            print("\nYou ACTIVATE! Light consumes you. You become a god... or a beacon for predators.")
            print(self.ai_oracle("I activated the Genesis Core"))
            print("ENDING: Catalyst")
        else:
            print("\nYou STUDY. You learn it can create worlds, but each creation costs a memory.")
            print(self.ai_oracle("I studied the device and chose to hide it"))
            print("ENDING: Keeper of Secrets")

if __name__ == "__main__":
    GenesisEngine().run()