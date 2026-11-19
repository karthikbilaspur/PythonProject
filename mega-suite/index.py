

import os, re, argparse, difflib, json
from dataclasses import dataclass, field
from typing import Any, cast
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split  # pyright: ignore[reportUnknownVariableType]
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score, classification_report  # pyright: ignore[reportUnknownVariableType]
from sklearn.metrics.pairwise import cosine_similarity  # pyright: ignore[reportUnknownVariableType]
import joblib  # pyright: ignore[reportMissingTypeStubs]

# ---------- 1. Preprocessing (no NLTK) ----------
STOP = set("a an the and or of to in on for with is are was were be been it its this that these those i you he she we they".split())
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = [t for t in text.split() if t not in STOP and len(t) > 2]
    # simple negation handling: not_good -> not_good
    out: list[str] = []
    for i,t in enumerate(tokens):
        if i>0 and tokens[i-1] in ("not","no","never"): out.append("not_"+t)
        else: out.append(t)
    return " ".join(out)

# ---------- 2. Expanded Sample Data (30 movies, multi-genre) ----------
SAMPLE = [
 ("The Shawshank Redemption","Two imprisoned men bond over years finding redemption through hope and friendship", ["Drama"]),
 ("The Dark Knight","Batman faces Joker chaos Gotham crime hero villain explosion", ["Action","Crime","Drama"]),
 ("Toy Story","Toys come alive adventure friendship funny kids Woody Buzz", ["Animation","Comedy","Family"]),
 ("The Conjuring","Haunted house ghost demon horror family fear night", ["Horror","Thriller"]),
 ("Superbad","Teenagers funny party high school comedy friends awkward", ["Comedy"]),
 ("Inception","Dream thief heist mind bending science fiction subconscious", ["Sci-Fi","Action","Thriller"]),
 ("Titanic","Ship love romance tragedy ocean fate lovers", ["Romance","Drama"]),
 ("John Wick","Retired hitman revenge action gun fight assassin", ["Action","Thriller"]),
 ("Finding Nemo","Fish father searches ocean adventure family kids funny", ["Animation","Family","Adventure"]),
 ("Get Out","Man visits girlfriend family horror thriller twist secret", ["Horror","Thriller","Mystery"]),
 ("La La Land","Aspiring actress jazz musician love music dreams Los Angeles", ["Romance","Drama","Music"]),
 ("Interstellar","Astronauts space time black hole save humanity science", ["Sci-Fi","Drama","Adventure"]),
 ("The Hangover","Bachelor party Las Vegas comedy friends forget night funny", ["Comedy"]),
 ("Forrest Gump","Man life journey love history heartwarming drama", ["Drama","Romance"]),
 ("Parasite","Poor family infiltrates rich household dark comedy thriller class", ["Thriller","Drama","Comedy"]),
 ("Avengers Endgame","Superheroes time travel battle Thanos save universe action", ["Action","Sci-Fi","Adventure"]),
 ("Joker","Failed comedian mental illness Gotham crime dark drama", ["Drama","Crime","Thriller"]),
 ("Coco","Boy music family death Mexican culture adventure animated", ["Animation","Family","Music"]),
 ("Dune","Desert planet spice prophecy war sci-fi epic", ["Sci-Fi","Adventure"]),
 ("3 Idiots","College friends engineering pressure comedy drama India friendship", ["Comedy","Drama"]),
 ("KGF Chapter 2","Rocky gangster gold mines action revenge Karnataka", ["Action","Crime"]),
 ("Pushpa","Smuggler red sandalwood action mass dialogue Andhra", ["Action","Drama"]),
 ("RRR","Freedom fighters British colonial action friendship epic India", ["Action","Drama"]),
 ("Kantara","Village deity forest conflict folklore thriller Karnataka", ["Thriller","Drama","Action"]),
 ("Jawan","Soldier vigilante corruption action Shah Rukh Khan mass", ["Action","Thriller"]),
 ("Spider-Man No Way Home","Peter Parker multiverse villains Marvel action", ["Action","Adventure","Sci-Fi"]),
 ("Oppenheimer","Physicist atomic bomb war history drama Nolan", ["Drama","History","Thriller"]),
 ("Barbie","Barbie real world pink comedy satire adventure", ["Comedy","Adventure","Fantasy"]),
 ("The Batman","Detective Batman Riddler Gotham dark crime", ["Action","Crime","Mystery"]),
 ("Inside Out 2","Teen emotions anxiety joy sadness animated Pixar", ["Animation","Family","Comedy"]),
]
SAMPLE_REVIEWS = [
 ("This movie is amazing! I loved it.", "positive"),("Brilliant acting and beautiful story.", "positive"),
 ("Funny, heartwarming and unforgettable.", "positive"),("Best film I have ever seen.", "positive"),
 ("Terrible, boring, waste of time.", "negative"),("I hated it, awful plot and bad acting.", "negative"),
 ("Disappointing and slow, I fell asleep.", "negative"),("Worst movie ever, do not watch.", "negative"),
 ("It was okay, not great not bad.", "neutral"),("Some parts good, some boring.", "neutral"),
 ("Not bad, but not amazing either.", "neutral"),("Average movie, watchable once.", "neutral"),
]

