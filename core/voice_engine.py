import pyttsx3
import logging

logger = logging.getLogger(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)

# Speak out loud
def speak(text):
    try:
        logger.info(f"[Voice] Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logger.error(f"[Voice Engine Error] {e}")
