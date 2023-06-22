import streamlit as st
from pytranscriber import Transcriber

def transcribe_audio(audio_file):
    transcriber = Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript

def main():
    st.title("Audio Transcription App")
    
    audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "flac"])
    
    if audio_file is not None:
        st.write("Transcribing audio...")
        transcript = transcribe_audio(audio_file)
        st.write("Transcription completed!")
        st.text_area("Transcript", transcript, height=200)

if __name__ == "__main__":
    main()
