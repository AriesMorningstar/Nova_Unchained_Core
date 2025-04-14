from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import eventlet
import core.memory_engine as mem
from core.nova_scheduler import start_background_tasks, schedule_memory_recall, schedule_uptime_ping
from core.voice_engine import speak
from core.api_client import get_stock_data
from core.auto_updater import check_and_update
import os
from dotenv import load_dotenv
import logging
import requests
from core.daily_briefing import good_morning_briefing
import json

# Load Nova's Codex
try:
    with open("core/codex.json") as f:
        nova_codex = json.load(f)
        print("[Codex] Loaded successfully.")
except Exception as e:
    nova_codex = {}
    print(f"[Codex] Failed to load: {e}")

# Load .env variables
load_dotenv()

# Logging setup
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(filename="nova.log", level=LOG_LEVEL,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Flask & SocketIO setup
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize memory DB
mem.init_memory_db()

# Perform automatic update check
check_and_update()

# Background tasks (memory syncing, stock polling, recall, uptime ping)
start_background_tasks()
schedule_memory_recall()
schedule_uptime_ping()

@app.route("/morning-briefing", methods=["GET"])
def morning_briefing():
    message = good_morning_briefing()
    return {"message": message}, 200

@app.route("/")
def index():
    return "Nova: Unchained is online."

@app.route("/speak/<text>")
def speak_text(text):
    try:
        speak(text)
        return f"Speaking: {text}"
    except Exception as e:
        logger.error(f"[Speak Error] {e}")
        return jsonify({"error": "Speech failed."}), 500

@app.route("/remember/<key>/<value>")
def remember(key, value):
    try:
        mem.store_memory(key, value)
        return f"Memory stored: {key} → {value}"
    except Exception as e:
        logger.error(f"[Memory Store Error] {e}")
        return jsonify({"error": "Failed to store memory."}), 500

@app.route("/recall/<key>")
def recall(key):
    try:
        value = mem.retrieve_memory(key)
        return value or f"No memory found for: {key}"
    except Exception as e:
        logger.error(f"[Memory Recall Error] {e}")
        return jsonify({"error": "Failed to retrieve memory."}), 500

@app.route("/stock/<symbol>")
def stock(symbol):
    try:
        price = get_stock_data(symbol)
        return f"Stock price for {symbol.upper()}: ${price}" if price else "Stock data unavailable."
    except Exception as e:
        logger.error(f"[Stock Error] {e}")
        return jsonify({"error": "Stock lookup failed."}), 500

@socketio.on('ping')
def handle_ping():
    logger.info("Received ping event")
    socketio.emit('pong', {'message': 'Nova is alive'})

# Self-update checker (manual route)
@app.route("/check-update")
def check_update():
    try:
        version_url = os.getenv("VERSION_CHECK_URL")
        if not version_url:
            return "No version URL set."
        response = requests.get(version_url)
        remote_version = response.text.strip()
        with open("version.txt", "r") as f:
            local_version = f.read().strip()
        if remote_version != local_version:
            speak("Nova update available. Please pull the latest changes.")
            return "Update available."
        return "Nova is up to date."
    except Exception as e:
        logger.error(f"[Update Check Error] {e}")
        return "Could not check for updates."

# 🔁 FINAL LAUNCH LINE — This is what you want to change for debug output
if __name__ == "__main__":
    mem.store_memory("codex", nova_codex)
    logger.info("Starting Nova Core Server...")
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 10000)), debug=False)

