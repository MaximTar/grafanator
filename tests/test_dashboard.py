from unittest.mock import patch, MagicMock

from dashboard import create_dashboard


def test_create_dashboard_success():
    with patch("dashboard.get_dashboard_by_title", return_value=None), patch(
        "dashboard.get_grafana_headers", return_value={"Authorization": "Bearer test"}
    ), patch("dashboard.requests.post") as mock_post:

        mock_response = MagicMock(status_code=200)
        mock_post.return_value = mock_response

        response = create_dashboard("node-123", "ds-uid")

        assert response.status_code == 200
        mock_post.assert_called_once()


def test_create_dashboard_replaces_existing():
    with patch("dashboard.get_dashboard_by_title", return_value={"uid": "existing-uid"}), patch(
        "dashboard.get_grafana_headers", return_value={"Authorization": "Bearer test"}
    ), patch("dashboard.requests.post") as mock_post, patch("dashboard.requests.delete") as mock_delete:

        mock_response = MagicMock(status_code=200)
        mock_post.return_value = mock_response

        response = create_dashboard("node-123", "ds-uid")

        assert response.status_code == 200
        mock_post.assert_called_once()
        mock_delete.assert_called_once()
