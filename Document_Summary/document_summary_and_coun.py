import tkinter as tk
from tkinter import scrolledtext
import spacy
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict
import nltk

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Initialize NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def detect_document_words(text):
    # Process text using spaCy
    doc = nlp(text)

    # Detect words
    words = []
    for token in doc:
        if not token.is_punct and not token.is_space:
            words.append(token.text)

    # Detect entities
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    # Detect nouns
    nouns = []
    for token in doc:
        if token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
            nouns.append(token.text)

    return words, entities, nouns

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

def analyze_document():
    text = input_text.get('1.0', tk.END)
    words, entities, nouns = detect_document_words(text)

    output_text.delete('1.0', tk.END)
    output_text.insert('1.0', "Words:\n")
    output_text.insert(tk.END, ', '.join(words[:100]) + '\n\n')

    output_text.insert(tk.END, "Entities:\n")
    for entity in entities:
        output_text.insert(tk.END, f"{entity[0]} ({entity[1]})\n")

    output_text.insert(tk.END, "\nNouns:\n")
    output_text.insert(tk.END, ', '.join(nouns[:100]))

def count_document_words():
    text = input_text.get('1.0', tk.END)
    words, _, _ = detect_document_words(text)
    word_count = len(words)
    output_text.delete('1.0', tk.END)
    output_text.insert('1.0', f"Word Count: {word_count}")

def generate_summary():
    text = input_text.get('1.0', tk.END)
    summary = summarize_document(text)
    output_text.delete('1.0', tk.END)
    output_text.insert('1.0', "Summary:\n" + summary)

# Create GUI
root = tk.Tk()
root.title("Document Analyzer")

input_label = tk.Label(root, text="Input Text:")
input_label.pack()

input_text = scrolledtext.ScrolledText(root, width=80, height=10)
input_text.pack()

button_frame = tk.Frame(root)
button_frame.pack()

analyze_button = tk.Button(button_frame, text="Analyze Document", command=analyze_document)
analyze_button.pack(side=tk.LEFT)

count_button = tk.Button(button_frame, text="Count Words", command=count_document_words)
count_button.pack(side=tk.LEFT)

generate_button = tk.Button(button_frame, text="Generate Summary", command=generate_summary)
generate_button.pack(side=tk.LEFT)

output_label = tk.Label(root, text="Output:")
output_label.pack()

output_text = scrolledtext.ScrolledText(root, width=80, height=15)
output_text.pack()

root.mainloop()