import os
import requests
import streamlit as st
import numpy as np
from pydub import AudioSegment
import deepspeech
import tempfile

def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, "wb") as outfile:
        outfile.write(response.content)

def transcribe_audio_deepspeech(audio_file, model_file):
    model = deepspeech.Model(model_file)
    audio = AudioSegment.from_file(audio_file).set_frame_rate(16000).set_channels(1)
    audio_data = np.frombuffer(audio.raw_data, dtype=np.int16)
    text = model.stt(audio_data)
    return text

def main():
    st.title("Audio Transcription App with DeepSpeech")

    # Get the current working directory
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Create the 'models' directory if it doesn't exist
    MODELS_DIR = os.path.join(CURRENT_DIR, "models")
    os.makedirs(MODELS_DIR, exist_ok=True)

    # Set the model path
    model_path = os.path.join(MODELS_DIR, "deepspeech-model.pbmm")

    # Download the DeepSpeech model if it's not already present
    model_url = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm"
    
    if not os.path.exists(model_path):
        st.write("Downloading DeepSpeech model...")
        download_file(model_url, model_path)

    st.header("Upload Audio File")
    audio_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])

    if audio_file is not None:
        audio_bytes = audio_file.read()

        # Display audio player
        st.header("Audio Player")
        st.audio(audio_bytes, format="audio/wav")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_file:
            tmp_audio_file.write(audio_bytes)
            transcription = transcribe_audio_deepspeech(tmp_audio_file.name, model_path)
            os.unlink(tmp_audio_file.name)

        st.header("Transcription")
        st.write(transcription)

if __name__ == "__main__":
    main()
