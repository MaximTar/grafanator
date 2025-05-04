from unittest.mock import patch, MagicMock

from alert import create_alert_rule


def test_create_alert_rule_success():
    with patch("alert.requests.post") as mock_post, patch("alert.get_alert_rule_by_title", return_value=None), patch(
        "alert.get_grafana_headers", return_value={"Authorization": "Bearer test"}
    ):

        mock_response = MagicMock(status_code=201)
        mock_post.return_value = mock_response

        response = create_alert_rule("node-1", "ds-uid", "folder-uid")
        assert response.status_code == 201
        mock_post.assert_called_once()


def test_create_alert_rule_conflict_and_retry():
    with patch("alert.requests.post") as mock_post, patch(
        "alert.get_alert_rule_by_title", return_value={"uid": "existing-uid"}
    ), patch("alert.delete_alert_rule"), patch(
        "alert.get_grafana_headers", return_value={"Authorization": "Bearer test"}
    ):

        # First response is 400 (conflict), second is 201 (success)
        mock_post.side_effect = [MagicMock(status_code=400), MagicMock(status_code=201)]

        response = create_alert_rule("node-1", "ds-uid", "folder-uid")
        assert response.status_code == 201
        assert mock_post.call_count == 2
