import random
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import requests

# Define a dictionary of intents and responses
intents = {
    "greeting": ["Hello! How can I assist you today?", "Hi there! What's on your mind?", "Hey, how's it going?"],
    "product": ["What product are you inquiring about?", "Can you please provide more information about the product?"],
    "issue": ["Sorry to hear that you're experiencing issues. Can you please describe the problem?", "I'd be happy to help you with your issue. Can you please provide more details?"],
    "solution": ["Have you tried restarting the product?", "Have you checked for any software updates?"],
    "escalation": ["I'd be happy to escalate your issue to our technical support team. Can you please provide your contact information?", "I'm going to escalate your issue to our technical support team. They will be in touch with you shortly."]
}

# Define a function to preprocess the user's input
def preprocess_input(input_text):
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(input_text)
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return " ".join(tokens)

# Define a function to classify the user's input
def classify_input(input_text):
    vectorizer = TfidfVectorizer()
    train_data = ["hello", "product", "issue", "solution", "escalation"]
    train_labels = [0, 1, 2, 3, 4]
    vectorizer.fit(train_data)
    input("Enter your input: ")
    vector = vectorizer.transform([input_text])
    model = MultinomialNB()
    model.fit(vectorizer.transform(train_data), train_labels)
    prediction = model.predict(vector)
    return prediction[0]

# Define a function to respond to user input
def respond_to_input(input_text):
    input_text = preprocess_input(input_text)
    prediction = classify_input(input_text)
    if prediction == 0:
        return random.choice(intents["greeting"])
    elif prediction == 1:
        return random.choice(intents["product"])
    elif prediction == 2:
        return random.choice(intents["issue"])
    elif prediction == 3:
        return random.choice(intents["solution"])
    elif prediction == 4:
        return random.choice(intents["escalation"])
    else:
        return "I didn't understand that. Can you please rephrase?"

# Define a function to escalate issues to technical support
def escalate_issue(issue):
    url = "https://example.com/technical-support"
    response = requests.post(url, json={"issue": issue})
    return response.json()

# Define a main function to run the chatbot
def main():
    print("Welcome to our customer support chatbot! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = respond_to_input(user_input)
        print("Bot:", response)
        if "escalate" in response:
            issue = user_input
            escalate_issue(issue)

# Run the main function
if __name__ == "__main__":
    main()