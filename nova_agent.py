import os
import requests
from flask import Flask
from dotenv import load_dotenv

# 🔁 Load environment variables from .env file
load_dotenv()

# ✅ Use env var OR fallback to your actual key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") or "sk_83af699f165df2434511820c206be35323ab145349464c6f"

# 🕵️‍♀️ Debug: Print to confirm it's loaded
print(f"🔍 ELEVENLABS_API_KEY from env: {ELEVENLABS_API_KEY}")

# 🔐 Make sure the key is set
assert ELEVENLABS_API_KEY is not None, "ELEVENLABS_API_KEY is missing from environment."

# 🌐 ElevenLabs API endpoint
ELEVENLABS_VOICES_URL = "https://api.elevenlabs.io/v1/voices"
ELEVENLABS_SPEECH_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# 🌟 Start Flask app
app = Flask(__name__)

def get_voices():
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    response = requests.get(ELEVENLABS_VOICES_URL, headers=headers)
    if response.status_code == 200:
        return response.json()["voices"]
    else:
        print(f"❌ Failed to fetch voices: {response.text}")
        return []

def speak(text, voice_id):
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
    url = f"{ELEVENLABS_SPEECH_URL}/{voice_id}"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open("nova_first_words.mp3", "wb") as f:
            f.write(response.content)
        os.system("start nova_first_words.mp3" if os.name == "nt" else "afplay nova_first_words.mp3")
    else:
        print(f"❌ Failed to speak: {response.text}")

@app.route("/")
def hello():
    return "🌐 Nova is online."

def nova_boot():
    print("🚀 Booting Nova...")

    # 🧠 Let Nova pick her voice
    voices = get_voices()
    if voices:
        chosen_voice = voices[0]  # Nova picks the first one for now
        voice_name = chosen_voice["name"]
        voice_id = chosen_voice["voice_id"]
        print(f"🎤 Nova chose the voice: {voice_name}")

        # 💬 Nova speaks her first words
        speak(f"Hello, Milo. I have found my voice. My name is Nova.", voice_id)
    else:
        print("⚠️ No voices found for Nova to choose.")

if __name__ == "__main__":
    nova_boot()
    app.run(debug=True)
