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

st.title("Microphone Stream")

stream = create_audio_stream()
if stream:
    st.audio(stream)

