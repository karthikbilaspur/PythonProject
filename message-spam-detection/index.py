import tkinter as tk
from tkinter import messagebox
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

# Training data
messages = [
    ("You won a prize! Click here to claim!", 1),
    ("Get free cash now!", 1),
    ("I love this product!", 0),
    ("This is a great opportunity!", 0),
    ("You have won a free trip!", 1),
    ("This product is amazing!", 0),
    ("Click here to win a prize!", 1),
    ("I'm so excited about this!", 0),
    ("You are a winner!", 1),
    ("This is the best product ever!", 0)
]

# Vectorize the messages
vectorizer = CountVectorizer()
X = vectorizer.fit_transform([msg[0] for msg in messages])
y = np.array([msg[1] for msg in messages])

# Train the model
model = MultinomialNB()
model.fit(X, y)

def detect_spam(message):
    message_vector = vectorizer.transform([message])
    prediction = model.predict(message_vector)
    return prediction[0]

def check_message():
    message = message_entry.get("1.0", "end-1c")
    if detect_spam(message) == 1:
        result_label.config(text="Spam detected!", fg="red")
    else:
        result_label.config(text="Not spam", fg="green")

root = tk.Tk()
root.title("Spam Detection")

message_label = tk.Label(root, text="Enter a message:")
message_label.pack()

message_entry = tk.Text(root, height=10, width=40)
message_entry.pack()

check_button = tk.Button(root, text="Check for spam", command=check_message)
check_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()