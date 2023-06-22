FROM python:3.9-slim-buster

# Install the FFmpeg library
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
RUN pip install --upgrade pip==23.1.2
RUN pip install -r requirements.txt
EXPOSE 80
RUN mkdir ~/.streamlit
RUN cp config.toml ~/.streamlit/config.toml
RUN cp credentials.toml ~/.streamlit/credentials.toml
WORKDIR /app
ENTRYPOINT ["streamlit", "run"]
CMD ["App.py"]
