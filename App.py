import streamlit as st
import streamlit_webrtc as webrtc
import speech_recognition as sr
import spacy
from spacy import displacy
import base64

spacy.cli.download("en_core_web_sm")

#grant permission to use microphone
def create_audio_stream():
    return webrtc.webrtc_streamer(
        key="audio",
        audio=True,
        video=False,
        facing_mode="user",
        height=0,
        width=0,
    )

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
    <div>
        <button id="play-button" onclick="play()">Play</button>
        <button id="copy-button" onclick="copyToClipboard()">Copy</button>
    </div>
    <script>
        var audio = document.getElementById("audio");
        var transcribedText = document.getElementById("transcribed-text");
        var words = transcribedText.innerText.split(" ");
        var wordIndex = 0;
        
        function play(){{
            audio.play();
        }}

        function copyToClipboard() {{
            var copyText = document.getElementById("entities");
            navigator.clipboard.writeText(copyText.innerHTML).then(
                function() {{
                    console.log("Text copied to clipboard");
                }},
                function(err) {{
                    console.error("Could not copy text: ", err);
                }}
            );
        }}
    </script>
    """

def main():
    st.set_page_config(page_title="Transcribe Audio", page_icon=":microphone:", layout="wide")
    st.title("Transcribe Audio")

    uploaded_file = st.file_uploader("Upload your .wav file", type=["wav"])
    if uploaded_file is not None:
        transcribed_text = transcribe_audio(uploaded_file)
        entities_html = highlight_entities(transcribed_text)
        
        uploaded_file.seek(0)
        audio_src = "data:audio/wav;base64," + base64.b64encode(uploaded_file.read()).decode()
        
        html = generate_html(audio_src, entities_html)
        st.components.v1.html(html, height=300)

    stream = create_audio_stream()
    if stream:
        st.audio(stream)

if __name__ == "__main__":
    main()
