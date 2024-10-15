# import streamlit as st
# from openai import OpenAI

# # Show title and description.
# st.title("💬 Chatbot")
# st.write(
#     "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
#     "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
#     "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
# )

# # Ask user for their OpenAI API key via `st.text_input`.
# # Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# # via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
# else:

#     # Create an OpenAI client.
#     client = OpenAI(api_key=openai_api_key)

#     # Create a session state variable to store the chat messages. This ensures that the
#     # messages persist across reruns.
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display the existing chat messages via `st.chat_message`.
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Create a chat input field to allow the user to enter a message. This will display
#     # automatically at the bottom of the page.
#     if prompt := st.chat_input("What is up?"):

#         # Store and display the current prompt.
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         # Generate a response using the OpenAI API.
#         stream = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )

#         # Stream the response to the chat using `st.write_stream`, then store it in 
#         # session state.
#         with st.chat_message("assistant"):
#             response = st.write_stream(stream)
#         st.session_state.messages.append({"role": "assistant", "content": response})
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
