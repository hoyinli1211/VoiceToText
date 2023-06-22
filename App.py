import streamlit as st
import pytranscriber as pt

# Define the Streamlit app
def app():
    st.title("Audio Transcription")

    # Upload the audio file
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if audio_file is not None:
        # Display the uploaded audio file
        st.audio(audio_file, format='audio/mp3')

        # Create the PyTranscriber object
        transcriber = pt.Transcriber()

        # Transcribe the audio file
        transcript = transcriber.transcribe(audio_file)

        # Display the transcript
        st.write("Transcript:")
        st.write(transcript)

# Run the Streamlit app
if __name__ == '__main__':
    app()
