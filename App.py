import streamlit as st
import speech_recognition as sr

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    transcribed_text = recognizer.recognize_google(audio)
    return transcribed_text

def main():
    st.set_page_config(page_title="Transcribe Audio", page_icon=":microphone:", layout="wide")
    st.title("Transcribe Audio")

    file = st.file_uploader("Upload a .wav file", type=["wav"])
    if file:
        transcribed_text = transcribe_audio(file)
        st.write("Transcribed Text: ", transcribed_text)

if __name__ == "__main__":
    main()
