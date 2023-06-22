FROM python:3.9-slim-buster

# Install the FFmpeg library
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run"]
CMD ["audio_transcription_app.py"]
