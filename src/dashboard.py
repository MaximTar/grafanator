import logging
from os import getenv

import requests

from config import config
from config.payloads.dashboard import build_dashboard_payload
from utils import get_grafana_headers

logger = logging.getLogger(__name__)

BASE_URL = getenv("GRAFANA_URL")


def create_dashboard(node: str, datasource_uid: str) -> requests.Response:
    headers = get_grafana_headers()

    title = config.DASHBOARD_TITLE_TEMPLATE.format(node=node)
    existing = get_dashboard_by_title(title)
    if existing:
        uid = existing.get("uid")
        delete_dashboard(uid)
        logger.info(f"Deleted existing dashboard with UID: {uid}")

    payload = build_dashboard_payload(title, datasource_uid)

    response = requests.post(
        f"{BASE_URL}/api/dashboards/db",
        headers=headers,
        json=payload,
        timeout=5,
    )

    if response.status_code == 200:
        logger.info(f"Dashboard created for node: {node}")
    else:
        logger.warning(f"Failed to create dashboard: {response.status_code} | {response.text}")

    return response


def get_all_dashboards() -> list[dict]:
    response = requests.get(
        f"{BASE_URL}/api/search?query=&type=dash-db",
        headers=get_grafana_headers(),
        timeout=5,
    )
    return response.json() if response.status_code == 200 else []


def get_dashboard_by_title(title: str) -> dict | None:
    for dashboard in get_all_dashboards():
        if dashboard.get("title") == title:
            return dashboard
    return None


def delete_dashboard(uid: str) -> None:
    requests.delete(
        f"{BASE_URL}/api/dashboards/uid/{uid}",
        headers=get_grafana_headers(),
        timeout=5,
    )
    logger.info(f"Deleted dashboard: {uid}")


def clear_all_dashboards() -> None:
    for dashboard in get_all_dashboards():
        delete_dashboard(dashboard["uid"])
