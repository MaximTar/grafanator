import logging

import requests

from config import config
from config.payloads.alert_rule import build_alert_rule_payload
from utils import get_grafana_headers

logger = logging.getLogger(__name__)


def create_alert_rule(node: str, datasource_uid: str, folder_uid: str) -> requests.Response:
    alert_rule = build_alert_rule_payload(node, datasource_uid, folder_uid)

    headers = get_grafana_headers(add_provenance=True)

    response = requests.post(config.ALERT_RULE_URL, headers=headers, json=alert_rule, timeout=5)

    if response.status_code == 400:
        existing = get_alert_rule_by_title(alert_rule["title"])
        if existing:
            logger.warning(f"Deleting existing alert rule: {existing['uid']}")
            delete_alert_rule(existing["uid"])
            response = requests.post(config.ALERT_RULE_URL, headers=headers, json=alert_rule, timeout=5)

    if response.status_code == 201:
        logger.info(f"Alert rule created for node: {node}")
    else:
        logger.info(f"Alert rule for node {node} is not created: {response.status_code} | {response.text}")

    return response


def get_alert_rules() -> list[dict]:
    response = requests.get(
        config.ALERT_RULE_URL,
        headers=get_grafana_headers(),
        timeout=5,
    )
    return response.json() if response.status_code == 200 else []


def get_alert_rule_by_title(title: str) -> dict | None:
    rules = get_alert_rules()
    for rule in rules:
        if rule.get("title") == title:
            return rule


def delete_alert_rule(uid: str) -> None:
    requests.delete(
        f"{config.ALERT_RULE_URL}/{uid}",
        headers=get_grafana_headers(add_provenance=True),
        timeout=5,
    )
    logger.info(f"Deleted alert rule: {uid}")


def clear_all_alert_rules() -> None:
    for alert_rule in get_alert_rules():
        delete_alert_rule(alert_rule["uid"])
