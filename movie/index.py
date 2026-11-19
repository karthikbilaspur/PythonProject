
# pyright: reportMissingTypeStubs=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false
"""
Movie AI Suite - Single File
Combines:
1. Genre Prediction (TF-IDF + LogisticRegression)
2. Movie Recommender (TF-IDF + Cosine Similarity)
3. Sentiment Analysis (TF-IDF + LogisticRegression)
4. Telegram Bot (python-telegram-bot v20 + TMDB/OMDb API ready, no IMDb scraping)
+ Tkinter GUI with 3 tabs

Run:
  python index.py              -> opens Tkinter GUI
  python index.py --telegram    -> starts Telegram bot (needs TELEGRAM_TOKEN)
  python index.py --demo        -> CLI demo

Install:
  pip install pandas numpy nltk scikit-learn python-telegram-bot requests
"""
import os
import argparse
from typing import Any
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

import pandas as pd
import numpy as np

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Setup NLTK ----------
for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]:
    try:
        nltk.download(pkg, quiet=True)
    except Exception:
        pass

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

def preprocess_text(text: str) -> str:
    tokens = word_tokenize(text.lower())
    out = [LEMMATIZER.lemmatize(t) for t in tokens if t.isalpha() and t not in STOP_WORDS]
    return " ".join(out)

# ---------- Sample fallback data (so file runs without CSVs) ----------
SAMPLE_MOVIES = [
    ("The Shawshank Redemption", "Two imprisoned men bond over years finding redemption through hope and friendship", "Drama"),
    ("The Dark Knight", "Batman faces Joker chaos Gotham crime hero villain explosion", "Action"),
    ("Toy Story", "Toys come alive adventure friendship funny kids Woody Buzz", "Animation"),
    ("The Conjuring", "Haunted house ghost demon horror family fear night", "Horror"),
    ("Superbad", "Teenagers funny party high school comedy friends awkward", "Comedy"),
    ("Inception", "Dream thief heist mind bending science fiction subconscious", "Sci-Fi"),
    ("Titanic", "Ship love romance tragedy ocean fate lovers", "Romance"),
    ("John Wick", "Retired hitman revenge action gun fight assassin", "Action"),
    ("Finding Nemo", "Fish father searches ocean adventure family kids funny", "Animation"),
    ("Get Out", "Man visits girlfriend family horror thriller twist secret", "Horror"),
    ("La La Land", "Aspiring actress jazz musician love music dreams Los Angeles", "Romance"),
    ("Interstellar", "Astronauts space time black hole save humanity science", "Sci-Fi"),
    ("The Hangover", "Bachelor party Las Vegas comedy friends forget night funny", "Comedy"),
    ("Forrest Gump", "Man life journey love history heartwarming drama", "Drama"),
]
SAMPLE_REVIEWS = [
    ("This movie is amazing! I loved it.", 1),
    ("Brilliant acting and beautiful story.", 1),
    ("Funny, heartwarming and unforgettable.", 1),
    ("Best film I have ever seen.", 1),
    ("Terrible, boring, waste of time.", 0),
    ("I hated it, awful plot and bad acting.", 0),
    ("Disappointing and slow, I fell asleep.", 0),
    ("Worst movie ever, do not watch.", 0),
]

# ---------- 1. Genre Prediction ----------
class GenrePredictor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = LogisticRegression(max_iter=1000, multi_class="auto")
        self.le = LabelEncoder()
        self.trained = False

    def train(self, df: pd.DataFrame) -> float:
        df = df.copy()
        df["clean"] = df["plot"].astype(str).apply(preprocess_text)
        X = self.vectorizer.fit_transform(df["clean"])
        y = self.le.fit_transform(df["genre"])
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(Xtr, ytr)
        acc = float(accuracy_score(yte, self.model.predict(Xte)))
        print(f"[Genre] Accuracy: {acc:.2f} | Classes: {list(self.le.classes_)}")
        self.trained = True
        return acc

    def predict(self, plot: str):
        if not self.trained:
            raise RuntimeError("Genre model not trained yet")
        clean = preprocess_text(plot)
        vec = self.vectorizer.transform([clean])
        probs = self.model.predict_proba(vec)[0]
        idx = int(np.argmax(probs))
        return self.le.inverse_transform([idx])[0], float(probs[idx])

