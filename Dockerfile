FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Instalar espeak e dependências mínimas
RUN apt-get update && \
    apt-get install -y espeak && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
