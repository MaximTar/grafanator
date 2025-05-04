def build_dashboard_payload(title: str, datasource_uid: str) -> dict:
    return {
        "dashboard": {
            "id": None,
            "uid": None,
            "title": title,
            "tags": [],
            "timezone": "browser",
            "schemaVersion": 16,
            "version": 0,
            "refresh": "5s",
            "panels": [
                {
                    "datasource": {"type": "prometheus", "uid": datasource_uid},
                    "targets": [
                        {
                            "editorMode": "code",
                            "expr": "node_time_seconds - node_boot_time_seconds",
                            "instant": False,
                            "legendFormat": "__auto",
                            "range": True,
                            "refId": "A",
                        }
                    ],
                    "type": "timeseries",
                }
            ],
        },
        "overwrite": False,
    }
