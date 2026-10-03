# Advanced Streamlit Chatbot

A simple ChatGPT-powered chatbot built with Streamlit. Combines a clean web UI with conversation history management.

### Features
- 💬 Interactive chat UI with `st.chat_message`
- 🧠 Context-aware - sends full conversation history to the model
- 🧹 Clear history via button or typing `clear`
- ⚙️ Model selector (gpt-3.5-turbo, gpt-4o-mini, gpt-4o)
- 🔒 API key loaded from environment variables

### Tech Stack
- Python
- Streamlit
- OpenAI API (>=1.0)

### Installation

1. Clone the repo:
```bash
git clone https://github.com/yourusername/streamlit-chatbot.git
cd streamlit-chatbot