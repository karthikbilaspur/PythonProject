# chronicle_weaver.py - The Memory Weaver
import json, random, torch
from pathlib import Path
from datetime import datetime
from transformers import T5ForConditionalGeneration, T5Tokenizer

CONFIG = {
    "model": "t5-base",
    "profile_db": "chronicle_db.json",
    "max_history_chars": 2000
}

class ChronicleWeaver:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[*] Loading {CONFIG['model']} on {self.device}...")
        self.tokenizer = T5Tokenizer.from_pretrained(CONFIG['model'])
        self.model = T5ForConditionalGeneration.from_pretrained(CONFIG['model']).to(self.device)
        self.db = self._load_db()
        self.genres = ["adventure", "romance", "sci-fi", "fantasy", "mystery", "noir", "cyberpunk", "epic", "horror", "cozy"]

    def _load_db(self):
        path = Path(CONFIG['profile_db'])
        return json.loads(path.read_text()) if path.exists() else {}

    def _save_db(self):
        Path(CONFIG['profile_db']).write_text(json.dumps(self.db, indent=2))

    def generate(self, prompt: str, history: str = "", max_len: int = 400) -> str:
        context = f"write a compelling story: {history[-800:]} \n new prompt: {prompt}" if history else f"write a compelling story: {prompt}"
        ids = self.tokenizer.encode(context, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        out = self.model.generate(
            ids, max_length=max_len, do_sample=True,
            temperature=0.88, top_p=0.92, top_k=60,
            repetition_penalty=1.18, no_repeat_ngram_size=3
        )
        return self.tokenizer.decode(out[0], skip_special_tokens=True)

# --- CLI ---
def main():
    engine = ChronicleWeaver()
    name = input("Enter your writer name: ").strip() or "Anon"
    if name not in engine.db:
        engine.db[name] = {"joined": str(datetime.now()), "stories": [], "stats": {}}

    history_buffer = ""
    print(f"\nWelcome {name}. Commands: random | profile | export | quit")

    while True:
        cmd = input("\n> Prompt (or command): ").strip()
        if not cmd: continue
        if cmd == "quit": break
        if cmd == "profile":
            stories = engine.db[name]['stories']
            print(f"Stories: {len(stories)} | Avg Rating: {sum(s['rating'] for s in stories if s['rating'])/len(stories) if stories else 0:.1f}")
            for s in stories[-3:]: print(f" - [{s['rating']}/5] {s['prompt'][:40]}...")
            continue
        if cmd == "export":
            Path(f"{name}_chronicles.md").write_text("\n\n".join([f"## {s['prompt']}\n{s['text']}" for s in engine.db[name]['stories']]))
            print("Exported to markdown!")
            continue
        if cmd.lower() == "random":
            cmd = random.choice(engine.genres)
            print(f"Genre roll: {cmd}")

        story = engine.generate(cmd, history_buffer)
        history_buffer = (history_buffer + " " + story)[-CONFIG['max_history_chars']:]
        print(f"\n---\n{story}\n---")

        if input("Continue? (y/n): ").lower() == 'y':
            direction = input("Direction: ")
            story2 = engine.generate(direction, history_buffer)
            print(f"\n{story2}")
            history_buffer += " " + story2
            story += "\n\n" + story2

        rating = input("Rate 1-5 (skip to ignore): ").strip()
        if rating in "12345":
            engine.db[name]['stories'].append({"prompt": cmd, "text": story, "rating": int(rating), "date": str(datetime.now())})
            engine._save_db()

if __name__ == "__main__":
    main()