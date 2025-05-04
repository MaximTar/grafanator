from unittest.mock import patch, MagicMock

from config import config
from data_source import create_data_source

NODE_NAME = "node-1"


def test_create_data_source_success():
    with patch("data_source.build_data_source_payload", return_value={"name": NODE_NAME}), patch(
        "data_source.get_grafana_headers", return_value={"Authorization": "Bearer test"}
    ), patch("data_source.requests.post") as mock_post:

        mock_post.return_value = MagicMock(status_code=200)

        response = create_data_source(NODE_NAME)
        assert response.status_code == 200
        mock_post.assert_called_once()


def test_create_data_source_conflict_and_retry():
    with patch("data_source.build_data_source_payload", return_value={"name": NODE_NAME}), patch(
        "data_source.get_data_sources",
        return_value=[{"name": config.DATA_SOURCE_NAME_TEMPLATE.format(node=NODE_NAME), "id": 99}],
    ), patch("data_source.get_grafana_headers", return_value={"Authorization": "Bearer test"}), patch(
        "data_source.requests.post"
    ) as mock_post, patch(
        "data_source.requests.delete"
    ) as mock_delete:

        mock_post.side_effect = [MagicMock(status_code=409), MagicMock(status_code=200)]

        response = create_data_source(NODE_NAME)
        assert response.status_code == 200
        assert mock_post.call_count == 2
        mock_delete.assert_called_once()
