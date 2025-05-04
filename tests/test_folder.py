from unittest.mock import patch, MagicMock

from config import config
from folder import create_folder


def test_create_folder_success():
    with patch("folder.get_grafana_headers", return_value={"Authorization": "Bearer test"}), patch(
        "folder.requests.post"
    ) as mock_post:

        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"uid": config.ALERT_FOLDER_UID})

        uid = create_folder()
        assert uid == config.ALERT_FOLDER_UID
        mock_post.assert_called_once()


def test_create_folder_already_exists():
    with patch("folder.get_grafana_headers", return_value={"Authorization": "Bearer test"}), patch(
        "folder.requests.post"
    ) as mock_post:

        mock_post.return_value = MagicMock(status_code=412)

        uid = create_folder()
        assert uid == config.ALERT_FOLDER_UID
        mock_post.assert_called_once()
