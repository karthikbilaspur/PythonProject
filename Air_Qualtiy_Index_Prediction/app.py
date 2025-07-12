import numpy as np
import pandas as pd
import streamlit as st
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load data
df = pd.read_csv("city_day.csv", na_values="=")

# Preprocess data
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# Drop columns
df = df.drop(["Date", "AQI_Bucket"], axis=1)

# Encode city
label_encoder = LabelEncoder()
df["City"] = label_encoder.fit_transform(df["City"])

# Define city mapping
city_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))

# Split data
y = df.pop("AQI")
x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=0)

# Train model
model = RandomForestRegressor(max_depth=50, random_state=0)
model.fit(x_train, y_train)

# Save model
joblib.dump(model, "aqi_model.joblib")

# Load model
# model = joblib.load("aqi_model.joblib")

def main():
    st.title("Air Quality Index Prediction")

    st.write("## User Input Features")

    # Get city names
    city_names = list(city_mapping.keys())

    # Create input form
    city = st.selectbox("City", city_names)
    city_encoded = city_mapping[city]

    pm2_5 = st.slider("PM2.5", float(df["PM2.5"].min()), float(df["PM2.5"].max()), float(df["PM2.5"].mean()))
    pm10 = st.slider("PM10", float(df["PM10"].min()), float(df["PM10"].max()), float(df["PM10"].mean()))
    no = st.slider("NO", float(df["NO"].min()), float(df["NO"].max()), float(df["NO"].mean()))
    no2 = st.slider("NO2", float(df["NO2"].min()), float(df["NO2"].max()), float(df["NO2"].mean()))
    nox = st.slider("NOx", float(df["NOx"].min()), float(df["NOx"].max()), float(df["NOx"].mean()))
    nh3 = st.slider("NH3", float(df["NH3"].min()), float(df["NH3"].max()), float(df["NH3"].mean()))
    co = st.slider("CO", float(df["CO"].min()), float(df["CO"].max()), float(df["CO"].mean()))
    so2 = st.slider("SO2", float(df["SO2"].min()), float(df["SO2"].max()), float(df["SO2"].mean()))
    o3 = st.slider("O3", float(df["O3"].min()), float(df["O3"].max()), float(df["O3"].mean()))
    benzene = st.slider("Benzene", float(df["Benzene"].min()), float(df["Benzene"].max()), float(df["Benzene"].mean()))
    toluene = st.slider("Toluene", float(df["Toluene"].min()), float(df["Toluene"].max()), float(df["Toluene"].mean()))
    xylene = st.slider("Xylene", float(df["Xylene"].min()), float(df["Xylene"].max()), float(df["Xylene"].mean()))

    # Create input data
    input_data = pd.DataFrame({
        "City": [city_encoded],
        "PM2.5": [pm2_5],
        "PM10": [pm10],
        "NO": [no],
        "NO2": [no2],
        "NOx": [nox],
        "NH3": [nh3],
        "CO": [co],
        "SO2": [so2],
        "O3": [o3],
        "Benzene": [benzene],
        "Toluene": [toluene],
        "Xylene": [xylene]
    })

    # Display city mapping
    st.sidebar.write("## City Label Mapping")
    st.sidebar.write(city_mapping)

    # Make prediction
    prediction = model.predict(input_data)

    # Display prediction
    st.write("## Prediction")
    st.write(f"Predicted AQI: {prediction[0]}")

if __name__ == "__main__":
    main()