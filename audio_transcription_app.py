import os
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import requests
import io

# Set the paths to the FFmpeg and FFprobe executables
AudioSegment.converter = "/usr/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/bin/ffprobe"

def audio_file_to_text(audio_file):
    recognizer = sr.Recognizer()
    audio_segment = AudioSegment.from_file(audio_file)

    with audio_file as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        text = f"Could not request results from Google Speech Recognition service; {e}"

    return text

def download_audio(url):
    response = requests.get(url)
    file = io.BytesIO(response.content)
    return file

def main():
    st.title("Audio Transcription App")

    option = st.selectbox("Choose the input source", ["Upload", "URL"], index=0)

    if option == "Upload":
        audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "flac"])
    else:
        url = st.text_input("Enter the audio file URL")
        audio_file = None
        if url:
            audio_file = download_audio(url)

    if audio_file is not None:
        st.audio(audio_file)
        st.write("Transcribing audio file...")

        transcript = audio_file_to_text(audio_file)
        st.write("Transcription:")
        st.write(transcript)

if __name__ == "__main__":
    main()
