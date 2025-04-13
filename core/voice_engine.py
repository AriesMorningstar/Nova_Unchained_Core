import os
import requests

ELEVENLABS_API_KEY = os.getenv("sk_83af699f165df2434511820c206be35323ab145349464c6f")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # Replace if using custom voice

def speak(text):
    if not ELEVENLABS_API_KEY:
        print("[TTS ERROR] ElevenLabs API key is missing. Nova's voice is muted.")
        print(f"[SPEAKING SIMULATION] {text}")
        return

    if not VOICE_ID:
        print("[TTS ERROR] ElevenLabs Voice ID is missing.")
        return

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
        )

        if response.status_code == 200:
            with open("temp_audio.mp3", "wb") as f:
                f.write(response.content)

            # Check if audio tools are available before trying to play audio
            if os.system("which mpg123 > /dev/null") == 0:
                os.system("mpg123 temp_audio.mp3")
            else:
                print("[TTS WARNING] 'mpg123' not found. Audio file saved but not played.")

            os.remove("temp_audio.mp3")
        else:
            print(f"[TTS ERROR] ElevenLabs responded with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[TTS ERROR] {e}")

