Overview
This project implements a simple chatbot using a pre-trained transformer model for intent classification and sentiment analysis. The chatbot can respond to basic greetings and goodbyes, and also provides sentiment analysis for user input.
Features
Intent Classification: Uses a pre-trained DistilBERT model to classify user input into intents (greeting or goodbye)
Sentiment Analysis: Uses the NLTK library's VADER sentiment analysis tool to analyze the sentiment of user input
Response Generation: Generates responses based on the classified intent
Customizable: Can be extended to support more intents and responses
Requirements
Python 3.x
transformers library (for pre-trained transformer models)
nltk library (for sentiment analysis and text processing)
torch library (for deep learning)
scikit-learn library (for data splitting)
Installation
Clone the repository
Install the required libraries: pip install transformers nltk torch scikit-learn
Download the NLTK data required for sentiment analysis: python -m nltk.downloader vader_lexicon
Usage
Run the chatbot: python chatbot.py
Interact with the chatbot by typing messages
Type 'quit' to exit the chatbot
Example Use Cases
User: "hi"
Bot: "Hello! How can I assist you today?"
Sentiment Analysis: "You seem to be in a positive mood!"
User: "bye"
Bot: "See you later! Have a great day!"
Sentiment Analysis: "You seem to be neutral."
