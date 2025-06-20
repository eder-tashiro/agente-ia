from flask import Flask, request, jsonify, send_file
from gtts import gTTS
from pydub import AudioSegment
import os
import google.generativeai as genai
import re

app = Flask(__name__)

genai.configure(api_key="AIzaSyDl4WzDlVTwASIHlPoRNc0j__wL3VdNPcY")  # ← substitua aqui

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

AUDIO_MP3 = "resposta.mp3"
AUDIO_WAV = "resposta.wav"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        prompt = request.json.get("prompt")
        if not prompt:
            return jsonify(error="Prompt vazio"), 400

        print(f"Prompt recebido: {prompt}")
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

        print(f"Resposta gerada: {text}")

        # Gerar .mp3 com gTTS
        tts = gTTS(text=text, lang='pt')
        tts.save(AUDIO_MP3)

        # Converter .mp3 para .wav
        sound = AudioSegment.from_mp3(AUDIO_MP3)
        sound.export(AUDIO_WAV, format="wav")

        return jsonify(response=text)

    except Exception as e:
        print("Erro no servidor:", str(e))
        return jsonify(error=str(e)), 500


@app.route("/audio", methods=["GET"])
def audio():
    if os.path.exists(AUDIO_WAV):
        return send_file(AUDIO_WAV, mimetype="audio/wav")
    return "Arquivo de áudio não encontrado", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
