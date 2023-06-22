import streamlit as st
import streamlit_webrtc as webrtc

# grant permission to use microphone
def create_audio_stream():
    return webrtc.webrtc_streamer(
        key="audio",
        audio=True,
        video=False,
        height=300,
        width=400,
        on_audio_data=get_audio_data,
        detection_interval=500,
        async_processing=True,
    )

def get_audio_data(audio_data):
    st.session_state.audio_data.append(audio_data)

def playback_audio():
    if st.session_state.audio_data:
        audio_data = b''.join(st.session_state.audio_data)
        st.audio(audio_data, format="audio/wav")

st.title("Microphone Stream")

if "audio_data" not in st.session_state:
    st.session_state.audio_data = []

stream = create_audio_stream()
if stream:
    st.button("Start Recording")
    if st.button("Stop Recording"):
        st.stop()
        playback_audio()
