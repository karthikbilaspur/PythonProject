import tkinter as tk
from tkinter import ttk
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import download
download('vader_lexicon')

# Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def analyze_sentiment():
    search_term = search_entry.get()
    language = language_var.get()
    location = location_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    tweets = api.search_tweets(q=search_term, lang=language, count=100)

    sia = SentimentIntensityAnalyzer()
    tweet_data = []

    for tweet in tweets:
        sentiment = sia.polarity_scores(tweet.text)
        tweet_data.append({
            'text': tweet.text,
            'sentiment': sentiment['compound'],
            'location': tweet.user.location,
            'date': tweet.created_at
        })

    df = pd.DataFrame(tweet_data)

    # Filter by location
    if location:
        df = df[df['location'] == location]

    # Filter by date range
    if start_date and end_date:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Sentiment analysis
    positive_tweets = len(df[df['sentiment'] > 0])
    negative_tweets = len(df[df['sentiment'] < 0])
    neutral_tweets = len(df[df['sentiment'] == 0])

    # Update GUI
    positive_label.config(text=f"Positive tweets: {positive_tweets}")
    negative_label.config(text=f"Negative tweets: {negative_tweets}")
    neutral_label.config(text=f"Neutral tweets: {neutral_tweets}")

    # Plot sentiment distribution
    plt.bar(['Positive', 'Negative', 'Neutral'], [positive_tweets, negative_tweets, neutral_tweets])
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title('Sentiment Distribution')
    plt.show()

    # Display tweet table
    tweet_table.delete(0, tk.END)
    for index, row in df.iterrows():
        tweet_table.insert(tk.END, f"{row['text']} - {row['sentiment']}")

def export_data():
    df = pd.DataFrame(tweet_data)
    df.to_csv('tweet_data.csv', index=False)

root = tk.Tk()
root.title("Twitter Sentiment Analysis")

# Search term
search_label = tk.Label(root, text="Search term:")
search_label.pack()
search_entry = tk.Entry(root, width=50)
search_entry.pack()

# Language
language_label = tk.Label(root, text="Language:")
language_label.pack()
language_var = tk.StringVar(root)
language_var.set("en")
language_option = tk.OptionMenu(root, language_var, "en", "es", "fr")
language_option.pack()

# Location
location_label = tk.Label(root, text="Location:")
location_label.pack()
location_entry = tk.Entry(root, width=50)
location_entry.pack()

# Date range
start_date_label = tk.Label(root, text="Start date (YYYY-MM-DD):")
start_date_label.pack()
start_date_entry = tk.Entry(root, width=50)
start_date_entry.pack()

end_date_label = tk.Label(root, text="End date (YYYY-MM-DD):")
end_date_label.pack()
end_date_entry = tk.Entry(root, width=50)
end_date_entry.pack()

# Analyze button
analyze_button = tk.Button(root, text="Analyze", command=analyze_sentiment)
analyze_button.pack()

# Sentiment labels
positive_label = tk.Label(root, text="Positive tweets: 0")
positive_label.pack()
negative_label = tk.Label(root, text="Negative tweets: 0")
negative_label.pack()
neutral_label = tk.Label(root, text="Neutral tweets: 0")
neutral_label.pack()

# Tweet table
tweet_table = tk.Listbox(root, width=100)
tweet_table.pack()

# Export button
export_button = tk.Button(root, text="Export data", command=export_data)
export_button.pack()

root.mainloop()