import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
import csv
import os
from typing import Any

# 👇 PASTE YOUR FREE OMDB API KEY HERE
API_KEY = "YOUR_OMDB_API_KEY"
# Get it from: http://www.omdbapi.com/apikey.aspx

class MovieScraper:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Movie Scraper")
        self.root.geometry("850x600")
        self.root.configure(bg="#1a1a2e")

        self.movies: list[dict[str, Any]] = []  # to save to csv
        self.poster_img = None

        # --- Title ---
        tk.Label(root, text="🎬 MOVIE SCRAPER", font=("Arial", 20, "bold"),
                 bg="#1a1a2e", fg="white").pack(pady=15)

        # --- Search Box ---
        search_frame = tk.Frame(root, bg="#1a1a2e")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Movie Name:", bg="#1a1a2e", fg="white",
                 font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        self.entry = tk.Entry(search_frame, width=35, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda _event: self.search_movie())

        tk.Button(search_frame, text="Search", bg="#e94560", fg="white",
                  font=("Arial", 11, "bold"), command=self.search_movie).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Save to CSV", bg="#0f3460", fg="white",
                  font=("Arial", 11, "bold"), command=self.save_csv).pack(side=tk.LEFT, padx=5)

        # --- Main Area ---
        main = tk.Frame(root, bg="#1a1a2e")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Poster left
        self.poster_label = tk.Label(main, text="No Poster", bg="#16213e",
                                     fg="white", width=30, height=20)
        self.poster_label.pack(side=tk.LEFT, padx=10)

        # Details right
        right = tk.Frame(main, bg="#1a1a2e")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(right, text="", font=("Arial", 16, "bold"),
                                    bg="#1a1a2e", fg="white", wraplength=400, justify="left")
        self.title_label.pack(anchor="w", pady=5)

        self.details = tk.Text(right, height=18, width=55, font=("Arial", 11),
                               bg="#16213e", fg="white", wrap=tk.WORD)
        self.details.pack(fill=tk.BOTH, expand=True)

        tk.Button(right, text="Download Poster", bg="#e94560", fg="white",
                  command=self.download_poster).pack(pady=8)

        # --- Status ---
        self.status = tk.Label(root, text="Enter a movie name and press Search",
                               bg="#1a1a2e", fg="#a8a8a8")
        self.status.pack(pady=5)

    def search_movie(self):
        name = self.entry.get().strip()
        if not name:
            messagebox.showwarning("Empty", "Please enter a movie name")
            return

        if API_KEY == "YOUR_OMDB_API_KEY":
            messagebox.showerror("API Key Missing",
                "Please paste your free OMDB API key in the code.\nGet it from omdbapi.com/apikey.aspx")
            return

        self.status.config(text=f"Scraping '{name}'...")
        self.root.update()

        try:
            url = f"http://www.omdbapi.com/?t={name}&apikey={API_KEY}&plot=full"
            res = requests.get(url, timeout=10)
            data = res.json()

            if data.get("Response") == "False":
                messagebox.showerror("Not Found", f"Movie not found: {data.get('Error')}")
                self.status.config(text="Not found")
                return

            # Save for CSV
            self.current = data
            self.movies.append(data)

            # Show details
            self.title_label.config(text=f"{data.get('Title')} ({data.get('Year')})")
            info = f"""⭐ IMDb Rating: {data.get('imdbRating')} / 10
🎭 Genre: {data.get('Genre')}
📅 Released: {data.get('Released')}
⏱️ Runtime: {data.get('Runtime')}
🎬 Director: {data.get('Director')}
👥 Actors: {data.get('Actors')}
🌍 Language: {data.get('Language')}
🏆 Awards: {data.get('Awards')}
💰 Box Office: {data.get('BoxOffice')}

📖 Plot:
{data.get('Plot')}
"""
            self.details.delete("1.0", tk.END)
            self.details.insert("1.0", info)

            # Load poster
            poster_url = data.get("Poster")
            if poster_url and poster_url != "N/A":
                img_data = requests.get(poster_url).content
                img = Image.open(BytesIO(img_data))
                img = img.resize((250, 370))
                self.poster_img = ImageTk.PhotoImage(img)
                self.poster_label.config(image=self.poster_img, text="")
                self.poster_url = poster_url
            else:
                self.poster_label.config(image="", text="No Poster")

            self.status.config(text=f"Found: {data.get('Title')} | Total scraped: {len(self.movies)}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error")

    def download_poster(self):
        if not hasattr(self, 'current'):
            messagebox.showwarning("No Movie", "Search a movie first")
            return
        try:
            os.makedirs("posters", exist_ok=True)
            name = self.current.get('Title').replace(" ", "_").replace(":", "")
            img_data = requests.get(self.current.get("Poster")).content
            path = f"posters/{name}.jpg"
            with open(path, "wb") as f:
                f.write(img_data)
            messagebox.showinfo("Saved", f"Poster saved to {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_csv(self):
        if not self.movies:
            messagebox.showwarning("Empty", "No movies scraped yet")
            return
        with open("movies.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Title", "Year", "imdbRating", "Genre", "Director", "Actors", "Plot", "Poster"])
            writer.writeheader()
            for m in self.movies:
                writer.writerow({k: m.get(k, "") for k in ["Title", "Year", "imdbRating", "Genre", "Director", "Actors", "Plot", "Poster"]})
        messagebox.showinfo("Saved", f"Saved {len(self.movies)} movies to movies.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieScraper(root)
    root.mainloop()