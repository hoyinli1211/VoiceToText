import os
import zipfile
import requests
import streamlit as st
import numpy as np
from pydub import AudioSegment
import deepspeech

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

    # Download and extract the DeepSpeech model if it's not already present
    model_url = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm"
    
    # Get the current working directory
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Create the 'models' directory if it doesn't exist
    MODELS_DIR = os.path.join(CURRENT_DIR, "models")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Set the model path and temporary zip file path
    model_path = os.path.join(MODELS_DIR, "deepspeech-model.pbmm")

    if not os.path.exists(model_path):
        st.write("Downloading DeepSpeech model...")
        zip_file_path = os.path.join(MODELS_DIR, "deepspeech-model.zip")
        download_file(model_url, zip_file_path)
        
        st.write("Extracting DeepSpeech model...")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(os.path.dirname(model_path))
        os.remove(zip_file_path)

    st.header("Upload Audio File")
    audio_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])

    if audio_file is not None:
        audio_bytes = audio_file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_file:
            tmp_audio_file.write(audio_bytes)
            transcription = transcribe_audio_deepspeech(tmp_audio_file.name, model_path)
            os.unlink(tmp_audio_file.name)

        st.header("Transcription")
        st.write(transcription)

if __name__ == "__main__":
    main()
