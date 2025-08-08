import tweepy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Twitter API credentials
consumer_key = 'your-consumer-key'
consumer_secret = 'your-consumer-secret'
access_token = 'your-access-token'
access_token_secret = 'your-access-token-secret'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define search query and fetch tweets
def fetch_tweets(query, count):
    try:
        tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en').items(count)
        return [tweet.text for tweet in tweets]
    except tweepy.TweepError as e:
        print(f"Error fetching tweets: {e}")
        return []

# Sentiment analysis using NLTK's VADER
def analyze_sentiment_vader(tweets):
    sia = SentimentIntensityAnalyzer()
    sentiments = []
    for tweet in tweets:
        sentiment = sia.polarity_scores(tweet)
        if sentiment['compound'] >= 0.05:
            sentiments.append('Positive')
        elif sentiment['compound'] <= -0.05:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')
    return sentiments

# Sentiment analysis using TextBlob
def analyze_sentiment_textblob(tweets):
    sentiments = []
    for tweet in tweets:
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            sentiments.append('Positive')
        elif analysis.sentiment.polarity < 0:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')
    return sentiments

# Plot sentiment distribution
def plot_sentiment_distribution(sentiments):
    sentiment_counts = Counter(sentiments)
    labels = list(sentiment_counts.keys())
    sizes = list(sentiment_counts.values())
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Sentiment Distribution')
    plt.show()

# Main function
def main():
    query = '#cancer'
    count = 100
    tweets = fetch_tweets(query, count)
    
    # Sentiment analysis using NLTK's VADER
    sentiments_vader = analyze_sentiment_vader(tweets)
    df_vader = pd.DataFrame({'Tweet': tweets, 'Sentiment': sentiments_vader})
    print("VADER Sentiment Analysis:")
    print(df_vader.head())
    plot_sentiment_distribution(sentiments_vader)
    
    # Sentiment analysis using TextBlob
    sentiments_textblob = analyze_sentiment_textblob(tweets)
    df_textblob = pd.DataFrame({'Tweet': tweets, 'Sentiment': sentiments_textblob})
    print("\nTextBlob Sentiment Analysis:")
    print(df_textblob.head())
    plot_sentiment_distribution(sentiments_textblob)

if __name__ == '__main__':
    nltk.download('vader_lexicon')
    main()