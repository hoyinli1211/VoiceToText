import streamlit as st
import requests
import io
import os
import tempfile
import zipfile
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
from streamlit import cache

def download_and_extract_model(url, model_path):
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        zf.extractall(model_path)

@cache
def download_and_load_vosk_model(model_url, model_path):
    if not os.path.exists(model_path):
        os.makedirs(model_path)
        download_and_extract_model(model_url, model_path)
    return load_vosk_model(model_path)

def load_vosk_model(model_path="vosk-model-en"):
    model = Model(model_path)
    return model

def audio_file_to_text(audio_file, model):
    rec = KaldiRecognizer(model, 16000)

    with open(audio_file, 'rb') as audio:
        audio_data = audio.read()

    results = []
    for data in AudioSegment.from_file(io.BytesIO(audio_data)).raw_data:
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result())["text"])
        else:
            results.append(json.loads(rec.PartialResult())["partial"])

    text = " ".join(results)
    return text

def download_audio(url):
    response = requests.get(url)
    file = io.BytesIO(response.content)
    return file

def convert_audio_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file, format="mp3")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as converted_file:
        audio.export(converted_file.name, format="wav")
        return converted_file.name

def main():
    st.title("Audio Transcription App")

    # Download and load the Vosk model
    model_url = "https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip"
    with tempfile.TemporaryDirectory() as temp_dir:
        model_path = os.path.join(temp_dir, "vosk-model-en")
        vosk_model = download_and_load_vosk_model(model_url, model_path)

        option = st.selectbox("Choose the input source", ["Upload", "URL"], index=0)

        if option == "Upload":
            audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "flac"])
        else:
            url = st.text_input("Enter the audio file URL")
            audio_file = None
            if url:
                audio_file = download_audio(url)

        if audio_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_file.read())
                audio_file.seek(0)
                st.audio(temp_file.name)

            st.write("Transcribing audio file...")
            converted_audio_file = convert_audio_to_wav(audio_file)
            transcript = audio_file_to_text(converted_audio_file, vosk_model)
            st.write("Transcription:")
            st.write(transcript)

if __name__ == "__main__":
    main()
