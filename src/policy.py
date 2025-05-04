import logging

import requests

from config import config
from utils import get_grafana_headers

logger = logging.getLogger(__name__)


def create_notification_policy(folder_uid: str, rule_group: str, receiver: str) -> requests.Response:
    response = requests.get(config.NOTIFICATION_POLICY_URL, headers=get_grafana_headers(), timeout=5)
    if response.status_code != 200:
        logger.error(f"Failed to fetch policy tree: {response.status_code} | {response.text}")
        return response

    policy_tree = response.json()
    routes = policy_tree.get("routes", [])

    matcher = [["grafana_folder", "=", folder_uid], ["rule_group", "=", rule_group]]
    for route in routes:
        if route.get("object_matchers") == matcher:
            route["receiver"] = receiver
            break
    else:
        routes.append(
            {"receiver": receiver, "object_matchers": matcher, "group_by": [], "continue": False, "routes": []}
        )

    payload = {"receiver": receiver, "group_by": [], "routes": routes}

    response = requests.put(
        config.NOTIFICATION_POLICY_URL, headers=get_grafana_headers(add_provenance=True), json=payload, timeout=5
    )

    if response.status_code in [200, 202]:
        logger.info(f"Notification policy synced: folder '{folder_uid}', group '{rule_group}', receiver '{receiver}'")
    else:
        logger.error(f"Failed to update notification policy: {response.status_code} | {response.text}")

    return response


def clear_all_notification_policies() -> None:
    response = requests.delete(
        config.NOTIFICATION_POLICY_URL, headers=get_grafana_headers(add_provenance=True), timeout=5
    )
    if response.status_code in [200, 202]:
        logger.info("Deleted notification policy tree")
    else:
        logger.error(f"Failed to delete policies: {response.status_code} | {response.text}")
