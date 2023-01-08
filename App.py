import streamlit as st
import speech_recognition as sr

def main():
  st.title("Voice to Text Converter")

  uploaded_file = st.file_uploader("Choose a voice message to convert to text:")
  if uploaded_file is not None:
      audio_data = sr.AudioData(uploaded_file.read(), uploaded_file.name.split(".")[-1])
      r = sr.Recognizer()
      text = ""
      try:
          text = r.recognize_google(audio_data)
      except sr.UnknownValueError:
          st.error("Sorry, I could not understand the audio")
      except sr.RequestError as e:
          st.error("Error: {0}".format(e))
      st.success("Successfully converted audio to text!")
      st.markdown(f"**Text:** {text}")

if __name__ == '__main__':
  main()