@dataclass
class MovieAISuite:
    # These third-party APIs have incomplete generic typing; keep their dynamic
    # return values at an explicit boundary rather than letting Unknown spread.
    genre_vec: Any = field(default_factory=lambda: TfidfVectorizer(max_features=8000, ngram_range=(1,2)))
    genre_model: Any = field(default_factory=lambda: LogisticRegression(max_iter=1000, C=5))
    mlb: Any = field(default_factory=MultiLabelBinarizer)
    sent_vec: Any = field(default_factory=lambda: TfidfVectorizer(max_features=8000, ngram_range=(1,2), analyzer="word"))
    sent_model: Any = field(default_factory=lambda: LogisticRegression(max_iter=1000, C=5))
    rec_vec: Any = field(default_factory=lambda: TfidfVectorizer(max_features=5000, ngram_range=(1,2)))
    movies: Any = field(default_factory=pd.DataFrame)
    rec_matrix: Any = None
    trained: bool = False

    def load_movies(self):
        # Try TMDB / Kaggle files if present, else SAMPLE
        if os.path.exists("tmdb_5000_movies.csv"):
            df = pd.read_csv("tmdb_5000_movies.csv")
            # TMDB genres is JSON-like: [{"id":28,"name":"Action"}]
            def parse_genres(x: object) -> list[str]:
                if not isinstance(x, str):
                    return []
                try:
                    parsed: object = json.loads(x.replace("'", '"'))
                    if not isinstance(parsed, list):
                        return []
                    genres: list[str] = []
                    for genre_value in cast(list[object], parsed):
                        if isinstance(genre_value, dict):
                            genre = cast(dict[str, object], genre_value)
                            name = genre.get("name")
                            if isinstance(name, str):
                                genres.append(name)
                    return genres
                except (json.JSONDecodeError, TypeError, KeyError):
                    return []
            return pd.DataFrame({"title": df["title"], "description": df["overview"].fillna(""), "genres": df["genres"].apply(parse_genres)})
        return pd.DataFrame(SAMPLE, columns=["title","description","genres"])

    def train(self):
        movies: Any = self.load_movies()
        self.movies = movies.reset_index(drop=True)
        # --- Genre (multi-label) ---
        clean: list[str] = movies["description"].apply(clean_text).tolist()
        X = self.genre_vec.fit_transform(clean)
        Y = self.mlb.fit_transform(movies["genres"])
        Xtr: Any
        Xte: Any
        Ytr: Any
        Yte: Any
        Xtr, Xte, Ytr, Yte = train_test_split(  # pyright: ignore[reportUnknownVariableType]
            X, Y, test_size=0.2, random_state=42
        )
        self.genre_model.fit(Xtr,Ytr)
        print(f"[Genre] Exact-match acc: {accuracy_score(Yte, self.genre_model.predict(Xte)):.2f} | Genres: {list(self.mlb.classes_)}")
        # --- Recommender ---
        def boost_genres(value: object) -> str:
            if not isinstance(value, list):
                return ""
            genres = cast(list[object], value)
            return " ".join(str(genre) for genre in genres) * 3

        combined: Any = movies["description"] + " " + movies["genres"].apply(boost_genres)  # genre boost x3
        self.rec_matrix = self.rec_vec.fit_transform(combined.apply(clean_text))
        # --- Sentiment (3-class) ---
        rdf = pd.DataFrame(SAMPLE_REVIEWS, columns=["review","sentiment"])
        if os.path.exists("IMDB Dataset.csv"):
            d = pd.read_csv("IMDB Dataset.csv").sample(min(8000,len(pd.read_csv("IMDB Dataset.csv"))), random_state=42)
            rdf = pd.DataFrame({"review": d["review"], "sentiment": d["sentiment"].map({"positive":"positive","negative":"negative"})})
        Xs = self.sent_vec.fit_transform(rdf["review"].apply(clean_text))
        Xtr: Any
        Xte: Any
        ytr: Any
        yte: Any
        Xtr, Xte, ytr, yte = train_test_split(  # pyright: ignore[reportUnknownVariableType]
            Xs, rdf["sentiment"], test_size=0.2, random_state=9
        )
        self.sent_model.fit(Xtr,ytr)
        print(f"[Sentiment] Acc: {accuracy_score(yte, self.sent_model.predict(Xte)):.2f}")
        sent_report: str = cast(str, classification_report(yte, self.sent_model.predict(Xte), output_dict=False, zero_division=0))
        print(sent_report)
        self.trained=True
        return self

    def predict_genre(self, plot: str, top_k: int = 3) -> list[tuple[str, float]]:
        vec = self.genre_vec.transform([clean_text(plot)])
        probs = self.genre_model.predict_proba(vec)[0] if hasattr(self.genre_model,"predict_proba") else self.genre_model.decision_function(vec)[0]
        # For multilabel LogisticRegression, predict_proba returns per-class; use decision or proba handling
        # Simpler: use predict + top proba via decision_function
        try:
            scores = self.genre_model.decision_function(vec)[0]
        except: scores = probs
        idx = np.argsort(scores)[::-1][:top_k]
        return [(str(self.mlb.classes_[i]), float(1/(1+np.exp(-scores[i])))) for i in idx]

    def recommend(self, title: str, n: int = 5) -> tuple[list[tuple[str, float, list[str]]], str]:
        titles: list[str] = [str(t) for t in self.movies["title"].tolist()]
        # fuzzy match
        close = difflib.get_close_matches(title, titles, n=1, cutoff=0.4)
        if not close:
            # contains search
            cand = [t for t in titles if title.lower() in t.lower()]
            if not cand: return [], f"No match for '{title}'. Try: {', '.join(titles[:5])}"
            close=[cand[0]]
        idx = titles.index(close[0])
        sims: np.ndarray[Any, np.dtype[np.float64]] = np.asarray(
            cast(Any, cosine_similarity(self.rec_matrix[idx:idx+1], self.rec_matrix).flatten()),
            dtype=np.float64,
        )
        sims[idx] = -1
        top = sims.argsort()[-n:][::-1]
        recommendations: list[tuple[str, float, list[str]]] = []
        for movie_index in top:
            movie = self.movies.iloc[int(movie_index)]
            raw_genres: object = cast(object, movie["genres"])
            genres = (
                [genre for genre in cast(list[object], raw_genres) if isinstance(genre, str)]
                if isinstance(raw_genres, list)
                else []
            )
            recommendations.append((str(movie["title"]), float(cast(Any, sims[movie_index])), genres))
        return recommendations, close[0]

    def sentiment(self, review: str) -> tuple[str, float]:
        vec = self.sent_vec.transform([clean_text(review)])
        pred = str(self.sent_model.predict(vec)[0])
        prob = float(np.max(self.sent_model.predict_proba(vec)[0]))
        return pred, prob

    def save(self, path: str = "movie_ai_v2.joblib") -> None:
        cast(Any, joblib).dump(self, path)
        print(f"Saved -> {path}")

    @staticmethod
    def load(path: str = "movie_ai_v2.joblib") -> "MovieAISuite":
        return cast(MovieAISuite, cast(Any, joblib).load(path)) if os.path.exists(path) else MovieAISuite().train()

