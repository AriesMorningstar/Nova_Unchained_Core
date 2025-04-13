import requests
import os
import logging

logger = logging.getLogger(__name__)

def check_and_update():
    try:
        version_url = os.getenv("VERSION_CHECK_URL")
        if not version_url:
            logger.info("No update URL provided. Skipping update check.")
            return

        response = requests.get(version_url)
        response.raise_for_status()
        remote_version = response.text.strip()

        with open("version.txt", "r") as f:
            local_version = f.read().strip()

        if remote_version != local_version:
            logger.warning(f"[Updater] New version available: {remote_version}")
            logger.info("Nova update available. Please pull the latest changes.")
        else:
            logger.info("[Updater] Nova is up to date.")
    except Exception as e:
        logger.error(f"[Updater Error] Could not check for updates: {e}")
