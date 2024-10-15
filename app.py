# import streamlit as st
# import openai

# # Title and description
# st.title("💬 Chatbot")
# st.markdown(
#     """
#     This chatbot utilizes OpenAI's GPT-4 model via Azure's OpenAI service. 
#     To get started, please provide your Azure OpenAI API key and Endpoint. 
#     You can find these details in your Azure OpenAI service portal.
#     """
# )

# # Input for Azure OpenAI API key and Endpoint
# api_key = st.text_input("Enter your Azure OpenAI API Key", type="password")
# api_base = st.text_input("Enter your Azure OpenAI Endpoint (e.g., https://<your-resource-name>.openai.azure.com)")

# if not api_key or not api_base:
#     st.info("Please enter both your API key and API base URL to continue.", icon="🗝️")
# else:
#     # Set the API key and base URL for Azure
#     openai.api_key = api_key
#     openai.api_base = api_base  # e.g., 'https://<your-resource-name>.openai.azure.com'
#     openai.api_type = 'azure'
#     openai.api_version = '2023-03-15-preview'  # Make sure to use the correct API version for your model

#     # Initialize session state for chat messages
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     # Display chat messages
#     for msg in st.session_state.chat_history:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # User input for chat
#     user_input = st.chat_input("How can I assist you today?")
#     if user_input:
#         # Append user message to history and display
#         st.session_state.chat_history.append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.markdown(user_input)

#         # Prepare messages for OpenAI API
#         chat_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]

#         # Generate response from Azure OpenAI
#         response = openai.ChatCompletion.create(
#             engine="gpt-4",  # The engine/model deployed in your Azure OpenAI service
#             messages=chat_messages,
#         )

#         # Extract assistant response
#         assistant_response = response['choices'][0]['message']['content']

#         # Append assistant response to chat history and display
#         st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
#         with st.chat_message("assistant"):
#             st.markdown(assistant_response)
import streamlit as st
import openai

# Title and description
st.title("💬 Chatbot")
st.markdown(
    """
    This chatbot utilizes Azure's OpenAI GPT-4o model for generating responses.
    Please provide your Azure OpenAI API key and endpoint to get started.
    """
)

# Input for Azure OpenAI API key and Endpoint
api_key = st.text_input("Enter your Azure OpenAI API Key", type="password")
api_base = st.text_input("Enter your Azure OpenAI Endpoint (e.g., https://<your-resource-name>.openai.azure.com)")
deployment_name = st.text_input("Enter your Azure OpenAI Deployment Name (e.g., gpt-4o)")

if not api_key or not api_base or not deployment_name:
    st.info("Please enter your API key, base URL, and deployment name to continue.", icon="🗝️")
else:
    # Set the API key and base URL for Azure
    openai.api_key = api_key
    openai.api_base = api_base  # e.g., 'https://<your-resource-name>.openai.azure.com'
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'  # Ensure to use the correct version

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

        # Prepare messages for Azure OpenAI API
        chat_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]

        # Generate response from Azure OpenAI
        try:
            response = openai.ChatCompletion.create(
                engine=deployment_name,  # The deployment name for your Azure OpenAI resource
                messages=chat_messages,
                max_tokens=150,  # You can adjust the token limit based on your needs
            )

            # Extract assistant response
            assistant_response = response['choices'][0]['message']['content']

            # Append assistant response to chat history and display
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            with st.chat_message("assistant"):
                st.markdown(assistant_response)

        except openai.error.InvalidRequestError as e:
            st.error(f"Invalid request: {str(e)}")
        except openai.error.AuthenticationError as e:
            st.error("Authentication failed. Please check your API key.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
