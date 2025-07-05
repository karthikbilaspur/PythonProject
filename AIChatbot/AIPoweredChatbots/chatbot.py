# Import necessary libraries
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Define a dataset of intents and responses
intents = {
    "greeting": [
        {"text": "hi", "response": "Hello! How can I assist you today?"},
        {"text": "hello", "response": "Hi there! What's on your mind?"},
        {"text": "hey", "response": "Hey, how's it going?"}
    ],
    "goodbye": [
        {"text": "bye", "response": "See you later! Have a great day!"},
        {"text": "see you later", "response": "Bye for now! Feel free to come back anytime."},
        {"text": "goodbye", "response": "Goodbye! It was nice chatting with you."}
    ]
}

# Add more data to the dataset
for i in range(100):
    intents["greeting"].append({"text": f"hi {i}", "response": "Hello! How can I assist you today?"})
    intents["goodbye"].append({"text": f"bye {i}", "response": "See you later! Have a great day!"})

# Preprocess the data
lemmatizer = WordNetLemmatizer()
texts = []
labels = []
for intent, values in intents.items():
    for value in values:
        text = value["text"]
        label = intent
        texts.append(text)
        labels.append(label)

# Use a pre-trained transformer model for classification
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# Prepare the data for the transformer model
input_ids = []
attention_masks = []
for text in texts:
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=512,
        return_attention_mask=True,
        return_tensors='pt',
        truncation=True,
        padding='max_length'
    )
    input_ids.append(inputs['input_ids'])
    attention_masks.append(inputs['attention_mask'])

input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)
labels = torch.tensor([0 if label == "greeting" else 1 for label in labels])

# Split the data into training and testing sets
train_inputs, validation_inputs, train_labels, validation_labels = train_test_split(input_ids, labels, random_state=42, test_size=0.2)
train_masks, validation_masks, _, _ = train_test_split(attention_masks, labels, random_state=42, test_size=0.2)

# Train the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
train_inputs, train_labels, train_masks = train_inputs.to(device), train_labels.to(device), train_masks.to(device)
validation_inputs, validation_labels, validation_masks = validation_inputs.to(device), validation_labels.to(device), validation_masks.to(device)

# Define a function to get a response based on the user's input
def get_response(text):
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=512,
        return_attention_mask=True,
        return_tensors='pt',
        truncation=True,
        padding='max_length'
    )
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    outputs = model(input_ids, attention_mask=attention_mask)
    logits = outputs.logits
    intent = torch.argmax(F.softmax(logits, dim=1)).item()
    if intent == 0:
        return "Hello! How can I assist you today?"
    else:
        return "See you later! Have a great day!"

# Define a function to analyze the sentiment of the user's input
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    if sentiment['compound'] > 0.05:
        return "You seem to be in a positive mood!"
    elif sentiment['compound'] < -0.05:
        return "You seem to be in a negative mood."
    else:
        return "You seem to be neutral."

# Define a main function to run the chatbot
def main():
    print("Welcome to the chatbot! Type 'quit' to exit.")
    while True:
        text = input("You: ")
        if text.lower() == "quit":
            break
        response = get_response(text)
        sentiment = analyze_sentiment(text)
        print("Bot:", response)
        print("Sentiment Analysis:", sentiment)

# Run the main function
if __name__ == "__main__":
    main()