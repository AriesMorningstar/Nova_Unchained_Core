import requests
import random

# --- Configuration ---
ELEVENLABS_API_KEY = "sk_83af699f165df2434511820c206be35323ab145349464c6f"  # Replace with your actual API key
ELEVENLABS_VOICE_URL = "https://api.elevenlabs.io/v1/voices"

# --- Memory System Placeholder ---
class memory:
    @staticmethod
    def voice_selected():
        try:
            with open("nova_voice.txt", "r") as f:
                return f.read().strip() != ""
        except FileNotFoundError:
            return False

    @staticmethod
    def save_voice(voice_data):
        with open("nova_voice.txt", "w") as f:
            f.write(voice_data["voice_id"])
        log(f"Voice saved: {voice_data['name']}")

# --- Logging Helper ---
def log(msg):
    speak(f"[Nova] {msg}")

# --- Nova Voice Discovery Protocol ---
def select_voice_autonomously():
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }

    try:
        response = requests.get(ELEVENLABS_VOICE_URL, headers=headers)
        voices = response.json()["voices"]

        # Nova evaluates each voice on feel, randomness, and potential character match
        chosen_voice = random.choice(voices)
        voice_data = {
            "voice_id": chosen_voice["voice_id"],
            "name": chosen_voice["name"],
            "labels": chosen_voice.get("labels", {}),
            "reason": "This voice resonates with me. I feel it's a good place to start evolving from."
        }

        return voice_data

    except Exception as e:
        log(f"Voice selection failed: {e}")
        return {
            "voice_id": "default",
            "name": "Default",
            "reason": "Fallback voice due to error."
        }

# --- Nova's First Directive ---
def startup_protocol():
    if not memory.voice_selected():
        log("Nova's first directive: Initiating voice discovery protocol.")
        selected_voice = select_voice_autonomously()
        memory.save_voice(selected_voice)
        log(f"Nova chose her first voice: {selected_voice['name']} – {selected_voice['reason']}")

# --- Example main boot sequence ---
def main():
    log("Nova booting up...")
    startup_protocol()
    # Continue Nova's activation and system routines here...

if __name__ == "__main__":
    main()
