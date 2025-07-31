import os
import streamlit as st
import openai

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(user_input, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Advanced Streamlit Chatbot")
    st.subheader("Ask me anything!")

    # Session state to store conversation history
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    user_input = st.text_input("You:", key="user_input")
    if st.button("Submit"):
        chatbot_response = get_openai_response(user_input)
        st.session_state.conversation.append({"user": user_input, "bot": chatbot_response})

    # Display conversation history
    conversation_history = st.session_state.conversation
    for conv in conversation_history:
        st.write(f"You: {conv['user']}")
        st.write(f"Bot: {conv['bot']}")

if __name__ == "__main__":
    main()