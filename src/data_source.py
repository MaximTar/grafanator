import logging
from os import getenv

import requests

from config import config
from config.payloads.data_source import build_data_source_payload
from utils import get_grafana_headers

logger = logging.getLogger(__name__)

BASE_URL = getenv("GRAFANA_URL")


def create_data_source(host: str, port: str) -> requests.Response:
    name = config.DATA_SOURCE_NAME_TEMPLATE.format(node=host)
    headers = get_grafana_headers()
    payload = build_data_source_payload(host, port)

    response = requests.post(
        f"{BASE_URL}/api/datasources",
        headers=headers,
        json=payload,
        timeout=5,
    )

    if response.status_code == 409:
        logger.warning(f"Conflict creating data source '{name}', trying to delete and recreate.")
        delete_data_source_by_name(name)
        response = requests.post(
            f"{BASE_URL}/api/datasources",
            headers=headers,
            json=payload,
            timeout=5,
        )

    return response


def get_data_sources() -> list[dict]:
    response = requests.get(
        f"{BASE_URL}/api/datasources",
        headers=get_grafana_headers(),
        timeout=5,
    )
    return response.json() if response.status_code == 200 else []


def get_data_source_by_name(name: str) -> dict | None:
    data_sources = get_data_sources()
    for data_source in data_sources:
        if data_source.get("name") == name:
            return data_source


def delete_data_source(ds_id: str) -> None:
    requests.delete(
        f"{BASE_URL}/api/datasources/{ds_id}",
        headers=get_grafana_headers(),
        timeout=5,
    )
    logger.info(f"Deleted data source: {ds_id}")


def delete_data_source_by_name(name: str) -> None:
    data_source = get_data_source_by_name(name)
    if data_source:
        delete_data_source(data_source["id"])


def clear_all_data_sources() -> None:
    for data_source in get_data_sources():
        delete_data_source(data_source["id"])
