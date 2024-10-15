# import streamlit as st
# import openai
# from google.cloud import speech_v1p1beta1 as speech
# from google.cloud import texttospeech
# from moviepy.editor import VideoFileClip, AudioFileClip
# import os

# # Set the Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mycreds.json"

# # Function to handle Google Speech-to-Text
# def transcribe_audio(file_path):
#     client = speech.SpeechClient()

#     with open(file_path, "rb") as audio_file:
#         content = audio_file.read()

#     audio = speech.RecognitionAudio(content=content)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         language_code="en-US",
#         model="default",
#         enable_automatic_punctuation=True,
#     )

#     response = client.recognize(config=config, audio=audio)

#     # Join the transcription into a single string
#     transcription = " ".join([result.alternatives[0].transcript for result in response.results])
#     return transcription

# # Function to correct transcription using GPT-4
# def correct_transcription_gpt4(transcription, api_key):
#     openai.api_key = api_key

#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": f"Please correct this transcription: {transcription}"}
#         ]
#     )
    
#     corrected_text = response['choices'][0]['message']['content']
#     return corrected_text

# # Function to convert text to speech using Google TTS
# def text_to_speech(corrected_text):
#     client = texttospeech.TextToSpeechClient()

#     synthesis_input = texttospeech.SynthesisInput(text=corrected_text)

#     # Select the voice (Wavenet voice model)
#     voice = texttospeech.VoiceSelectionParams(
#         language_code="en-US",
#         name="en-US-Wavenet-J",
#     )

#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.MP3
#     )

#     response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

#     output_audio_path = "output_audio.mp3"
#     with open(output_audio_path, "wb") as out:
#         out.write(response.audio_content)

#     return output_audio_path

# # Function to replace audio in video
# def replace_audio_in_video(video_path, new_audio_path):
#     video = VideoFileClip(video_path)
#     audio = AudioFileClip(new_audio_path)

#     final_video = video.set_audio(audio)
#     output_video_path = "final_output_video.mp4"
#     final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

#     return output_video_path

# # Streamlit App
# st.title("Video Audio Replacement with AI-Generated Voice")

# # File uploader
# video_file = st.file_uploader("Upload a video file", type=["mp4"])

# # Input for OpenAI API key
# api_key = st.text_input("Enter your OpenAI API Key", type="password")

# if video_file and api_key:
#     # Save uploaded video to disk
#     with open("uploaded_video.mp4", "wb") as f:
#         f.write(video_file.read())

#     # Extract audio and save to disk
#     video_clip = VideoFileClip("uploaded_video.mp4")
#     video_clip.audio.write_audiofile("extracted_audio.wav")

#     st.write("Transcribing audio using Google Speech-to-Text...")
#     transcription = transcribe_audio("extracted_audio.wav")
#     st.write("Original transcription:", transcription)

#     st.write("Correcting transcription using GPT-4...")
#     corrected_transcription = correct_transcription_gpt4(transcription, api_key)
#     st.write("Corrected transcription:", corrected_transcription)

#     st.write("Converting corrected transcription to speech using Google TTS...")
#     new_audio_path = text_to_speech(corrected_transcription)

#     st.write("Replacing audio in video...")
#     final_video_path = replace_audio_in_video("uploaded_video.mp4", new_audio_path)

#     st.video(final_video_path)
#     st.success("Process completed! You can download the video with replaced audio.")
# else:
#     st.info("Please upload a video file and provide your OpenAI API key to proceed.")
import os
import streamlit as st
import openai
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from moviepy.editor import VideoFileClip, AudioFileClip
import tempfile

# Set the Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mycreds.json"

# Function to handle Google Speech-to-Text
def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        model="default",
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    # Join the transcription into a single string
    transcription = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcription

# Function to correct transcription using GPT-4
def correct_transcription_gpt4(transcription, api_key):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please correct this transcription: {transcription}"}
        ]
    )
    
    corrected_text = response['choices'][0]['message']['content']
    return corrected_text

# Function to convert text to speech using Google TTS with voice gender selection
def text_to_speech(corrected_text, voice_gender):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=corrected_text)

    # Mapping voice gender selection to Google's SSML gender type
    gender_mapping = {
        "Male": texttospeech.SsmlVoiceGender.MALE,
        "Female": texttospeech.SsmlVoiceGender.FEMALE,
        "Neutral": texttospeech.SsmlVoiceGender.NEUTRAL
    }

    # Select the voice and set the language code
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=gender_mapping[voice_gender],
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    output_audio_path = "output_audio.mp3"
    with open(output_audio_path, "wb") as out:
        out.write(response.audio_content)

    return output_audio_path

# Function to replace audio in video
def replace_audio_in_video(video_path, new_audio_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(new_audio_path)

    final_video = video.set_audio(audio)
    output_video_path = "final_output_video.mp4"
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

    return output_video_path

# Streamlit App
st.title("Video Audio Replacement with AI-Generated Voice")

# File uploader for video
video_file = st.file_uploader("Upload a video file", type=["mp4"])

# Input for OpenAI API key
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Select voice gender for text-to-speech conversion
voice_gender = st.selectbox("Select voice gender:", ["Male", "Female", "Neutral"])

if video_file and api_key:
    # Save uploaded video to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as temp_video:
        temp_video.write(video_file.read())
        temp_video_path = temp_video.name

    # Extract audio from the video
    video_clip = VideoFileClip(temp_video_path)
    audio_file_path = "extracted_audio.wav"
    video_clip.audio.write_audiofile(audio_file_path)

    st.write("Transcribing audio using Google Speech-to-Text...")
    transcription = transcribe_audio(audio_file_path)
    st.write("Original transcription:", transcription)

    st.write("Correcting transcription using GPT-4...")
    corrected_transcription = correct_transcription_gpt4(transcription, api_key)
    st.write("Corrected transcription:", corrected_transcription)

    st.write(f"Converting corrected transcription to speech using Google TTS ({voice_gender} voice)...")
    new_audio_path = text_to_speech(corrected_transcription, voice_gender)

    st.write("Replacing audio in video...")
    final_video_path = replace_audio_in_video(temp_video_path, new_audio_path)

    st.video(final_video_path)
    st.success("Process completed! You can download the video with replaced audio.")
else:
    st.info("Please upload a video file and provide your OpenAI API key to proceed.")
