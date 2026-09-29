"""app.py - FastAPI for password generator"""
from fastapi import FastAPI
from password_engine import ExtremePasswordAI
from strength_analyzer import StrengthAnalyzer

app = FastAPI(title="Extreme Password AI")
engine = ExtremePasswordAI()
analyzer = StrengthAnalyzer()
engine.train(["P@ssw0rd!", "S3cur1ty!", "Str0ngP@ss!"])

@app.get("/")
def home():
    return {"status": "Extreme Password AI Online", "endpoints": ["/generate/secure", "/generate/memorable", "/check/{password}"]}

@app.get("/generate/secure")
def gen_secure(length: int = 12):
    return {"password": engine.generate_secure(length), "type": "secure"}

@app.get("/generate/memorable")
def gen_memorable(words: int = 4):
    return {"password": engine.generate_memorable(words=words), "type": "memorable"}

@app.get("/generate/extreme")
def gen_extreme(length: int = 16):
    return {"password": engine.generate_extreme(length), "type": "extreme"}

@app.get("/check/{password}")
def check(password: str):
    return analyzer.check_strength(password)

# Run: uvicorn app:app --reload
