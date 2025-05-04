from config import config


def build_alert_rule_payload(node: str, datasource_uid: str, folder_uid: str) -> dict:
    return {
        # Displayed name of the alert rule in Grafana
        "title": config.ALERT_TITLE_TEMPLATE.format(node=node),
        # Final evaluation condition for triggering alert
        "condition": "C",
        # What state to assume when there's no data
        "noDataState": "NoData",
        # What state to assume if evaluation fails
        "execErrState": "OK",
        # Query steps used in evaluation
        "data": [
            # Step A: metric expression from Prometheus
            {
                "refId": "A",
                "datasourceUid": datasource_uid,
                "relativeTimeRange": {"from": 1800, "to": 0},  # last 30 min
                "model": {
                    "refId": "A",
                    "expr": config.ALERT_EXPRESSION,
                },
            },
            # Step B: reduce expression A to a single number
            {
                "refId": "B",
                "relativeTimeRange": {"from": 1800, "to": 0},
                "datasourceUid": "__expr__",
                "model": {
                    "conditions": [
                        {
                            "evaluator": {"params": [], "type": "gt"},  # dummy evaluator (ignored here)
                            "operator": {"type": "and"},
                            "query": {"params": ["B"]},
                            "reducer": {"params": [], "type": "last"},
                            "type": "query",
                        }
                    ],
                    "datasource": {"type": "__expr__", "uid": "__expr__"},
                    "expression": "A",  # input: result from A
                    "reducer": "last",  # take last point from A
                    "refId": "B",
                    "settings": {"mode": "dropNN"},  # drop NaNs/nulls
                    "type": "reduce",  # reduce vector → scalar
                },
            },
            # Step C: threshold evaluation on B
            {
                "refId": "C",
                "relativeTimeRange": {"from": 1800, "to": 0},
                "datasourceUid": "__expr__",
                "model": {
                    "refId": "C",
                    "type": "threshold",  # threshold logic
                    "datasource": {"type": "__expr__", "uid": "__expr__"},
                    "conditions": [
                        {
                            "type": "query",
                            # trigger if < config.CPU_ALERT_THRESHOLD
                            "evaluator": {"params": [config.ALERT_CPU_THRESHOLD], "type": "lt"},
                            "operator": {"type": "and"},
                            "query": {"params": ["C"]},
                            "reducer": {"params": [], "type": "last"},
                        }
                    ],
                    "expression": "B",  # input from step B
                },
            },
        ],
        # How long the condition must persist before triggering
        "for": config.ALERT_DURATION,
        # This message will appear in alerts
        "annotations": {
            "summary": config.ALERT_SUMMARY_TEMPLATE.format(node=node),
        },
        # Folder in Grafana where this rule will be stored
        "folderUID": folder_uid,
        # Rule group name (can help organize alerts)
        "ruleGroup": config.ALERT_RULE_GROUP,
    }
