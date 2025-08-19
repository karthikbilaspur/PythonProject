import tkinter as tk
from tkinter import scrolledtext
import spacy

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

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

# Create GUI
root = tk.Tk()
root.title("Document Word Detection")

input_label = tk.Label(root, text="Input Text:")
input_label.pack()

input_text = scrolledtext.ScrolledText(root, width=80, height=10)
input_text.pack()

analyze_button = tk.Button(root, text="Analyze Document", command=analyze_document)
analyze_button.pack()

count_button = tk.Button(root, text="Count Words", command=count_document_words)
count_button.pack()

output_label = tk.Label(root, text="Output:")
output_label.pack()

output_text = scrolledtext.ScrolledText(root, width=80, height=15)
output_text.pack()

root.mainloop()