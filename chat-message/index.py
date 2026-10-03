import os
import streamlit as st
from openai import OpenAI

# Load client - set OPENAI_API_KEY in env or st.secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_response(prompt, history, model="gpt-3.5-turbo"):
    try:
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        # Add past conversation for context
        for conv in history:
            messages.append({"role": "user", "content": conv["user"]})
            messages.append({"role": "assistant", "content": conv["bot"]})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.set_page_config(page_title="Advanced Streamlit Chatbot")
    st.title("Advanced Streamlit Chatbot")
    st.subheader("Ask me anything!")

    # Init session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Sidebar controls - from terminal version's extra commands
    with st.sidebar:
        model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"])
        if st.button("Clear History"):
            st.session_state.conversation = []
            st.rerun()
        st.write(f"Messages: {len(st.session_state.conversation)}")

    # Display history using chat UI
    for conv in st.session_state.conversation:
        with st.chat_message("user"):
            st.write(conv["user"])
        with st.chat_message("assistant"):
            st.write(conv["bot"])

    # Chat input - better than text_input + button
    user_input = st.chat_input("You:")

    if user_input:
        if user_input.lower() == "clear":
            st.session_state.conversation = []
            st.rerun()
        elif user_input.lower() == "quit":
            st.info("To quit, just close the tab. Clearing history...")
            st.session_state.conversation = []
            st.rerun()
        else:
            # Show user message immediately
            with st.chat_message("user"):
                st.write(user_input)

            # Get response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    chatbot_response = get_openai_response(user_input, st.session_state.conversation, model=model)
                st.write(chatbot_response)

            # Save to history
            st.session_state.conversation.append({"user": user_input, "bot": chatbot_response})

if __name__ == "__main__":
    main()