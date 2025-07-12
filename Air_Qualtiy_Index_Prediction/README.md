Air Quality Index Prediction
Overview
This project uses a Random Forest Regressor model to predict the Air Quality Index (AQI) based on various pollutant concentrations and city information. The model is trained on a dataset of city-day level air quality data and is deployed as a Streamlit web application.
Features
Predicts AQI based on pollutant concentrations (PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene) and city information
Uses a Random Forest Regressor model for prediction
Deployed as a Streamlit web application for easy interaction
Requirements
Python 3.x
NumPy
Pandas
Scikit-learn
Streamlit
Joblib
Installation
Clone the repository: git clone https://github.com/your-username/air-quality-index-prediction.git
Install the required packages: pip install -r requirements.txt
Download the dataset and place it in the project directory
Usage
Run the Streamlit application: streamlit run app.py
Open a web browser and navigate to http://localhost:8501
Select a city and input pollutant concentrations to predict the AQI
Model Performance
The model performance is not evaluated in this repository. You can add your own evaluation metrics and methods to assess the model's performance.
Contributing
Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.
License
This project is licensed under the MIT License. See LICENSE for details.
Acknowledgments
The dataset used in this project is assumed to be publicly available.
The Streamlit library is used for deploying the model as a web application.
Future Work
Evaluate the model's performance on a test dataset
Explore other machine learning models for AQI prediction
Integrate real-time air quality data for more accurate predictions