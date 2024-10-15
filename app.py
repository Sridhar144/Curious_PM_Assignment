
import streamlit as st
from openai import OpenAI

# Title and description
st.title("💬 Chatbot")
st.markdown(
    """
    This chatbot utilizes OpenAI's GPT-3.5 model for generating responses. 
    To get started, please provide your OpenAI API key. You can obtain it [here](https://platform.openai.com/account/api-keys). 
    For a step-by-step guide on building this app, check out our tutorial [here](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps).
    """
)

# Input for OpenAI API key
api_key = st.text_input("Enter your OpenAI API Key", type="password")

if not api_key:
    st.info("Please enter your OpenAI API key to continue.", icon="🗝️")
else:
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Initialize session state for chat messages
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input for chat
    user_input = st.chat_input("How can I assist you today?")
    if user_input:
        # Append user message to history and display
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Prepare messages for OpenAI API
        chat_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]

        # Generate response from OpenAI
        response_stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_messages,
            stream=True,
        )

        # Stream the response to the chat and append to history
        with st.chat_message("assistant"):
            assistant_response = st.write_stream(response_stream)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})