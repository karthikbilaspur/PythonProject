import tkinter as tk
from tkinter import scrolledtext
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict

# Initialize NLTK data
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def summarize_document(text, ratio=0.2):
    # Tokenize sentences
    sentences = sent_tokenize(text)

    # Calculate word frequencies
    word_freq = defaultdict(int)
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    for sentence in sentences:
        words = nltk.word_tokenize(sentence.lower())
        for word in words:
            if word not in stop_words:
                word_freq[stemmer.stem(word)] += 1

    # Calculate sentence scores
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence.lower())
        for word in words:
            if word not in stop_words:
                sentence_scores[sentence] += word_freq[stemmer.stem(word)]

    # Sort sentences by score and select top-scoring sentences
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    num_sentences = int(len(sentences) * ratio)
    top_sentences = sorted_sentences[:num_sentences]

    # Return summarized text
    summary = ' '.join([sentence[0] for sentence in top_sentences])
    return summary

def generate_summary():
    text = input_text.get('1.0', tk.END)
    summary = summarize_document(text)
    output_text.delete('1.0', tk.END)
    output_text.insert('1.0', summary)

# Create GUI
root = tk.Tk()
root.title("Document Summary Generator")

input_label = tk.Label(root, text="Input Text:")
input_label.pack()

input_text = scrolledtext.ScrolledText(root, width=80, height=10)
input_text.pack()

generate_button = tk.Button(root, text="Generate Summary", command=generate_summary)
generate_button.pack()

output_label = tk.Label(root, text="Summary:")
output_label.pack()

output_text = scrolledtext.ScrolledText(root, width=80, height=5)
output_text.pack()

root.mainloop()