import threading
import time
import logging
from core.memory_engine import retrieve_memory
from core.voice_engine import speak
import requests
import os

logger = logging.getLogger(__name__)

def background_memory_sync():
    while True:
        try:
            logger.info("[Scheduler] Syncing memory...")
            time.sleep(3600)
        except Exception as e:
            logger.error(f"[Scheduler Error] Memory sync failed: {e}")

def schedule_memory_recall():
    def recall_task():
        while True:
            try:
                logger.info("[Scheduler] Recalling memory...")
                remembered = retrieve_memory("favorite_color")
                if remembered:
                    logger.info(f"[Scheduler] Remembered favorite color: {remembered}")
                time.sleep(7200)
            except Exception as e:
                logger.error(f"[Recall Error] {e}")
    threading.Thread(target=recall_task, daemon=True).start()

def schedule_uptime_ping():
    def ping_task():
        while True:
            try:
                ping_url = os.getenv("UPTIME_PING_URL")
                if ping_url:
                    requests.get(ping_url)
                    logger.info("[Scheduler] Sent uptime ping.")
                time.sleep(900)
            except Exception as e:
                logger.error(f"[Uptime Ping Error] {e}")
    threading.Thread(target=ping_task, daemon=True).start()

def start_background_tasks():
    threading.Thread(target=background_memory_sync, daemon=True).start()
