FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Instalar ffmpeg para conversão de áudio com pydub
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
