import tkinter as tk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
nltk.download('vader_lexicon')

class SentimentalAnalysisGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sentimental Analysis")

        # Create input label and text box
        self.input_label = tk.Label(self.window, text="Enter text:")
        self.input_label.pack()
        self.input_text = tk.Text(self.window, height=10, width=50)
        self.input_text.pack()

        # Create button to analyze sentiment
        self.analyze_button = tk.Button(self.window, text="Analyze Sentiment", command=self.analyze_sentiment)
        self.analyze_button.pack()

        # Create button to load text file
        self.load_button = tk.Button(self.window, text="Load Text File", command=self.load_text_file)
        self.load_button.pack()

        # Create button to save analysis result
        self.save_button = tk.Button(self.window, text="Save Analysis Result", command=self.save_analysis_result)
        self.save_button.pack()

        # Create label to display sentiment result
        self.sentiment_label = tk.Label(self.window, text="")
        self.sentiment_label.pack()

        # Create button to generate word cloud
        self.wordcloud_button = tk.Button(self.window, text="Generate Word Cloud", command=self.generate_wordcloud)
        self.wordcloud_button.pack()

        # Initialize sentiment result
        self.sentiment_result = None

    def analyze_sentiment(self):
        # Get input text
        text = self.input_text.get("1.0", "end-1c")

        # Initialize sentiment analyzer
        sia = SentimentIntensityAnalyzer()

        # Analyze sentiment
        sentiment = sia.polarity_scores(text)

        # Determine sentiment label
        if sentiment['compound'] >= 0.05:
            sentiment_label = "Positive"
        elif sentiment['compound'] <= -0.05:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        # Display sentiment result
        self.sentiment_result = {
            "Sentiment": sentiment_label,
            "Positive": sentiment['pos'],
            "Negative": sentiment['neg'],
            "Neutral": sentiment['neu']
        }
        self.sentiment_label.config(text=f"Sentiment: {sentiment_label}\n"
                                       f"Positive: {sentiment['pos']:.2f}\n"
                                       f"Negative: {sentiment['neg']:.2f}\n"
                                       f"Neutral: {sentiment['neu']:.2f}")

    def load_text_file(self):
        # Open file dialog to select text file
        file_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])

        # Read text from file
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", text)

    def save_analysis_result(self):
        # Check if sentiment result is available
        if self.sentiment_result:
            # Open file dialog to save analysis result
            file_path = filedialog.asksaveasfilename(title="Save Analysis Result", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

            # Save analysis result to CSV file
            if file_path:
                pd.DataFrame([self.sentiment_result]).to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Analysis result saved successfully!")
        else:
            messagebox.showerror("Error", "No analysis result available!")

    def generate_wordcloud(self):
        # Get input text
        text = self.input_text.get("1.0", "end-1c")

        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400).generate(text)

        # Display word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = SentimentalAnalysisGUI()
    gui.run()