# ---------- 2. Recommender ----------
class Recommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.movies = None
        self.vectors: Any = None

    def fit(self, movies_df: pd.DataFrame):
        self.movies = movies_df.reset_index(drop=True).copy()
        self.movies["clean"] = self.movies["description"].astype(str).apply(preprocess_text)
        self.vectors = self.vectorizer.fit_transform(self.movies["clean"])
        return self

    def recommend(self, title: str, n: int = 5) -> list[str]:
        if self.movies is None:
            return []
        match = self.movies[self.movies["title"].str.lower() == title.lower()]
        if match.empty:
            # fuzzy fallback: contains
            match = self.movies[self.movies["title"].str.lower().str.contains(title.lower())]
        if match.empty:
            return []
        idx = match.index[0]
        sims = cosine_similarity(self.vectors[idx:idx + 1], self.vectors).flatten()
        sims[idx] = -1
        top = sims.argsort()[-n:][::-1]
        return self.movies.iloc[top]["title"].tolist()

# ---------- 3. Sentiment Analysis ----------
class SentimentAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = LogisticRegression(max_iter=1000)
        self.trained = False

    def train(self, df: pd.DataFrame) -> None:
        df = df.copy()
        df["clean"] = df["review"].astype(str).apply(preprocess_text)
        X = self.vectorizer.fit_transform(df["clean"])
        y = df["sentiment"].values
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=9)
        self.model.fit(Xtr, ytr)
        print(f"[Sentiment] Accuracy: {accuracy_score(yte, self.model.predict(Xte)):.2f}")
        print(classification_report(yte, self.model.predict(Xte)))
        self.trained = True

    def predict(self, review: str):
        clean = preprocess_text(review)
        vec = self.vectorizer.transform([clean])
        pred = int(self.model.predict(vec)[0])
        prob = float(np.max(self.model.predict_proba(vec)[0])) if hasattr(self.model, "predict_proba") else 1.0
        return ("Positive" if pred == 1 else "Negative"), prob

# ---------- Data Loading ----------
def load_movies():
    # Try real CSVs, else fallback to sample
    if os.path.exists("movie_plots.csv"):
        df = pd.read_csv("movie_plots.csv")
        movies = pd.DataFrame({"title": df.get("title", range(len(df))), "description": df["plot"], "genre": df["genre"]})
        return movies
    return pd.DataFrame(SAMPLE_MOVIES, columns=["title", "description", "genre"])

def load_reviews():
    if os.path.exists("IMDB Dataset.csv"):
        df = pd.read_csv("IMDB Dataset.csv")
        df["sentiment"] = df["sentiment"].map({"positive": 1, "negative": 0})
        return df[["review", "sentiment"]].dropna().sample(min(5000, len(df)), random_state=42)
    return pd.DataFrame(SAMPLE_REVIEWS, columns=["review", "sentiment"])

# ---------- Global models ----------
genre_model = GenrePredictor()
recommender = Recommender()
sentiment_model = SentimentAnalyzer()

def train_all():
    movies = load_movies()
    reviews = load_reviews()
    genre_df = pd.DataFrame({"plot": movies["description"], "genre": movies["genre"]})
    genre_model.train(genre_df)
    recommender.fit(movies[["title", "description"]])
    sentiment_model.train(reviews)
    return movies

