from unittest.mock import patch

import pytest

with patch("contact_point.create_contact_point", return_value=None), patch(
    "folder.create_folder", return_value="mock-folder-uid"
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
