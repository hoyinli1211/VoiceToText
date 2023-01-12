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

def generate_html(text):
    return f"""
    <button onclick="copyText()">Copy Text</button>
    <div id="highlighted-text">{text}</div>
    <script>
        function copyText() {{
            // Get the text with NER highlighted
            var text = document.getElementById("highlighted-text").innerText;
            // Create a temporary textarea element
            var textArea = document.createElement("textarea");
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            // Copy the text to the clipboard
            document.execCommand("copy");
            // Remove the temporary textarea element
            document.body.removeChild(textArea);
        }}
    </script>
    """

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
