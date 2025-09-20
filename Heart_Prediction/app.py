from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model and scaler
model = joblib.load('heart_disease_model.pkl')
scaler = joblib.load('scaler.pkl')

# Define a function to validate user input data
def validate_data(data):
    required_fields = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    for field in required_fields:
        if field not in data:
            return False
    return True

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not validate_data(data):
            return jsonify({'error': 'Invalid request data'}), 400
        features = pd.DataFrame([data])
        features = scaler.transform(features)
        prediction = model.predict(features)
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)