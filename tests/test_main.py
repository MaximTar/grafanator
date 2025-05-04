from unittest.mock import patch

import pytest

with (
    patch("contact_point.create_contact_point", return_value=None),
    patch("folder.create_folder", return_value="mock-folder-uid"),
    patch("policy.create_notification_policy", return_value=None),
    patch("policy.clear_all_notification_policies", return_value=None),
    patch("alert.clear_all_alert_rules", return_value=None),
    patch("contact_point.clear_all_contact_points", return_value=None),
    patch("dashboard.clear_all_dashboards", return_value=None),
    patch("data_source.clear_all_data_sources", return_value=None),
):
    from main import application


@pytest.fixture
def client():
    application.config["TESTING"] = True
    with application.test_client() as client:
        yield client


def test_add_dashboard_route_success(client):
    with patch("main.setup_node", return_value=("OK", 200)) as mock_setup:
        response = client.post("/add_dashboard/test-node")
        assert response.status_code == 200
        assert response.data == b"OK"
        mock_setup.assert_called_once_with("test-node", "mock-folder-uid")


def test_check_dashboard_found(client):
    mock_dashboard = {"title": "Node test-node Dashboard"}
    with patch("main.get_all_dashboards", return_value=[mock_dashboard]):
        response = client.post("/check_dashboard/test-node")
        assert response.status_code == 200
        assert response.data == b"OK"


def test_check_dashboard_not_found(client):
    with patch("main.get_all_dashboards", return_value=[]):
        response = client.post("/check_dashboard/test-node")
        assert response.status_code == 404
        assert b"No dashboards found" in response.data
