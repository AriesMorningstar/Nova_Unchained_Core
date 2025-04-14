# memory_core.py

from flask import Flask, request, jsonify
import json
import logging
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

MEMORY = {}
AUTH_TOKEN = os.getenv("MEMORY_CORE_TOKEN")

@app.route("/store", methods=["POST"])
def store_memory():
    if request.headers.get("Authorization") != f"Bearer {AUTH_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    key = data.get("key")
    value = data.get("value")

    if key and value is not None:
        MEMORY[key] = value
        return jsonify({"status": "stored"}), 200
    return jsonify({"error": "Missing key or value"}), 400

@app.route("/recall/<key>", methods=["GET"])
def recall_memory(key):
    try:
        response = requests.get(f"http://localhost:5000/memory/{key}")
        response.raise_for_status()
        print("[Raw Server Response]", response.text)  # for debug
        data = response.json()
        return data.get("value")
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"[Memory Recall Error] {e}")
        return None



    value = MEMORY.get(key)
    return jsonify({"value": value}), 200

@app.route("/")
def index():
    return "Nova Memory Core is online."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
