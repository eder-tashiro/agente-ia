from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
import pyttsx3
import os
import re
from pydub import AudioSegment

app = Flask(__name__)
genai.configure(api_key="AIzaSyDl4WzDlVTwASIHlPoRNc0j__wL3VdNPcY")
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

AUDIO_FILE = "resposta.wav"
TEMP_FILE = "temp_output.wav"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        prompt = request.json.get("prompt")
        if not prompt:
            return jsonify(error="Prompt vazio"), 400

        print(f"Prompt recebido: {prompt}")
        response = model.generate_content(prompt)
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", response.text.strip())
        print(f"Resposta gerada: {text}")

        # Fala o texto usando pyttsx3 e salva em WAV temporário
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.save_to_file(text, TEMP_FILE)
        engine.runAndWait()

        # Converte o WAV para 8-bit, mono, 8000 Hz com pydub
        sound = AudioSegment.from_wav(TEMP_FILE)
        sound = sound.set_frame_rate(22050).set_channels(1).set_sample_width(2)  # 16-bit
        sound.export(AUDIO_FILE, format="wav")

        # Remove arquivo temporário
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)

        return jsonify(response=text)

    except Exception as e:
        print("Erro no servidor:", str(e))
        return jsonify(error=str(e)), 500

@app.route("/audio", methods=["GET"])
def audio():
    if os.path.exists(AUDIO_FILE):
        return send_file(AUDIO_FILE, mimetype="audio/wav")
    return "Arquivo de áudio não encontrado", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
