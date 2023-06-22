import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment

def audio_file_to_text(audio_file):
    recognizer = sr.Recognizer()
    audio_segment = AudioSegment.from_file(audio_file)

    with audio_file as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        text = f"Could not request results from Google Speech Recognition service; {e}"

    return text

def main():
    st.title("Audio Transcription App")

    audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg", "flac"])

    if audio_file is not None:
        st.audio(audio_file)
        st.write("Transcribing audio file...")

        transcript = audio_file_to_text(audio_file)
        st.write("Transcription:")
        st.write(transcript)

if __name__ == "__main__":
    main()
