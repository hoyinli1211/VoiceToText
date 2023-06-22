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
        media_stream_constraints={
            "audio": True,
            "video": False,
        }
    )

st.title("Microphone Stream")

stream = create_audio_stream()
if stream:
    st.audio(stream)

