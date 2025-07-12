import streamlit as st
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

# Load data
data = pd.read_excel("data.xlsx")

# Split data into features and target
y = data['label']
X = data.drop(["label"], axis=1)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=0)

# Train logistic regression model
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)

# Evaluate model
y_pred = lr.predict(X_test)
st.write("Model Evaluation:")
st.write(classification_report(y_test, y_pred))

def predict_crop(input_data):
    """Predict crop label based on input data."""
    input_data_scaled = scaler.transform(input_data)
    crop_label = lr.predict(input_data_scaled)
    return crop_label[0]

def main():
    st.title("Agriculture Optimisation App")
    st.write("Enter the parameter values to predict the crop label:")

    col1, col2, col3 = st.columns(3)
    n = col1.number_input("N", value=0.0)
    p = col1.number_input("P", value=0.0)
    k = col2.number_input("K", value=0.0)
    temperature = col2.number_input("Temperature", value=0.0)
    humidity = col3.number_input("Humidity", value=0.0)
    ph = col3.number_input("pH", value=0.0)
    rainfall = st.number_input("Rainfall", value=0.0)

    input_data = np.array([[n, p, k, temperature, humidity, ph, rainfall]])

    crop_label = predict_crop(input_data)

    st.subheader("Predicted Crop Label:")
    st.write(crop_label)

    # Additional features
    st.subheader("About the Model:")
    st.write("This model uses Logistic Regression to predict crop labels based on input parameters.")
    st.write("The model was trained on a dataset with the following features:")
    st.write(data.columns)

if __name__ == '__main__':
    main()