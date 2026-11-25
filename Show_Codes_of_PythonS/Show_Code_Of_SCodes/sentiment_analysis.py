import tkinter as tk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sentiment Analyzer")
        self.root.config(background="light blue")
        self.root.geometry("600x500")

        self.sia = SentimentIntensityAnalyzer()

        self.create_widgets()

    def create_widgets(self):
        self.text_label = tk.Label(self.root, text="Enter Your Sentence:", bg="light blue")
        self.text_label.pack(pady=10)

        self.text_area = tk.Text(self.root, height=10, width=70, font="lucida 13")
        self.text_area.pack(pady=10)

        self.button_frame = tk.Frame(self.root, bg="light blue")
        self.button_frame.pack(pady=10)

        self.check_button = tk.Button(self.button_frame, text="Check Sentiment", fg="Black", bg="light yellow", command=self.detect_sentiment)
        self.check_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(self.button_frame, text="Clear", fg="Black", bg="light yellow", command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.button_frame, text="Exit", fg="Black", bg="light yellow", command=self.root.quit)
        self.exit_button.pack(side=tk.LEFT, padx=10)

        self.result_frame = tk.Frame(self.root, bg="light blue")
        self.result_frame.pack(pady=10)

        self.sentiment_labels = {
            "positive": tk.Label(self.result_frame, text="Positive Sentiment:", bg="light blue"),
            "neutral": tk.Label(self.result_frame, text="Neutral Sentiment:", bg="light blue"),
            "negative": tk.Label(self.result_frame, text="Negative Sentiment:", bg="light blue"),
            "overall": tk.Label(self.result_frame, text="Overall Sentiment:", bg="light blue")
        }

        for label in self.sentiment_labels.values():
            label.pack(pady=5)

        self.sentiment_entries = {
            "positive": tk.Entry(self.result_frame),
            "neutral": tk.Entry(self.result_frame),
            "negative": tk.Entry(self.result_frame),
            "overall": tk.Entry(self.result_frame)
        }

        for entry in self.sentiment_entries.values():
            entry.pack(pady=5)

    def detect_sentiment(self):
        sentence = self.text_area.get("1.0", tk.END)
        sentiment_dict = self.sia.polarity_scores(sentence)

        self.sentiment_entries["positive"].delete(0, tk.END)
        self.sentiment_entries["positive"].insert(0, f"{sentiment_dict['pos']*100:.2f}%")

        self.sentiment_entries["neutral"].delete(0, tk.END)
        self.sentiment_entries["neutral"].insert(0, f"{sentiment_dict['neu']*100:.2f}%")

        self.sentiment_entries["negative"].delete(0, tk.END)
        self.sentiment_entries["negative"].insert(0, f"{sentiment_dict['neg']*100:.2f}%")

        if sentiment_dict['compound'] >= 0.05:
            overall_sentiment = "Positive"
        elif sentiment_dict['compound'] <= -0.05:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Neutral"

        self.sentiment_entries["overall"].delete(0, tk.END)
        self.sentiment_entries["overall"].insert(0, overall_sentiment)

    def clear_all(self):
        self.text_area.delete("1.0", tk.END)
        for entry in self.sentiment_entries.values():
            entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SentimentAnalyzer()
    app.run()