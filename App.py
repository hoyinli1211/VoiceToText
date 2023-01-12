import streamlit as st
import wave

def main():
    st.set_page_config(page_title="Upload Voice File", page_icon=":microphone:", layout="wide")
    st.title("Upload Voice File")

    file = st.file_uploader("Upload a .wav file", type=["wav"])
    if file:
        with wave.open(file, "rb") as f:
            st.write("File Name: ", f.getparams())

if __name__ == "__main__":
    main()
