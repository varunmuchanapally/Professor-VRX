# Professor-VRX
# 🧠 Professor VRX – Multilingual Voice Explainer

Professor VRX is an interactive Flask-based web application that allows users to input text, receive a clear and beginner-friendly explanation from Google's Gemini model, and listen to that explanation spoken aloud in the selected language using Google Text-to-Speech (TTS).

---

## 🚀 Features

- 🎤 Text-to-speech conversion in **multiple languages**
- 🤖 Explanations generated via **Gemini 2.0 Flash** model
- 🌐 Supported Languages:
  - English 🇺🇸
  - Spanish 🇪🇸
  - Japanese 🇯🇵
  - ...and more!
- 🔊 Audio player embedded in the UI
- 🟢 Live animated sphere that reacts while audio is playing

---

## 🧩 Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Three.js (for sphere animation)
- **Backend:** Python (Flask)
- **APIs Used:**
  - [Gemini (Google Generative Language API)](https://ai.google.dev/)
  - [Google Cloud Text-to-Speech API](https://cloud.google.com/text-to-speech)

---

## 🛠️ Installation
```bash

1. Clone the repository

git clone https://github.com/varunmuchanapally/Professor-VRX.git
cd vrx

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

3. Install dependencies
pip install -r requirements.txt

4. Add your API keys

Open app.py and update:
GEMINI_API_KEY = "your_gemini_api_key"
GOOGLE_TTS_API_KEY = "your_google_tts_api_key"

Running the App
python app.py
