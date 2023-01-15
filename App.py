import streamlit as st
import speech_recognition as sr
import spacy
from spacy import displacy

spacy.cli.download("en_core_web_sm")

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    transcribed_text = recognizer.recognize_google(audio)
    return transcribed_text

def highlight_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    html = displacy.render(doc, style="ent")
    return html

def main():
    st.set_page_config(page_title="Transcribe Audio", page_icon=":microphone:", layout="wide")
    st.title("Transcribe Audio")

    uploaded_file = st.file_uploader("Upload your .wav file", type=["wav"])
    if uploaded_file is not None:
        transcribed_text = transcribe_audio(uploaded_file)
        entities_html = highlight_entities(transcribed_text)
        st.components.v1.html(entities_html)

if __name__ == "__main__":
    main()
