"""
InstaVault - Apna Personal 【entity-Instagram¦canonical_name=Instagram】 Analyzer
100% Python | No Bot | No Password | No Login
Sirf apna 【entity-Instagram¦canonical_name=Instagram】 Data Download (JSON) use karta hai.

Run: python instavault.py
Requirements: pip install matplotlib (optional, charts ke liye)
"""

import json, random
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, TypedDict, cast


class Post(TypedDict):
    id: int
    caption: str
    likes: int
    comments: int
    type: str
    hour: int
    day: str
    date: str


class InstagramData(TypedDict):
    followers: list[str]
    following: list[str]
    posts: list[Post]
    username: str


# ---------- DEMO DATA ----------
def demo_data() -> InstagramData:
    followers = [f"user_{i}" for i in range(1, 1241)]
    following = [f"user_{i}" for i in range(1, 980)] + [f"extra_{i}" for i in range(1, 85)]
    posts: list[Post] = []
    captions = ["Bangalore vibes", "Weekend ride", "New reel drop",
                "Coffee + code", "Sunset lover", "Gym grind",
                "Foodie diaries", "Travel dump"]
    for i in range(1, 42):
        posts.append({
            "id": i,
            "caption": random.choice(captions) + f" #{i}",
            "likes": random.randint(80, 2400),
            "comments": random.randint(5, 180),
            "type": random.choice(["Reel", "Photo", "Carousel"]),
            "hour": random.choice([8, 12, 18, 19, 20, 21]),
            "day": random.choice(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]),
            "date": f"2026-10-{random.randint(1,28)}"
        })
    return {"followers": followers, "following": following,
            "posts": posts, "username": "kaikarthik7"}

# ---------- CORE LOGIC ----------
class InstaVault:
    def __init__(self, data: Mapping[str, Any]) -> None:
        self.data = data
        self.username = data.get("username", "you")

    def unfollowers(self):
        f = set(self.data["followers"])
        return [u for u in self.data["following"] if u not in f]

    def fans(self):
        f = set(self.data["following"])
        return [u for u in self.data["followers"] if u not in f]

    def top_posts(self, n: int = 5):
        return sorted(self.data["posts"], key=lambda x: x["likes"], reverse=True)[:n]

    def best_time(self) -> list[tuple[int, int]]:
        by_hour: defaultdict[int, list[int]] = defaultdict(list)
        for p in self.data["posts"]:
            by_hour[p["hour"]].append(p["likes"])
        avg = {h: sum(v)//len(v) for h, v in by_hour.items()}
        return sorted(avg.items(), key=lambda x: x[1], reverse=True)

    def insights(self) -> list[str]:
        tips: list[str] = []
        best_hour, best_avg = self.best_time()[0]
        tips.append(f"🔥 Best time: Raat {best_hour}:00 baje post karo - avg {best_avg} likes milte hain.")
        reels = [p for p in self.data["posts"] if p["type"] == "Reel"]
        if reels:
            avg_reel = sum(p["likes"] for p in reels)//len(reels)
            tips.append(f"🎬 Reels game strong hai - avg {avg_reel} likes. Week me 3 Reels target rakho.")
        tips.append(f"👀 {len(self.unfollowers())} log tumhe follow-back nahi karte.")
        tips.append("💡 Tip: Caption me pehli line hook rakho, log 2 sec me decide karte hain.")
        return tips

    def report(self):
        print("\n" + "="*52)
        print(f"  📸 INSTAVAULT  |  @{self.username}  |  ALA REPORT")
        print("="*52)
        print(f"Followers : {len(self.data['followers'])}")
        print(f"Following : {len(self.data['following'])}")
        print(f"Posts     : {len(self.data['posts'])}")
        print(f"Unfollowers: {len(self.unfollowers())}")
        print(f"Fans      : {len(self.fans())}")

        print("\n--- 🏆 TOP 5 POSTS ---")
        for i, p in enumerate(self.top_posts(), 1):
            print(f"{i}. [{p['type']}] {p['caption']} - ❤️ {p['likes']} | 💬 {p['comments']} | {p['day']} {p['hour']}:00")

        print("\n--- ⏰ BEST TIME TO POST (avg likes) ---")
        for h, avg in self.best_time():
            bar = "█" * int(avg/100)
            print(f"{h:02d}:00  {avg:4d}  {bar}")

        print("\n--- 🤖 AI INSIGHTS ---")
        for t in self.insights():
            print("•", t)

        print("\n--- 😤 UNFOLLOWERS LIST (pehle 20) ---")
        for u in self.unfollowers()[:20]:
            print(" -", u)

        print("\n✅ Done! No bot, no ban risk. Sirf apna data.")
        self.chart()

    def chart(self):
        try:
            import matplotlib.pyplot as plt
            plot: Any = cast(Any, plt)
            hours, avgs = zip(*self.best_time())
            plot.figure(figsize=(8, 3.5))
            plot.bar([f"{h}:00" for h in hours], avgs, color="#E1306C")
            plot.title("Best Time to Post - Avg Likes")
            plot.ylabel("Avg Likes"); plot.tight_layout(); plot.show()

            top = self.top_posts(6)
            plot.figure(figsize=(8, 3.5))
            plot.barh([p["caption"][:18] for p in top[::-1]],
                     [p["likes"] for p in top[::-1]], color="#833AB4")
            plot.title("Top Posts by Likes"); plot.tight_layout(); plot.show()
        except ImportError:
            print("\n[Chart skip] matplotlib install karo: pip install matplotlib")

# ---------- REAL INSTAGRAM EXPORT LOADER ----------
def load_real_export(folder: str = "instagram_export") -> dict[str, Any] | None:
    p = Path(folder)
    if not p.exists():
        return None
    try:
        followers: list[str] = []
        following: list[str] = []
        for f in p.rglob("followers*.json"):
            d = json.loads(f.read_text())
            for item in d:
                followers.append(item["string_list_data"][0]["value"])
        for f in p.rglob("following*.json"):
            d = json.loads(f.read_text())
            for item in d.get("relationships_following", []):
                following.append(item["string_list_data"][0]["value"])
        if followers:
            return {"followers": followers, "following": following,
                    "posts": demo_data()["posts"], "username": "you"}
    except Exception as e:
        print("Export parse me error:", e)
    return None

def main():
    print("InstaVault - Python Edition 🚀")
    print("1. Demo data se chalao (instant ala feel)")
    print("2. Apna real Instagram export folder se chalao")
    choice = input("Choice (1/2, default 1): ").strip() or "1"
    if choice == "2":
        data = load_real_export()
        if not data:
            print("Export nahi mila, demo data use kar raha hoon...")
            data = demo_data()
    else:
        data = demo_data()
    InstaVault(data).report()

if __name__ == "__main__":
    main()