import os
import openai

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Welcome to the ChatGPT terminal chatbot!")
    conversation_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        elif user_input.lower() == "clear":
            conversation_history = []
            print("Conversation history cleared.")
            continue
        response = chat_with_gpt(user_input)
        conversation_history.append({"user": user_input, "bot": response})
        print(f"Bot: {response}")
        print("\nConversation History:")
        for i, conv in enumerate(conversation_history):
            print(f"{i+1}. You: {conv['user']}")
            print(f"{i+1}. Bot: {conv['bot']}\n")

if __name__ == "__main__":
    main()