import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfullerimport requests
from bs4 import BeautifulSoup
import time

# Amazon Product Advertising API credentials
access_key = "YOUR_ACCESS_KEY"
secret_key = "YOUR_SECRET_KEY"
associate_tag = "YOUR_ASSOCIATE_TAG"

# Function to get product data using Amazon Product Advertising API
def get_product_data(asin):
    url = f"http://webservices.amazon.com/onca/xml?Service=AWSECommerceService&Operation=ItemLookup&ItemId={asin}&ResponseGroup=Large&AWSAccessKeyId={access_key}&AssociateTag={associate_tag}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    price = soup.find('LowestNewPrice').text.strip()
    reviews = soup.find('TotalReviews').text.strip()
    sales_rank = soup.find('SalesRank').text.strip()
    return price, reviews, sales_rank

# Function to track price history
def track_price_history(asin):
    price_data = []
    for i in range(30):  # Track price for 30 days
        price, reviews, sales_rank = get_product_data(asin)
        price_data.append({'Date': pd.to_datetime('today'), 'Price': price, 'Reviews': reviews, 'SalesRank': sales_rank})
        time.sleep(86400)  # Wait 1 day before checking price again
    return pd.DataFrame(price_data)

# Function to build ARIMA model
def build_arima_model(price_data):
    model = ARIMA(price_data['Price'], order=(1,1,1))
    model_fit = model.fit()
    return model_fit

# Function to build LSTM model
def build_lstm_model(price_data):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(price_data[['Price']])
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(scaled_data.shape¹, 1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, min_delta=0.001)
    model.fit(scaled_data, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    return model

# Track price history
price_data = track_price_history("B076MX9GVR")

# Build ARIMA model
arima_model = build_arima_model(price_data)

# Build LSTM model
lstm_model = build_lstm_model(price_data)

# Predict future price using ARIMA model
future_price_arima = arima_model.forecast(steps=7)

# Predict future price using LSTM model
future_price_lstm = lstm_model.predict(np.array([price_data['Price'].values[-7:]]))

print(f"Predicted price in 7 days using ARIMA: ${future_price_arima:.2f}")
print(f"Predicted price in 7 days using LSTM: ${future_price_lstm:.2f}")