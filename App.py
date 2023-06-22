import streamlit as st
import speech_recognition as sr
import requests
import io
import audioread
import tempfile

def audio_file_to_text(audio_file):
    recognizer = sr.Recognizer()

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
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_file.read())
            audio_file.seek(0)
            st.audio(temp_file.name)

        st.write("Transcribing audio file...")
        transcript = audio_file_to_text(audio_file)
        st.write("Transcription:")
        st.write(transcript)

if __name__ == "__main__":
    main()
