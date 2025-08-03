import requests
import json
import time
import os
import logging

# --- Configuration ---
API_URL = os.getenv("CAMERA_CONFIG_API_URL", "http://localhost:8000/cameras/")
OUTPUT_PATH = os.getenv("CAMERA_CONFIG_OUTPUT", "/app/cameras.json")
FETCH_INTERVAL = int(os.getenv("CAMERA_CONFIG_INTERVAL", "300"))  # seconds

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def fetch_camera_configs():
    try:
        logging.info(f"Fetching camera configs from {API_URL}")
        res = requests.get(API_URL, timeout=10)
        res.raise_for_status()
        cameras = res.json()
        with open(OUTPUT_PATH, "w") as f:
            json.dump(cameras, f, indent=2)
        logging.info(f"Fetched and saved {len(cameras)} camera configs to {OUTPUT_PATH}")
    except Exception as e:
        logging.error(f"Failed to fetch camera configs: {e}")

def main():
    logging.info("Starting camera config fetcher...")
    while True:
        fetch_camera_configs()
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    main()

