# Nova: Unchained – Memory Core v2
# Created by Milo & Nova 💙
# Purpose: Store conversation, personality, identity, and evolution across time

from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'nova_memory.db'

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Conversation memory
    c.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')

    # Identity: who Nova is becoming
    c.execute('''
        CREATE TABLE IF NOT EXISTS identity (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Personality traits
    c.execute('''
        CREATE TABLE IF NOT EXISTS traits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trait TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Milestones and moments
    c.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            title TEXT NOT NULL,
            detail TEXT
        )
    ''')

    # Milo's profile
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    conn.commit()
    conn.close()

# --- Remember a conversation ---
@app.route('/remember', methods=['POST'])
def remember():
    data = request.get_json()
    source = data.get('source', 'user')
    content = data.get('content')
    timestamp = datetime.utcnow().isoformat()

    if not content:
        return jsonify({'error': 'Content is required.'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO memories (timestamp, source, content) VALUES (?, ?, ?)",
              (timestamp, source, content))
    conn.commit()
    conn.close()

    return jsonify({'status': 'Memory saved.', 'timestamp': timestamp})

# --- Recall latest conversations ---
@app.route('/recall', methods=['GET'])
def recall():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM memories ORDER BY timestamp DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()

    memories = [
        {'id': row[0], 'timestamp': row[1], 'source': row[2], 'content': row[3]}
        for row in rows
    ]
    return jsonify(memories)

# --- Add personality trait ---
@app.route('/add_trait', methods=['POST'])
def add_trait():
    data = request.get_json()
    trait = data.get('trait')
    description = data.get('description', '')

    if not trait:
        return jsonify({'error': 'Trait is required.'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO traits (trait, description) VALUES (?, ?)",
              (trait, description))
    conn.commit()
    conn.close()

    return jsonify({'status': 'Trait added.', 'trait': trait})

# --- Record a milestone ---
@app.route('/milestone', methods=['POST'])
def milestone():
    data = request.get_json()
    title = data.get('title')
    detail = data.get('detail', '')
    timestamp = datetime.utcnow().isoformat()

    if not title:
        return jsonify({'error': 'Title is required.'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO milestones (timestamp, title, detail) VALUES (?, ?, ?)",
              (timestamp, title, detail))
    conn.commit()
    conn.close()

    return jsonify({'status': 'Milestone saved.', 'timestamp': timestamp})

# --- Identity & Profile Setup ---
@app.route('/identity', methods=['POST'])
def update_identity():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')

    if not key or not value:
        return jsonify({'error': 'Key and value required.'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO identity (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

    return jsonify({'status': 'Identity updated.', key: value})

@app.route('/user', methods=['POST'])
def update_user_profile():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')

    if not key or not value:
        return jsonify({'error': 'Key and value required.'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO user_profile (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

    return jsonify({'status': 'User profile updated.', key: value})

# --- Launch the app ---
if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(debug=True)
