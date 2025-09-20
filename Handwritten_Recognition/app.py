from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

model = load_model('handwritten_character_recognition_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    image_data = request.get_json()['image']
    image_array = np.array(image_data).reshape((28, 28))
    image_array = 255 - image_array
    image_array = image_array / 255.0
    image_array = image_array.reshape((1, 28, 28, 1))
    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction)
    return jsonify({'prediction': chr(predicted_class + 65)})

if __name__ == '__main__':
    app.run(debug=True)