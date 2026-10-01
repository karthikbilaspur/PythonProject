
from fastapi import FastAPI
from word_engine import WordEngine
from brain import AIBrain
import uvicorn

app = FastAPI(title="AI Assistant Extreme API")
engine = WordEngine()
brain = AIBrain()

@app.get("/")
def home():
    return {"status": "AI Assistant Extreme Online", "total_words": sum(len(v) for v in engine.data.values()), "level": brain.get_user_level(), "xp": brain.get_xp()}

@app.get("/random")
def random_word(category: str = None):
    return engine.generate_random_word(category)

@app.get("/search/{word}")
def search(word: str):
    return engine.search_word(word) or {"error": "not found"}

# Run with: uvicorn app:app --reload
