import logging

import requests
from flask import Flask, jsonify

from alert import create_alert_rule, clear_all_alert_rules
from config import config
from contact_point import create_contact_point, clear_all_contact_points
from dashboard import create_dashboard, get_all_dashboards, clear_all_dashboards
from data_source import create_data_source, clear_all_data_sources
from folder import create_folder
from policy import create_notification_policy, clear_all_notification_policies

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_node(node: str, folder_uid: str):
    logger.info(f"Setting up dashboard for node: {node}")

    if not node.replace(".", "").replace(":", "").isalnum():
        return jsonify(config.INVALID_NODE_MSG), 400

    if ":" in node:
        host, port = node.split(":")
    else:
        host, port = node, "9090"

    response = create_data_source(host, port)
    if response.status_code != 200:
        return error_response("data source", response)

    try:
        datasource_uid = response.json()["datasource"]["uid"]
    except (KeyError, ValueError):
        return jsonify(config.INVALID_RESPONSE_MSG), 500

    response = create_dashboard(host, datasource_uid)
    if response.status_code != 200:
        return error_response("dashboard", response)

    response = create_alert_rule(host, datasource_uid, folder_uid)
    if response.status_code != 201:
        return error_response("alert rule", response)

    logger.info(f"Dashboard setup complete for {host}")
    return "OK", 200


def error_response(stage: str, response: requests.Response) -> tuple[dict, int]:
    logger.error(f"Failed to create {stage}")
    return response.json(), response.status_code


def create_app() -> Flask:
    app = Flask(__name__)

    if config.RESET_GRAFANA:
        clear_all_notification_policies()
        clear_all_alert_rules()
        clear_all_contact_points()
        clear_all_dashboards()
        clear_all_data_sources()

    create_contact_point()
    folder_uid: str = create_folder()
    create_notification_policy(folder_uid, config.ALERT_RULE_GROUP, config.CONTACT_POINT_NAME)

    @app.route("/add_dashboard/<string:node>", methods=["POST"])
    def add_dashboard(node: str):
        return setup_node(node, folder_uid)

    @app.route("/check_dashboard/<string:node>", methods=["POST"])
    def check_dashboard(node: str):
        dashboards = get_all_dashboards() or []
        for dashboard in dashboards:
            if dashboard.get("title") == config.DASHBOARD_TITLE_TEMPLATE.format(node=node):
                return "OK", 200
        return jsonify(config.NO_DASHBOARD_MSG), 404

    @app.route("/health", methods=["GET"])
    def health():
        return "OK", 200

    return app


application: Flask = create_app()
