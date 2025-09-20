import cv2
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import RPi.GPIO as GPIO
import Adafruit_DHT
import requests
import time

# Set up GPIO pins for LED lights
GPIO.setmode(GPIO.BCM)
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

# Set up temperature and humidity sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 23

# Set up webcam
cap = cv2.VideoCapture(0)

# Set up thermostat API endpoint
thermostat_api = "http://thermostat-api.com/set-temperature"

# Collect training data
def collect_data():
    data = []
    labels = []
    for i in range(100):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        data.append([brightness, temperature, humidity])
        label = int(input("Enter optimal lighting level (0-100): "))
        labels.append(label)
        time.sleep(0.1)
    return np.array(data), np.array(labels)

data, labels = collect_data()

# Train the neural network
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)
mlp = MLPRegressor(hidden_layer_sizes=(10,), max_iter=1000)
mlp.fit(X_train, y_train)

try:
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        lighting_level = mlp.predict([[brightness, temperature, humidity]])[0]
        
        # Adjust LED lights
        if lighting_level > 50:
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
        
        # Adjust thermostat temperature
        try:
            if lighting_level > 50:
                requests.put(thermostat_api, json={"temperature": 22})
            else:
                requests.put(thermostat_api, json={"temperature": 25})
        except Exception as e:
            print(f"Error adjusting thermostat: {e}")
        
        cv2.imshow('Image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Exiting program")
finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()