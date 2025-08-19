import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Load the MNIST dataset
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

# Normalize the pixel values
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255

# Define the model architecture
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test))

# Create a Tkinter window
window = tk.Tk()
window.title("AI Drawing Game")

# Create a canvas for drawing
canvas = tk.Canvas(window, width=280, height=280)
canvas.pack()

# Create a variable to store the drawing
drawing = []

# Define a function to handle mouse events
def draw(event):
    x, y = event.x, event.y
    drawing.append((x, y))
    canvas.create_oval(x-2, y-2, x+2, y+2, fill='black')

# Bind the mouse events to the canvas
canvas.bind('<B1-Motion>', draw)

# Define a function to guess the drawing
def guess():
    # Create a new image
    img = Image.new('L', (280, 280), color=255)
    draw = ImageDraw.Draw(img)
    for x, y in drawing:
        draw.ellipse([(x-2, y-2), (x+2, y+2)], fill=0)

    # Resize the image to 28x28
    img = img.resize((28, 28))

    # Convert the image to a numpy array
    img_array = np.array(img) / 255

    # Make a prediction
    prediction = model.predict(img_array.reshape((1, 28, 28)))

    # Show the result
    result = np.argmax(prediction)
    messagebox.showinfo("Result", f"I think you drew a: {result}")

# Create a button to guess the drawing
guess_button = tk.Button(window, text="Guess", command=guess)
guess_button.pack()

# Create a button to clear the drawing
def clear():
    global drawing
    drawing = []
    canvas.delete("all")

clear_button = tk.Button(window, text="Clear", command=clear)
clear_button.pack()

# Start the Tkinter event loop
window.mainloop()