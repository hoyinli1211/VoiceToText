import streamlit as st
import requests
import io
import tempfile
from pydub import AudioSegment
import speech_recognition as sr

def download_audio(url):
    response = requests.get(url)
    file = io.BytesIO(response.content)
    return file

def convert_audio_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file, format="mp3")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as converted_file:
        audio.export(converted_file.name, format="wav")
        return converted_file.name

def transcribe_audio_sphinx(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_sphinx(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sphinx could not understand the audio."
    except sr.RequestError as e:
        return f"Sphinx error; {e}"

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
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_file.read())
            audio_file.seek(0)
            st.audio(temp_file.name)

        st.write("Transcribing audio file...")
        converted_audio_file = convert_audio_to_wav(audio_file)
        transcript = transcribe_audio_sphinx(converted_audio_file)
        st.write("Transcription:")
        st.write(transcript)

if __name__ == "__main__":
    main()
