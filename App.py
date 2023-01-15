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
def generate_html(audio_src, text):
    return f"""
    <audio id="audio" src="{audio_src}" controls></audio>
    <p id="transcribed-text">{text}</p>
    <script>
        var audio = document.getElementById("audio");
        var transcribedText = document.getElementById("transcribed-text");
        var words = transcribedText.innerText.split(" ");
        var wordIndex = 0;

        var synth = window.speechSynthesis;
        var voices = synth.getVoices();
        var utterance = new SpeechSynthesisUtterance();
        utterance.voice = voices[0];
        utterance.pitch = 1;
        utterance.rate = 1;

        audio.addEventListener("timeupdate", function(){{
            var currentTime = audio.currentTime;
            while (wordIndex < words.length && words[wordIndex].end < currentTime) {{
                words[wordIndex].element.style.backgroundColor = "white";
                wordIndex++;
            }}
            if (wordIndex < words.length) {{
                words[wordIndex].element.style.backgroundColor = "yellow";
            }}
        }});

        audio.addEventListener("play", function(){{
            wordIndex = 0;
            utterance.text = transcribedText.innerText;
            synth.speak(utterance);
        }});

        audio.addEventListener("pause", function(){{
            synth.cancel();
        }});

        audio.addEventListener("ended", function(){{
            synth.cancel();
        }});

        transcribedText.innerHTML = words.map(function(word) {{
            var element = document.createElement("span");
            element.innerText = word;
            element.style.backgroundColor = "white";
            return element;
        }});
    </script>
    """

def main():
    st.set_page_config(page_title="Transcribe Audio", page_icon=":microphone:", layout="wide")
    st.title("Transcribe Audio")

    uploaded_file = st.file_uploader("Upload your .wav file", type=["wav"])
    if uploaded_file is not None:
        transcribed_text = transcribe_audio(uploaded_file)
        entities_html = highlight_entities(transcribed_text)
        st.components.v1.html(generate_html(entities_html), height=2000, scrolling=True

if __name__ == "__main__":
    main()
