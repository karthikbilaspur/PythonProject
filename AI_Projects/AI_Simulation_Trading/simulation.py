from typing import Any, cast

import pandas as pd
import numpy as np
import nltk  # type: ignore[import-not-found]
from nltk.sentiment import SentimentIntensityAnalyzer  # type: ignore[import-not-found]
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import yfinance as yf  # type: ignore[import-not-found]

# Retrieve stock data
stock_data = yf.download('AAPL', start='2020-01-01', end='2022-02-26', progress=False)  # type: ignore[reportUnknownMemberType]
if stock_data is None or stock_data.empty:
    raise ValueError('Unable to download stock data for AAPL.')

stock_data = stock_data.reset_index().copy()
if 'Date' in stock_data.columns and 'date' not in stock_data.columns:
    stock_data = stock_data.rename(columns={'Date': 'date'})
stock_data['date'] = pd.to_datetime(stock_data['date'])

# Retrieve news articles
news_data = pd.read_csv('news_articles.csv')
if 'date' not in news_data.columns:
    raise ValueError("'date' column not found in news_articles.csv.")
if 'article_text' not in news_data.columns:
    raise ValueError("'article_text' column not found in news_articles.csv.")

news_data = news_data[['date', 'article_text']].dropna().copy()
news_data['date'] = pd.to_datetime(news_data['date'])

# Perform sentiment analysis on news articles
nltk.download('vader_lexicon', quiet=True)  # type: ignore[reportUnknownMemberType]
sia = SentimentIntensityAnalyzer()
news_data['sentiment'] = news_data['article_text'].map(
    lambda x: float(cast(dict[str, float], sia.polarity_scores(str(x)))['compound'])
)

# Merge stock data and news data
merged_data = pd.merge(
    stock_data[['date', 'Close']],
    news_data[['date', 'sentiment']],
    on='date',
    how='inner',
)
if merged_data.empty:
    raise ValueError('No overlapping dates between stock data and news data.')

# Create features and target variable
merged_data = merged_data.sort_values('date').reset_index(drop=True)
X = merged_data[['sentiment', 'Close']].iloc[:-1].copy().astype(float)
y = (merged_data['Close'].shift(-1).iloc[:-1] > merged_data['Close'].iloc[:-1]).astype(bool)

# Split data into training and testing sets
X_values = X.to_numpy(dtype=float)
y_values = y.to_numpy(dtype=bool)
X_train, X_test, y_train, y_test = train_test_split(
    X_values, y_values, test_size=0.2, random_state=42, shuffle=False
)

# Train random forest classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Make predictions on test data
y_pred = rf.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy:.3f}')

# Simulate trading
capital = 10000.0
shares = 0
for record in merged_data.to_dict(orient='records'):
    sentiment = float(record['sentiment'])
    close_price = float(record['Close'])
    prediction = rf.predict(np.asarray([[sentiment, close_price]], dtype=float))
    buy_signal = bool(prediction[0])

    if buy_signal:
        # Buy shares
        shares += 10
        capital -= close_price * 10
    elif shares > 0:
        # Sell shares
        shares -= 10
        capital += close_price * 10

    date_value = pd.Timestamp(cast(Any, record['date']))
    print(f'Day {date_value.date()}: Capital={capital:.2f}, Shares={shares}')

print(f'Final Capital: {capital:.2f}')