# ---------- 4. Telegram Bot (v20, async, no scraping) ----------
async def start_telegram():
    try:
        from telegram import Update
        from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
    except ImportError:
        print("Install: pip install python-telegram-bot")
        return
    token = os.getenv("TELEGRAM_TOKEN") or os.getenv("API_KEY")
    if not token:
        print("Set TELEGRAM_TOKEN env var to run bot.")
        return

    async def reply(update: Update, text: str) -> None:
        message = update.effective_message
        if message is not None:
            await message.reply_text(text)

    async def start(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
        await reply(update,
            "Movie AI Bot\n\n/name <plot> - predict genre from plot\n/recommend <movie> - get similar movies\n/sentiment <review> - positive / negative\n/genres - list genres"
        )
    async def name_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        plot = " ".join(ctx.args or [])
        if not plot:
            await reply(update, "Usage: /name A man escapes prison...")
            return
        g, conf = genre_model.predict(plot)
        await reply(update, f"Predicted Genre: {g}\nConfidence: {conf*100:.1f}%")
    async def recommend_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        title = " ".join(ctx.args or [])
        recs = recommender.recommend(title, 5)
        await reply(update, "Recommendations:\n" + ("\n".join(recs) if recs else "No movie found"))
    async def sentiment_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        review = " ".join(ctx.args or [])
        s, p = sentiment_model.predict(review)
        await reply(update, f"Sentiment: {s} ({p*100:.1f}%)")
    async def genres_cmd(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
        await reply(update, ", ".join(genre_model.le.classes_))

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("name", name_cmd))
    app.add_handler(CommandHandler("recommend", recommend_cmd))
    app.add_handler(CommandHandler("sentiment", sentiment_cmd))
    app.add_handler(CommandHandler("genres", genres_cmd))
    print("Telegram bot running...")
    app.run_polling()

# ---------- Tkinter GUI ----------
def launch_gui():
    train_all()
    window = tk.Tk()
    window.title("Movie AI Suite - Genre | Recommender | Sentiment")
    window.geometry("620x560")
    tabs = ttk.Notebook(window)
    tabs.pack(fill="both", expand=True, padx=10, pady=10)

    # Tab 1 - Genre
    t1 = ttk.Frame(tabs); tabs.add(t1, text="Genre Prediction")
    tk.Label(t1, text="Enter movie plot:").pack(pady=(10,0), anchor="w", padx=10)
    plot_box = scrolledtext.ScrolledText(t1, height=8, width=70); plot_box.pack(padx=10, pady=5)
    res1 = tk.Label(t1, text="", font=("Arial", 12, "bold")); res1.pack(pady=5)
    def do_genre():
        plot = plot_box.get("1.0", tk.END).strip()
        if not plot:
            messagebox.showerror("Error", "Please enter a movie plot."); return
        g, conf = genre_model.predict(plot)
        res1.config(text=f"Predicted genre: {g}  |  Confidence: {conf*100:.2f}%")
    ttk.Button(t1, text="Predict Genre", command=do_genre).pack(pady=5)
    ttk.Button(t1, text="Clear", command=lambda: [plot_box.delete("1.0", tk.END), res1.config(text="")]).pack()

    # Tab 2 - Recommender
    t2 = ttk.Frame(tabs); tabs.add(t2, text="Recommender")
    tk.Label(t2, text="Movie title:").pack(pady=(10,0), anchor="w", padx=10)
    title_entry = ttk.Entry(t2, width=60); title_entry.pack(padx=10, pady=5)
    title_entry.insert(0, "The Shawshank Redemption")
    res2 = tk.Text(t2, height=10, width=70); res2.pack(padx=10, pady=5)
    def do_rec():
        recs = recommender.recommend(title_entry.get().strip(), 5)
        res2.delete("1.0", tk.END)
        res2.insert(tk.END, "\n".join(recs) if recs else "No movie found. Try exact title from dataset.")
    ttk.Button(t2, text="Get Recommendations", command=do_rec).pack(pady=5)

    # Tab 3 - Sentiment
    t3 = ttk.Frame(tabs); tabs.add(t3, text="Sentiment")
    tk.Label(t3, text="Enter review:").pack(pady=(10,0), anchor="w", padx=10)
    rev_box = scrolledtext.ScrolledText(t3, height=8, width=70); rev_box.pack(padx=10, pady=5)
    res3 = tk.Label(t3, text="", font=("Arial", 12, "bold")); res3.pack(pady=5)
    def do_sent():
        r = rev_box.get("1.0", tk.END).strip()
        if not r:
            messagebox.showerror("Error", "Please enter a review."); return
        s, p = sentiment_model.predict(r)
        res3.config(text=f"Sentiment: {s}  |  Confidence: {p*100:.2f}%")
    ttk.Button(t3, text="Analyze Sentiment", command=do_sent).pack(pady=5)

    window.mainloop()

# ---------- CLI ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--telegram", action="store_true", help="Run Telegram bot")
    parser.add_argument("--demo", action="store_true", help="CLI demo")
    args = parser.parse_args()

    if args.telegram:
        train_all()
        import asyncio
        asyncio.run(start_telegram())
    elif args.demo:
        movies = train_all()
        print("\n--- Genre ---", genre_model.predict("A haunted house ghost demon family fear night"))
        print("--- Recommend ---", recommender.recommend("The Shawshank Redemption", 5))
        print("--- Sentiment ---", sentiment_model.predict("This movie is amazing! I loved it."))
    else:
        launch_gui()