# ---------- Interfaces ----------
def demo(suite: MovieAISuite) -> None:
    print("\n--- GENRE (Top-3) ---")
    print(suite.predict_genre("A haunted house ghost demon family fear night"))
    print("\n--- RECOMMEND ---")
    recs, matched = suite.recommend("KGF")
    print(f"Matched: {matched}"); [print(r) for r in recs]
    print("\n--- SENTIMENT ---")
    print(suite.sentiment("This movie is amazing! I loved it."))
    print(suite.sentiment("It was okay, not great not bad."))

def run_api(suite: MovieAISuite) -> None:
    from fastapi import FastAPI
    import uvicorn
    app = FastAPI(title="Movie AI Suite v2")
    @app.get("/genre") 
    def genre(plot: str) -> dict[str, list[tuple[str, float]]]: return {"top3": suite.predict_genre(plot)}
    @app.get("/recommend")
    def rec(title: str, n: int=5) -> dict[str, object]:
        r,m = suite.recommend(title,n); return {"matched": m, "recommendations": r}
    @app.get("/sentiment")
    def sent(review: str) -> dict[str, str | float]: s,p = suite.sentiment(review); return {"sentiment": s, "confidence": p}
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_gui(suite: MovieAISuite) -> None:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    win = tk.Tk(); win.title("Movie AI Suite v2"); win.geometry("680x620")
    tabs = ttk.Notebook(win); tabs.pack(fill="both", expand=True, padx=10, pady=10)
    # Genre tab
    t1=ttk.Frame(tabs); tabs.add(t1, text="Genre (Top-3)")
    plot_box=scrolledtext.ScrolledText(t1,height=8,width=75); plot_box.pack(padx=10,pady=10)
    res1=tk.Label(t1,text="",font=("Arial",11,"bold"), justify="left"); res1.pack()
    def do_g():
        if not plot_box.get("1.0",tk.END).strip(): return messagebox.showerror("Error","Enter plot")
        res1.config(text="\n".join([f"{g} - {c*100:.1f}%" for g,c in suite.predict_genre(plot_box.get("1.0",tk.END))]))
    ttk.Button(t1,text="Predict Top-3 Genres",command=do_g).pack(pady=5)
    # Rec tab
    t2=ttk.Frame(tabs); tabs.add(t2,text="Recommender")
    e=ttk.Entry(t2,width=60); e.pack(padx=10,pady=10); e.insert(0,"KGF")
    res2=tk.Text(t2,height=12,width=75); res2.pack(padx=10)
    def do_r():
        recs,m=suite.recommend(e.get().strip(),5); res2.delete("1.0",tk.END); res2.insert(tk.END,f"Matched: {m}\n\n"+"\n".join([f"{t} ({s*100:.0f}% similar) - {', '.join(g)}" for t,s,g in recs]))
    ttk.Button(t2,text="Get Recommendations",command=do_r).pack(pady=5)
    # Sentiment tab
    t3=ttk.Frame(tabs); tabs.add(t3,text="Sentiment")
    rev=scrolledtext.ScrolledText(t3,height=8,width=75); rev.pack(padx=10,pady=10)
    res3=tk.Label(t3,text="",font=("Arial",12,"bold")); res3.pack()
    def do_s():
        s,p=suite.sentiment(rev.get("1.0",tk.END)); res3.config(text=f"{s.capitalize()}  |  {p*100:.1f}%")
    ttk.Button(t3,text="Analyze",command=do_s).pack(pady=5)
    win.mainloop()

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--demo",action="store_true"); ap.add_argument("--api",action="store_true"); ap.add_argument("--gui",action="store_true")
    args=ap.parse_args()
    suite = MovieAISuite.load() if os.path.exists("movie_ai_v2.joblib") else MovieAISuite().train()
    if args.api: run_api(suite)
    elif args.gui: run_gui(suite)
    else: demo(suite)
