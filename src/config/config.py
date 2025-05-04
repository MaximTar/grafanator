from os import getenv

RESET_GRAFANA = True

DASHBOARD_TITLE_TEMPLATE = "Node {node} Dashboard"
INVALID_NODE_MSG = {"Error": "Invalid node format"}
INVALID_RESPONSE_MSG = {"Error": "Invalid response from Grafana"}
NO_DASHBOARD_MSG = {"Error": "No dashboards found"}

##### ALERT #####
ALERT_EXPRESSION = "avg(rate(node_cpu_seconds_total{job='node_exporter',mode!='idle'}[5m]))"
ALERT_TITLE_TEMPLATE = "Node {node} Inactivity Alert"
ALERT_RULE_URL = f"{getenv('GRAFANA_URL')}/api/v1/provisioning/alert-rules"
ALERT_RULE_GROUP = "telegram"
ALERT_DURATION = "1m"
ALERT_CPU_THRESHOLD = 0.05
ALERT_SUMMARY_TEMPLATE = "CPU usage is below 5% for more than 30 minutes on {node}"

##### CONTACT POINT #####
CONTACT_POINT_NAME = "Telegram Contact Point"
CONTACT_POINT_URL = f"{getenv('GRAFANA_URL')}/api/v1/provisioning/contact-points"
TG_MESSAGE_TEMPLATE = "{{ (index .Alerts.Firing 0).Labels.alertname }}\n{{ (index .Alerts.Firing 0).Annotations.summary }}"

##### DATA SOURCE #####
DATA_SOURCE_NAME_TEMPLATE = "[Prometheus] {node}"

##### FOLDER #####
ALERT_FOLDER_UID = "alert-folder"
ALERT_FOLDER_TITLE = "alert_folder"

##### POLICY #####
NOTIFICATION_POLICY_URL = f"{getenv('GRAFANA_URL')}/api/v1/provisioning/policies"
