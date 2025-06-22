from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
import os
import re
import subprocess

app = Flask(__name__)
genai.configure(api_key="AIzaSyDl4WzDlVTwASIHlPoRNc0j__wL3VdNPcY")
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

AUDIO_FILE = "resposta.wav"
TEXT_FILE = "resposta.txt"

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

        # Salva o texto em um arquivo temporário
        with open(TEXT_FILE, "w") as f:
            f.write(text)

        # Usa espeak para gerar o áudio
        subprocess.run(["espeak", "-v", "pt", "-s", "140", "-f", TEXT_FILE, "-w", AUDIO_FILE], check=True)

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
