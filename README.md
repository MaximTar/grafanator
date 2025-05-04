# Grafanator

[![CI](https://github.com/maximtar/grafanator/actions/workflows/test.yml/badge.svg)](https://github.com/your-org/grafanator/actions) 
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight Flask-based service that automates Grafana configuration via HTTP.

---

## Why use it?

**Grafanator** exposes a simple API that lets you trigger dashboard creation and alert setup for any node or service.

When you add new servers, setting everything up in Grafana by hand &mdash; data source, dashboard, alert, notifications &mdash; takes time and gets annoying fast. 

This service does it for you. You just send one POST request, and it creates everything you need. 

Works with Ansible or any other tool you use to spin up new machines.

### How to use it?

1. Run Grafana and create a service account with an API key.  
2. Start this service and pass it the API key and Grafana URL.  
3. Create a server (e.g. in the cloud).  
4. Run your Ansible playbook &mdash; it installs Node Exporter and hits the service’s `/add_dashboard/<node>` endpoint.  
5. That’s it &mdash; Grafana now has:
   - a data source pointing to the new server
   - a simple dashboard
   - an alert rule
   - a contact point for notifications (e.g. Telegram)

No need to touch the Grafana UI at all.

---

## Requirements

- Grafana instance (functionality tested on v11.0.0)
- Node Exporter and Prometheus are installed on the target server and accessible from Grafana 

---

## API Endpoints

| Method | Endpoint                       | Description                           |
|--------|--------------------------------|---------------------------------------|
| POST   | `/add_dashboard/<node>[:port]` | Creates data source, dashboard, alert |
| POST   | `/check_dashboard/<node>`      | Checks if a dashboard exists          |
| GET    | `/health`                      | Health check                          |

---

## Usage

### Start the service

```bash
docker compose --env-file .env up --build
```

---

### Add a new dashboard

```http
POST /add_dashboard/<node>[:<prometheus-port>]
```

Example:
```bash
curl -X POST http://localhost:5000/add_dashboard/3.13.4.9:9090
```

Prometheus port is optional. If omitted, the default port 9090 will be used.

---

### Check if a dashboard exists

```http
POST /check_dashboard/<node>
```

Example:
```bash
curl -X POST http://localhost:5000/check_dashboard/3.13.4.9
```

Returns:
- `200 OK` &mdash; Dashboard exists
- `404 Not Found` &mdash; Not found

---

## Environment Variables

Make sure the following env vars are set in your `.env` file or via Docker:

| Variable             | Description                        |
|----------------------|------------------------------------|
| `SERVICE_PORT`       | Port where this service will run   |
| `GRAFANA_URL`        | URL of your Grafana instance       |
| `GRAFANA_API_KEY`    | Grafana API key with edit rights   |
| `TELEGRAM_BOT_TOKEN` | Token for Telegram alert contact   |
| `TELEGRAM_CHAT_ID`   | Telegram chat ID for notifications |

---

## Running Tests

To run tests:
```bash
docker compose -f docker-compose.yaml -f docker-compose-test-override.yaml up --build
```

---

## 🤝 Contributing
PRs welcome. If you spot a bug or have a feature request, feel free to open an issue.
