import streamlit as st
from pydub import AudioSegment

def get_audio_duration(audio_file):
    audio = AudioSegment.from_file(audio_file)
    return audio.duration_seconds

def main():
    st.title("Audio File Information App")

    audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "flac"])

    if audio_file is not None:
        st.audio(audio_file)
        duration = get_audio_duration(audio_file)
        st.write(f"Audio duration: {duration:.2f} seconds")

if __name__ == "__main__":
    main()
