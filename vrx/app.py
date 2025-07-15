from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyCqJ-oM6-bEzlc5F14mxm3QRnEevJHnqMk"
GOOGLE_TTS_API_KEY = "AIzaSyC5Ldx6r3EwhR2gE8tv7sJPAId5Zf4F8Lw"

LANGUAGE_CODES = {
    "English": ("en-US", "en-US-Wavenet-D"),
    "Spanish": ("es-ES", "es-ES-Wavenet-B"),
    "German": ("de-DE", "de-DE-Wavenet-B"),
    "Portuguese": ("pt-BR", "pt-BR-Wavenet-A"),
    "Korean": ("ko-KR", "ko-KR-Wavenet-B"),
    "Japanese": ("ja-JP", "ja-JP-Wavenet-B"),
    "Chinese": ("cmn-CN", "cmn-CN-Wavenet-A"),
}

os.makedirs("static", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGE_CODES.keys())

@app.route("/speak", methods=["POST"])
def speak():
    try:
        # Step 1: Get text and language from client
        data = request.get_json()
        user_input = data.get("text", "").strip()
        language = data.get("language", "English")

        if not user_input:
            return jsonify({"error": "Text input is empty."}), 400

        # Step 2: Get language code and voice name
        lang_code, voice_name = LANGUAGE_CODES.get(language, ("en-US", "en-US-Wavenet-D"))

        # Step 3: Gemini Explanation
        gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        gemini_prompt = (
            f"You are a friendly {language.lower()}-speaking professor. "
            f"Translate the following input into conversational {language}. "
            "Avoid repetitions, numbers, or special characters. "
            "Summarize it simply and clearly:\n\n" + user_input
        )
        gemini_prompt = (
        f"Translate and explain the following input in clear, conversational {language}. "
        "Do not include any questions or unnecessary commentary. When asled who are you reply that you are professor that can help students "
        "Keep it expressive and natural. If i ask a question always reply with a solution. I do not want bold words as well make it lower case and plain"
        "Focus only on giving a simple, direct explanation:\n\n" + user_input
        )
        gemini_payload = {
            "contents": [{
                "parts": [{"text": gemini_prompt}]
            }]
        }

        gemini_headers = { "Content-Type": "application/json" }
        gemini_params = { "key": GEMINI_API_KEY }

        gemini_response = requests.post(
            gemini_url,
            headers=gemini_headers,
            params=gemini_params,
            json=gemini_payload
        )

        gemini_response.raise_for_status()
        gemini_data = gemini_response.json()
        if "candidates" not in gemini_data or not gemini_data["candidates"]:
            return jsonify({"error": "Gemini API returned no response."}), 500

        explanation = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
        # Step 4: Google TTS
        tts_url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_TTS_API_KEY}"
        tts_payload = {
            "input": {"text": explanation},
            "voice": {
                "languageCode": lang_code,
                "name": voice_name,
                "ssmlGender": "MALE"
            },
            "audioConfig": {
                "audioEncoding": "MP3",
                "speakingRate": 0.85
            }
        }

        tts_response = requests.post(tts_url, headers={"Content-Type": "application/json"}, json=tts_payload)
        tts_response.raise_for_status()

        audio_content = tts_response.json()["audioContent"]
        audio_path = os.path.join("static", "response.mp3")

        with open(audio_path, "wb") as f:
            f.write(base64.b64decode(audio_content))

        # Step 5: Return result to frontend
        return jsonify({
            "text": explanation,
            "audio": "/static/response.mp3"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === 🚀 Start App ===
if __name__ == "__main__":
    app.run(debug=True)
