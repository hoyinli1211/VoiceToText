import streamlit as st
import speech_recognition as sr
import spacy
from spacy import displacy

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

    file = st.file_uploader("Upload a .wav file", type=["wav"])
    if file:
        transcribed_text = transcribe_audio(file)
        entities_html = highlight_entities(transcribed_text)
        st.write("Transcribed Text: ",transcribed_text)
        st.write("Entities: ", unsafe_allow_html=True)
        st.write(entities_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
