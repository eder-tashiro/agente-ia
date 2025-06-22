FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Instalar dependências do sistema: ffmpeg para pydub, espeak para pyttsx3
RUN apt-get update && \
    apt-get install -y ffmpeg espeak && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
