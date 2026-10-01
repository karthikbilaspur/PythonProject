import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import LSTM, Dense

# Amazon Product Advertising API credentials
access_key = "YOUR_ACCESS_KEY"
secret_key = "YOUR_SECRET_KEY"
associate_tag = "YOUR_ASSOCIATE_TAG"


# Function to get product data using Amazon Product Advertising API
def get_product_data(asin: str):
    url = (
        "http://webservices.amazon.com/onca/xml?Service=AWSECommerceService&"
        f"Operation=ItemLookup&ItemId={asin}&ResponseGroup=Large&"
        f"AWSAccessKeyId={access_key}&AssociateTag={associate_tag}"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "xml")

    def get_tag_text(tag_name: str):
        element = soup.find(tag_name)
        return element.text.strip() if element is not None else "0"

    price = get_tag_text("LowestNewPrice")
    reviews = get_tag_text("TotalReviews")
    sales_rank = get_tag_text("SalesRank")
    return price, reviews, sales_rank


# Function to track price history
def track_price_history(asin: str) -> pd.DataFrame:
    price_data = []
    for _ in range(30):
        price, reviews, sales_rank = get_product_data(asin)
        price_data.append(
            {
                "Date": pd.to_datetime("today"),
                "Price": float(price.replace("$", "")),
                "Reviews": int(reviews),
                "SalesRank": int(sales_rank),
            }
        )
        time.sleep(86400)
    return pd.DataFrame(price_data)


# Function to build ARIMA model
def build_arima_model(price_data: pd.DataFrame):
    prices = pd.to_numeric(price_data["Price"], errors="coerce").dropna()
    if prices.empty:
        raise ValueError("No valid prices found in the dataset")

    adfuller_result = adfuller(prices)
    print(f"ADF statistic: {adfuller_result[0]}, p-value: {adfuller_result[1]}")

    model = ARIMA(prices, order=(1, 1, 1))
    model_fit = model.fit()
    return model_fit


# Function to build LSTM model
def build_lstm_model(price_data: pd.DataFrame):
    prices = pd.to_numeric(price_data["Price"], errors="coerce").dropna().to_numpy(dtype=float)
    if prices.size < 10:
        raise ValueError("Not enough data points to train the LSTM model.")

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(prices.reshape(-1, 1))

    sequence_length = 7
    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i - sequence_length : i, 0])
        y.append(scaled_data[i, 0])

    X = np.array(X).reshape(-1, sequence_length, 1)
    y = np.array(y)

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(sequence_length, 1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mean_squared_error")

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=5,
        min_delta=0.001,
        restore_best_weights=True,
    )
    model.fit(X, y, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping], verbose=0)
    return model, scaler


if __name__ == "__main__":
    # Track price history
    price_data = track_price_history("B076MX9GVR")

    # Build ARIMA model
    arima_model = build_arima_model(price_data)

    # Build LSTM model
    lstm_model, scaler = build_lstm_model(price_data)

    # Predict future price using ARIMA model
    future_price_arima = arima_model.forecast(steps=7)

    # Predict future price using LSTM model
    last_sequence = pd.to_numeric(price_data["Price"], errors="coerce").dropna().to_numpy(dtype=float)[-7:]
    last_sequence_scaled = scaler.transform(last_sequence.reshape(-1, 1))
    future_price_lstm_scaled = lstm_model.predict(last_sequence_scaled.reshape(1, -1, 1), verbose=0)[0][0]
    future_price_lstm = scaler.inverse_transform(np.array([[future_price_lstm_scaled]])).item()

    print(f"Predicted price in 7 days using ARIMA: ${future_price_arima.mean():.2f}")
    print(f"Predicted price in 7 days using LSTM: ${future_price_lstm:.2f}")