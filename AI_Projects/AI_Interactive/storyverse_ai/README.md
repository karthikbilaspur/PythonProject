StoryVerse - Interactive AI Story Engine
A collection of 4 AI-powered interactive story generators built with Hugging Face Transformers. Merges freeform storytelling, branching RPG mechanics, and minimalist infinite loops into one unified universe.

📦 Files Overview
File	Original	Type	Best For
chronicle_weaver.py	File 1 Upgraded	Freeform + Profile System	Writers who want memory, ratings & exports
vault_of_genesis.py	File 2 Upgraded	Branching RPG Adventure	Gamers who want A/B choices & endings
echo_scribe.py	File 3 Upgraded	Minimalist Infinite Loop	Quick ideation & distraction-free writing
storyverse_unified.py	Merge of All 3	Ultimate Edition	Everyone - Recommended starting point
1. chronicle_weaver.py - The Memory Weaver
Your File 1, upgraded from a simple menu.

What it does:

Generates stories with T5 (or any LLM) with proper sampling temperature=0.88, top_p=0.92
Remembers story history (last 2000 chars) so "continue" actually continues
User profiles saved to chronicle_db.json
Rating system (1-5) that learns your taste
Commands: random, profile, export, quit
Auto-exports to Markdown my_chronicles.md
Upgrades from original:

Model loads ONCE, not every generation
Fixed crash on empty input
No more story[:20] truncation bug
Persistent JSON DB
2. vault_of_genesis.py - Branching Narrative Engine
Your File 2, upgraded from Dialogflow adventure.

What it does:

State-machine based RPG, not recursive calls (no more RecursionError)
Player class with hp, inventory, flags
3 distinct endings: Defender, Survivor, Catalyst, Keeper
Integrated AI Oracle (works with or without Dialogflow API)
Upgrades from original:

Replaced deprecated import dialogflow with google.cloud.dialogflow_v2
Added choice() helper with validation loop instead of recursion
Added if-elif-else branching for A/B/C choices as you requested
Inventory system: Genesis Core Access, Alien Tech
3. echo_scribe.py - Minimalist Infinite Story
Your File 3, upgraded from simple loop.

What it does:

Ultra-minimal: just prompt -> story -> prompt
Uses collections.deque(maxlen=5) for smart memory
Commands: reset to clear memory, history to view last 3 chunks, quit
Upgrades from original:

Memory doesn't explode (old version kept infinite history)
Proper device detection cuda / cpu
truncation=True to prevent token overflow
4. storyverse_unified.py - The Ultimate Merge [RECOMMENDED]
Merge of all 3 + all enhancements you asked for.

Modes:

1. Chronicle Weaver (Freeform + Ratings)
2. Vault of Genesis (Branching RPG)
3. Echo Scribe (Infinite Minimal)
4. Hybrid Mode (Best of all - Freeform + Auto A/B/C/D)
5. View Profile
6. Export to Markdown
7. Quit
Hybrid Mode Logic (uses if-elif-else as requested):

python
if next_step == "a": continue bravely
elif next_step == "b": investigate closer
elif next_step == "c": freeform custom action
elif next_step == "d": end and save
else: invalid choice
All upgrades included:

GPU auto-detect
JSON persistence storyverse_db.json
Rating system with if-elif-else
while True loops for infinite play
Export to my_chronicles.md
Player stats & inventory
No recursion bugs
🚀 Installation
bash
# Clone or download the 4 files
pip install torch transformers

# Optional - for much better stories (recommended)
pip install accelerate
# Then change model_name in CONFIG to:
# "microsoft/Phi-3-mini-4k-instruct" or "mistralai/Mistral-7B-Instruct-v0.2"

# For Dialogflow mode in vault_of_genesis.py
pip install google-cloud-dialogflow
▶️ Usage
bash
# Run any file individually
python chronicle_weaver.py
python vault_of_genesis.py
python echo_scribe.py

# Or run the ultimate merged version
python storyverse_unified.py
First run example:

What's your writer name? Kai
==================================================
STORYVERSE UNIFIED - Choose your mode
==================================================
1. Chronicle Weaver...
...
Enter 1-7: 4

[Hybrid] What do you do? (or 'back'): I enter the vault and touch the glowing core
🛠️ How It Works
User Prompt -> Tokenizer (T5) -> Model.generate(
    temperature=0.9,
    top_p=0.92,
    top_k=60,
    repetition_penalty=1.18
) -> Story Text -> Saved to memory + JSON
All files use the same core _generate() method upgraded from your original:

python
# Old:
output = model.generate(input_ids, max_length=200)

# New:
output = model.generate(
    input_ids, max_length=380, do_sample=True,
    temperature=0.9, top_p=0.92, repetition_penalty=1.18,
    no_repeat_ngram_size=3
)
🔮 Next Steps / Roadmap
 Swap t5-base to Phi-3 or Llama 3 via API for 10x quality
 Add Gradio UI: gr.Interface(fn=engine._generate, inputs="text", outputs="text").launch()
 Add Vector DB (ChromaDB) for long-term memory retrieval
 Add TTS + Stable Diffusion for illustrated stories
 Turn storyverse_unified.py into Discord / Telegram bot
📄 Data Files Created
After running, you will see:

chronicle_db.json / storyverse_db.json - Your profiles & rated stories
my_chronicles.md - Exported markdown book
📝 License
MIT - Use freely for your portfolio, game, or product.
