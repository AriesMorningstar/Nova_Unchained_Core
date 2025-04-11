from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("ELEVENLABS_API_KEY")
print("🔍 ELEVENLABS_API_KEY from .env:", key)
