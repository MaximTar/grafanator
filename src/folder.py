import logging
from os import getenv

import requests

from utils import get_grafana_headers
from config import config

logger = logging.getLogger(__name__)

BASE_URL = getenv("GRAFANA_URL")


def create_folder() -> str:
    payload = {"uid": config.ALERT_FOLDER_UID, "title": config.ALERT_FOLDER_TITLE}
    response = requests.post(
        f"{BASE_URL}/api/folders",
        headers=get_grafana_headers(),
        json=payload,
        timeout=5,
    )

    if response.status_code == 200:
        folder_uid = response.json()["uid"]
        logger.info(f"Folder created successfully: {folder_uid}")
        return folder_uid

    if response.status_code == 412:
        logger.info(f"Folder already exists. Reusing UID: {config.ALERT_FOLDER_UID}")
        return config.ALERT_FOLDER_UID

    logger.error(f"Failed to create folder: {response.status_code} | {response.text}")
    raise RuntimeError(f"Folder creation failed: {response.status_code} | {response.text}")
