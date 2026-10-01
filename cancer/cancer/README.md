# Cancer_Sentiment_Analyses

This Python script performs sentiment analysis on tweets related to cancer using two libraries: NLTK's VADER and TextBlob. Here's a breakdown of the code:
Key Features:
Tweet Fetching: Fetches tweets based on a specific query (#cancer) using the Tweepy library.
Sentiment Analysis: Performs sentiment analysis using NLTK's VADER and TextBlob libraries, categorizing tweets as Positive, Negative, or Neutral.
Data Visualization: Plots the sentiment distribution using a pie chart for both VADER and TextBlob analyses.
Code Structure:
Tweet Fetching Function: fetch_tweets function fetches tweets based on a query and count.
Sentiment Analysis Functions: analyze_sentiment_vader and analyze_sentiment_textblob functions perform sentiment analysis using VADER and TextBlob, respectively.
Data Visualization Function: plot_sentiment_distribution function plots the sentiment distribution.
Main Function: main function calls the above functions and displays the results.
