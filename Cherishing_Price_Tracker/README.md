# Amazon Price Prediction Project

A Python project that uses machine learning models (ARIMA and LSTM) to predict future prices of Amazon products.

## Features

* **Amazon Product Advertising API**: Retrieves product data, including price, reviews, and sales rank.
* **ARIMA Model**: A statistical model that combines autoregression, differencing, and moving average components to forecast future prices.
* **LSTM Model**: A type of recurrent neural network that captures complex temporal dependencies in sequential data, making it suitable for time series forecasting.
* **Price Prediction**: Predicts future prices using ARIMA and LSTM models.

## Requirements

* **Python 3.x**: Required to run the script.
* **TensorFlow**: Required for building and training LSTM models.
* **Statsmodels**: Required for building and training ARIMA models.
* **Pandas**: Required for data manipulation and analysis.
* **NumPy**: Required for numerical computations.
* **Scikit-learn**: Required for data preprocessing and model evaluation.
* **Requests**: Required for making HTTP requests to Amazon.
* **BeautifulSoup**: Required for parsing HTML and XML responses.

## Installation

1. Install Python 3.x if you haven't already.
2. Install the required libraries using pip:
```bash
pip install tensorflow statsmodels pandas numpy scikit-learn requests beautifulsoup4