import streamlit as st
import requests
import io
import audioread
import tempfile
from pydub import AudioSegment
import deepspeech

def load_deepspeech_model():
    model = deepspeech.Model(model_path="https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm", scorer_path="https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer")
    model.enableExternalScorer(scorer_path)
    return model

def audio_file_to_text(audio_file, model):
    with open(audio_file, "rb") as audio:
        audio_data = audio.read()

    text = model.stt(audio_data)
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

    # Load DeepSpeech model once
    deepspeech_model = load_deepspeech_model()

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
        transcript = audio_file_to_text(converted_audio_file, deepspeech_model)
        st.write("Transcription:")
        st.write(transcript)

if __name__ == "__main__":
    main()
