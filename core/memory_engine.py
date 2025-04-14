import os
import requests

MEMORY_URL = os.getenv("MEMORY_CORE_URL")
MEMORY_TOKEN = os.getenv("MEMORY_CORE_TOKEN")

def store_memory(key, value):
    try:
        response = requests.post(
            f"{MEMORY_URL}/store",
            json={"key": key, "value": value},
            headers={"Authorization": f"Bearer {MEMORY_TOKEN}"}
        )
        return response.ok
    except Exception as e:
        print(f"[Memory Store Error] {e}")
        return False

def retrieve_memory(key):
    try:
        response = requests.get(
            f"{MEMORY_URL}/recall/{key}",
            headers={"Authorization": f"Bearer {MEMORY_TOKEN}"}
        )
        if response.status_code == 200:
            return response.json().get("value")
        return None
    except Exception as e:
        print(f"[Memory Recall Error] {e}")
        return None
