from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)

model = load_model('model/digit_recognition_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    image_data = request.get_json()['image']

    image_array = np.array(image_data).reshape((280, 280))

    image_array = np.array(Image.fromarray(image_array).resize((28, 28)))

    image_array = image_array / 255.0

    image_array = image_array.reshape((1, 28, 28, 1))

    prediction = model.predict(image_array)

    predicted_digit = np.argmax(prediction)

    return jsonify({'prediction': int(predicted_digit)})

if __name__ == '__main__':
    app.run(debug=True)