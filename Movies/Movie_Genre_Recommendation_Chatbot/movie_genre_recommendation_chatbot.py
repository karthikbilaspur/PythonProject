import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import tkinter as tk
from tkinter import messagebox

# Load dataset (assuming a CSV file with 'plot' and 'genre' columns)
df = pd.read_csv('movie_plots.csv')

# Preprocess text data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t.lower() for t in tokens]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    return ' '.join(tokens)

df['plot'] = df['plot'].apply(preprocess_text)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['plot'], df['genre'], test_size=0.2, random_state=42)

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Build the model
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(5000,)))
model.add(Dropout(0.5))
model.add(Dense(len(set(df['genre'])), activation='softmax'))

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train_tfidf, y_train, epochs=10, batch_size=32, validation_data=(X_test_tfidf, y_test))

# Create a function to predict movie genre
def predict_genre(plot):
    plot = preprocess_text(plot)
    plot_tfidf = vectorizer.transform([plot])
    prediction = model.predict(plot_tfidf)
    return df['genre'].unique()[np.argmax(prediction)]

# Create a GUI function
def predict_and_display():
    plot = text_box.get("1.0", tk.END)
    if plot.strip() == "":
        messagebox.showerror("Error", "Please enter a movie plot.")
        return
    genre = predict_genre(plot)
    result_label.config(text=f"Predicted genre: {genre}")
    confidence = np.max(model.predict(vectorizer.transform([preprocess_text(plot)])))
    confidence_label.config(text=f"Confidence: {confidence*100:.2f}%")

def clear_text():
    text_box.delete("1.0", tk.END)
    result_label.config(text="")
    confidence_label.config(text="")

# Create the GUI window
window = tk.Tk()
window.title("Movie Genre Prediction Chatbot")

# Create the text box for user input
text_box = tk.Text(window, height=10, width=50)
text_box.pack(padx=10, pady=10)

# Create the predict button
button_frame = tk.Frame(window)
button_frame.pack(pady=10)
predict_button = tk.Button(button_frame, text="Predict Genre", command=predict_and_display)
predict_button.pack(side=tk.LEFT, padx=10)
clear_button = tk.Button(button_frame, text="Clear", command=clear_text)
clear_button.pack(side=tk.LEFT, padx=10)

# Create the result labels
result_frame = tk.Frame(window)
result_frame.pack(pady=10)
result_label = tk.Label(result_frame, text="")
result_label.pack()
confidence_label = tk.Label(result_frame, text="")
confidence_label.pack()

# Run the GUI event loop
window.mainloop()