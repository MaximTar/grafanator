import logging
from os import getenv

import requests

from config import config
from config.payloads.contact_point import build_contact_point_payload
from utils import get_grafana_headers

logger = logging.getLogger(__name__)


def create_contact_point() -> str:
    token = getenv("TG_BOT_TOKEN")
    chat_id = getenv("TG_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("Telegram bot token or chat ID is missing")

    existing = get_contact_point_by_title(config.CONTACT_POINT_NAME)

    payload = build_contact_point_payload(token, chat_id)

    url = f"{config.CONTACT_POINT_URL}/{existing['uid']}" if existing else config.CONTACT_POINT_URL
    method = requests.put if existing else requests.post
    headers = get_grafana_headers(add_provenance=False if existing else True)

    response = method(url, headers=headers, json=payload, timeout=5)

    if response.status_code in [200, 202]:
        logger.info(f"{'Updated' if existing else 'Created'} contact point '{config.CONTACT_POINT_NAME}'")
        return existing["uid"] if existing else response.json()["uid"]
    else:
        logger.error(f"Failed to create contact point: {response.status_code} | {response.text}")
        raise RuntimeError(f"Failed to create contact point: {response.status_code} | {response.text}")


def get_contact_points() -> list[dict]:
    response = requests.get(
        config.CONTACT_POINT_URL,
        headers=get_grafana_headers(),
        timeout=5,
    )
    return response.json() if response.status_code == 200 else []


def get_contact_point_by_title(title: str) -> dict | None:
    for contact_point in get_contact_points():
        if contact_point["name"] == title:
            return contact_point


def delete_contact_point(uid: str) -> None:
    requests.delete(
        f"{config.CONTACT_POINT_URL}/{uid}",
        headers=get_grafana_headers(add_provenance=True),
        timeout=5,
    )
    logger.info(f"Deleted contact point: {uid}")


def clear_all_contact_points() -> None:
    for contact_point in get_contact_points():
        # example email receiver have no uid
        if contact_point["uid"]:
            delete_contact_point(contact_point["uid"])
