from os import getenv


def get_grafana_headers(add_provenance=False) -> dict:
    headers = {
        "Authorization": f"Bearer {getenv('GRAFANA_API_KEY')}",
        "Content-Type": "application/json",
    }
    # By default, you cannot edit API-provisioned alerting resources in Grafana
    # To enable editing these resources in the Grafana UI, add the X-Disable-Provenance: true header
    if add_provenance:
        headers["X-Disable-Provenance"] = "true"
    return headers
