# chatbot.py

import random

# Define a dictionary with intents and responses
intents = {
    "greeting": {
        "patterns": ["hi", "hello", "hey", "greetings"],
        "responses": ["Hi there! How can I assist you today?", "Hello! What's on your mind?", "Hey, how's it going?"]
    },
    "goodbye": {
        "patterns": ["bye", "see you later", "goodbye"],
        "responses": ["See you later! Have a great day!", "Bye for now! Feel free to come back anytime.", "Goodbye! It was nice chatting with you."]
    },
    "help": {
        "patterns": ["help", "what can you do", "how can you assist me"],
        "responses": ["I can help you with a variety of tasks, such as answering questions, providing information, and chatting with you. What do you need help with?"]
    },
    "thanks": {
        "patterns": ["thanks", "thank you"],
        "responses": ["You're welcome! Is there anything else I can help you with?", "No problem! Feel free to ask me anything else."]
    }
}

# Define a function to match user input to intents
def match_intent(message):
    message = message.lower()
    for intent, values in intents.items():
        for pattern in values["patterns"]:
            if pattern in message:
                return intent
    return None

# Define a function to get a response based on the intent
def get_response(intent):
    if intent is not None:
        return random.choice(intents[intent]["responses"])
    else:
        return "Sorry, I didn't understand that. Can you please rephrase?"

# Define a chatbot function
def chatbot(message):
    intent = match_intent(message)
    response = get_response(intent)
    return response

# Define a main function to run the chatbot
def main():
    print("Welcome to the chatbot! Type 'quit' to exit.")
    while True:
        message = input("You: ")
        if message.lower() == "quit":
            break
        response = chatbot(message)
        print("Bot: ", response)

# Run the main function
if __name__ == "__main__":
    main()