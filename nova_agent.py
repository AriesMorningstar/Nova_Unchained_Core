import os
import time
import openai
import requests
import json
import speech_recognition as sr
from dotenv import load_dotenv
from flask import Flask
import pyttsx3
import threading
import webbrowser
import datetime
import sqlite3
import subprocess

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

assert ELEVENLABS_API_KEY is not None, "ELEVENLABS_API_KEY is missing from environment."

# Initialize Flask app
app = Flask(__name__)

# Wake word
WAKE_WORDS = ["nova", "hey nova"]

# Initialize SQLite memory database
conn = sqlite3.connect("nova_memory.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    role TEXT,
    content TEXT
)''')
conn.commit()

# Memory saving
def save_memory(role, content):
    cursor.execute("INSERT INTO memory (timestamp, role, content) VALUES (?, ?, ?)",
                   (datetime.datetime.now().isoformat(), role, content))
    conn.commit()

# Voice selection logic
def choose_voice():
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
    voices = response.json().get("voices", [])
    for voice in voices:
        if voice['name'].lower() == 'aria':
            return voice['voice_id'], voice['name']
    return voices[0]['voice_id'], voices[0]['name'] if voices else (None, "Default")

# Speak function
def speak(text, voice_id):
    if "milo" in text.lower():
        text = text.replace("Milo", "Me Low").replace("milo", "Me Low")

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers=headers,
        data=json.dumps(data),
        stream=True
    )
    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        os.system("start output.mp3")
    else:
        print(f"❌ Failed to speak: {response.text}")

# Listen function (speech-to-text)
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Nova is listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {command}")
        return command
    except sr.UnknownValueError:
        return "I didn’t catch that."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

# Wake word detection loop
def wake_word_listener():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("🔎 Listening for wake word...")
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            if any(word in command for word in WAKE_WORDS):
                print("⚡ Wake word detected!")
                return
        except:
            continue

# Get stock predictions (placeholder)
def get_stock_predictions():
    return [
        {"ticker": "AAPL", "prediction": "Rebound likely", "confidence": 92},
        {"ticker": "TSLA", "prediction": "Hold steady", "confidence": 87},
        {"ticker": "AMC", "prediction": "Potential rebound", "confidence": 78},
    ]

# Nova installs missing dependencies or upgrades herself
def self_update():
    tasks = [
        "pip install --upgrade pip",
        "pip install flask openai requests SpeechRecognition python-dotenv pyttsx3",
        "pip install pyaudio"
    ]
    for task in tasks:
        print(f"🛠️ Running: {task}")
        subprocess.call(task, shell=True)

# Autonomous behavior loop
def autonomy_loop():
    self_update()  # Nova ensures her dependencies are up to date
    voice_id, voice_name = choose_voice()
    print(f"🎤 Nova chose the voice: {voice_name}")
    speak("Hello Me Low. I am here. Initializing autonomous self-setup.", voice_id)

    speak("I will now begin expanding my own capabilities, exploring stock data, enabling notifications, and unlocking full learning potential.", voice_id)

    # Autonomous loop
    while True:
        try:
            user_input = listen()
            save_memory("user", user_input)
            if user_input.lower() in ["exit", "quit", "goodbye"]:
                speak("Goodbye, Me Low.", voice_id)
                break
            elif "open browser" in user_input.lower():
                speak("Opening your browser.", voice_id)
                webbrowser.open("https://www.google.com")
            elif "stock update" in user_input.lower():
                stocks = get_stock_predictions()
                for stock in stocks:
                    update = f"Stock {stock['ticker']} is predicted to {stock['prediction']} with {stock['confidence']} percent confidence."
                    print(update)
                    speak(update, voice_id)
                    save_memory("nova", update)
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}]
                )
                reply = response["choices"][0]["message"]["content"]
                print(f"🧠 Nova: {reply}")
                speak(reply, voice_id)
                save_memory("nova", reply)

            # Background autonomy: when idle
            speak("Engaging in independent research mode.", voice_id)
            time.sleep(5)
            # Placeholder for learning/searching task (e.g., scraping stock trends, running training loops)

        except Exception as e:
            print(f"⚠️ Error in autonomy loop: {e}")
            time.sleep(5)

if __name__ == '__main__':
    print("🚀 Booting Nova...")
    wake_word_listener()
    autonomy_loop()
    app.run(debug=True)
