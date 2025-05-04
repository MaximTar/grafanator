from config import config


def build_data_source_payload(host: str, port: str) -> dict:
    return {
        "name": config.DATA_SOURCE_NAME_TEMPLATE.format(node=host),
        "type": "prometheus",
        "url": f"http://{host}:{port}",
        "access": "proxy",
        "basicAuth": False,
        "jsonData": {"httpMethod": "GET"},
    }
