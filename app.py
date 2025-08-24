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
import streamlit as st
import os
import requests
import moviepy.editor as mp
from gtts import gTTS
import whisper
import os
import subprocess

def check_ffmpeg():
    try:
        ffmpeg_path = subprocess.check_output(['which', 'ffmpeg']).decode('utf-8').strip()
        st.write(f"ffmpeg is installed at: {ffmpeg_path}")
    except subprocess.CalledProcessError:
        st.write("ffmpeg is not installed or not found.")


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():

    st.set_page_config(layout="wide")
    st.subheader("Checking ffmpeg Installation:")
    # check_ffmpeg()
    st.title("Welcome to Sridhar's work")
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

    public_dir = "public"
    input_dir = os.path.join(public_dir, "input")
    output_dir = os.path.join(public_dir, "output")
    
    ensure_directory(public_dir)
    ensure_directory(input_dir)
    ensure_directory(output_dir)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Upload your video file for video adjustment, audio separation and AI voice generation and Preview the magic!")
        video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
        serial_number = len(os.listdir(input_dir)) + 1

        if video_file is not None:
            input_video_path = os.path.join(input_dir, f"input{serial_number}.mp4")
            with open(input_video_path, "wb") as f:
                f.write(video_file.read())
            st.video(input_video_path)

    if video_file is not None:
        with col2:
            st.header("Processing Outputs")
            audio_col1, audio_col2 = st.columns(2)
            audio_clip = mp.VideoFileClip(input_video_path).audio
            audio_path = os.path.join(output_dir, f"audio{serial_number}.mp3")
            audio_clip.write_audiofile(audio_path)
            audio_col1.audio(audio_path, format='audio/mp3')
            with open(audio_path, 'rb') as f:
                audio_col1.download_button("Download Original Audio", f, file_name=f"audio{serial_number}.mp3")

            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            transcribed_text = result["text"]

            text_col1, text_col2 = st.columns(2)
            with st.container():
                text_col1.text_area("Original Transcribed Text", transcribed_text, height=200)
                transcribed_text_path = os.path.join(output_dir, f"transcription{serial_number}.txt")
                with open(transcribed_text_path, "w") as f:
                    f.write(transcribed_text)
                with open(transcribed_text_path, 'rb') as f:
                    text_col1.download_button("Download Original Text", f, file_name=f"transcription{serial_number}.txt")

                azure_openai_key = "22ec84421ec24230a3638d1b51e3a7dc"
                azure_openai_endpoint = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
                headers = {"Content-Type": "application/json", "api-key": azure_openai_key}
                prompt = f"Rewrite only corrected grammar: {transcribed_text}"
                data = {"messages": [{"role": "user", "content": prompt}], "max_tokens": 500}
                response = requests.post(azure_openai_endpoint, headers=headers, json=data)

                if response.status_code == 200:
                    corrected_text = response.json()["choices"][0]["message"]["content"].strip()
                    text_col2.text_area("Corrected Text", corrected_text, height=200)
                    corrected_text_path = os.path.join(output_dir, f"corrected_text{serial_number}.txt")
                    with open(corrected_text_path, "w") as f:
                        f.write(corrected_text)
                    with open(corrected_text_path, 'rb') as f:
                        text_col2.download_button("Download Corrected Text", f, file_name=f"corrected_text{serial_number}.txt")

                    corrected_audio_path = os.path.join(output_dir, f"corrected_audio{serial_number}.mp3")
                    tts = gTTS(corrected_text)
                    tts.save(corrected_audio_path)

                    original_duration = mp.AudioFileClip(audio_path).duration
                    corrected_audio_clip = mp.AudioFileClip(corrected_audio_path)
                    adjusted_audio = corrected_audio_clip.fx(mp.vfx.speedx, corrected_audio_clip.duration / original_duration)
                    adjusted_audio_path = os.path.join(output_dir, f"adjusted_audio{serial_number}.mp3")
                    adjusted_audio.write_audiofile(adjusted_audio_path)

                    audio_col2.audio(adjusted_audio_path, format='audio/mp3')
                    with open(adjusted_audio_path, 'rb') as f:
                        audio_col2.download_button("Download Adjusted Audio", f, file_name=f"adjusted_audio{serial_number}.mp3")

                    video_col1, video_col2 = st.columns(2)
                    video_no_audio_path = os.path.join(output_dir, f"video_no_audio{serial_number}.mp4")
                    video_no_audio = mp.VideoFileClip(input_video_path).without_audio()
                    video_no_audio.write_videofile(video_no_audio_path)
                    video_col1.video(video_no_audio_path)
                    with open(video_no_audio_path, 'rb') as f:
                        video_col1.download_button("Download Video without Audio", f, file_name=f"video_no_audio{serial_number}.mp4")

                    final_video_path = os.path.join(output_dir, f"final_video{serial_number}.mp4")
                    final_audio_clip = mp.AudioFileClip(adjusted_audio_path)
                    final_video = video_no_audio.set_audio(final_audio_clip)
                    final_video.write_videofile(final_video_path)
                    video_col2.video(final_video_path)
                    with open(final_video_path, 'rb') as f:
                        video_col2.download_button("Download Final Video", f, file_name=f"final_video{serial_number}.mp4")

                else:
                    st.error(f"Failed to connect to Azure OpenAI: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()
