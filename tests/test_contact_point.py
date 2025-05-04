import os
from unittest.mock import patch, MagicMock

from contact_point import create_contact_point


def test_create_contact_point_create_new():
    with patch("contact_point.get_contact_point_by_title", return_value=None), patch(
        "contact_point.get_grafana_headers", return_value={"Authorization": "Bearer test"}
    ), patch("contact_point.requests.post") as mock_post:

        os.environ["TG_BOT_TOKEN"] = "dummy"
        os.environ["TG_CHAT_ID"] = "123"

        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"uid": "abc-uid"})

        uid = create_contact_point()
        assert uid == "abc-uid"
        mock_post.assert_called_once()


def test_create_contact_point_updates_existing():
    with patch("contact_point.get_contact_point_by_title", return_value={"uid": "existing-uid"}), patch(
        "contact_point.get_grafana_headers", return_value={"Authorization": "Bearer test"}
    ), patch("contact_point.requests.put") as mock_put:

        os.environ["TG_BOT_TOKEN"] = "dummy"
        os.environ["TG_CHAT_ID"] = "123"

        mock_put.return_value = MagicMock(status_code=200)

        uid = create_contact_point()
        assert uid == "existing-uid"
        mock_put.assert_called_once()
