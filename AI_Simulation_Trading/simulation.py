import pandas as pd
import numpy as np
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import yfinance as yf

# Retrieve stock data
stock_data = yf.download('AAPL', start='2020-01-01', end='2022-02-26')

# Retrieve news articles
news_data = pd.read_csv('news_articles.csv')

# Perform sentiment analysis on news articles
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
news_data['sentiment'] = news_data['article_text'].apply(lambda x: sia.polarity_scores(x)['compound'])

# Merge stock data and news data
merged_data = pd.merge(stock_data, news_data, on='date')

# Create features and target variable
X = merged_data[['sentiment', 'Close']]
y = merged_data['Close'].shift(-1) > merged_data['Close']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train random forest classifier
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

# Make predictions on test data
y_pred = rf.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy:.3f}')

# Simulate trading
capital = 10000
shares = 0
for i in range(len(stock_data)):
    sentiment = news_data.iloc[i]['sentiment']
    close_price = stock_data.iloc[i]['Close']
    prediction = rf.predict([[sentiment, close_price]])
    if prediction > 0.5:
        # Buy shares
        shares += 10
        capital -= close_price * 10
    else:
        # Sell shares
        if shares > 0:
            shares -= 10
            capital += close_price * 10
    print(f'Day {i+1}: Capital={capital:.2f}, Shares={shares}')

print(f'Final Capital: {capital:.2f}')