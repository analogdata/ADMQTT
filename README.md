# MQTT Manager — Analog Data

A fully containerized MQTT management tool with a branded Streamlit UI. Includes an Eclipse Mosquitto broker and a web-based dashboard to publish, subscribe, and monitor MQTT topics — all running via Docker Compose.

![Analog Data](https://cdn.analogdata.ai/static/images/logo/ad_logo.png)

## Project Structure

```
myMQTT/
├── docker-compose.yaml          # Mosquitto broker + Streamlit app
├── Dockerfile                   # Streamlit app container image
├── requirements.txt             # Python dependencies
├── app.py                       # Streamlit navigation entrypoint
├── branding.py                  # Analog Data UI theme & components
├── mqtt_client.py               # MQTT publish/subscribe client logic
├── pages/
│   ├── 0_dashboard.py           # Dashboard — stats, quick actions
│   ├── 1_publisher.py           # Publisher — send messages to topics
│   └── 2_subscriber.py          # Subscriber — listen on topics
├── .streamlit/
│   └── config.toml              # Streamlit theme configuration
├── mosquitto/
│   ├── config/
│   │   └── mosquitto.conf       # Broker configuration
│   ├── data/                    # Persisted messages & retained data (auto-created)
│   └── log/                     # Broker log files (auto-created)
├── docs/
│   └── USAGE.md                 # Full usage guide (CLI, Python, ESP8266)
├── pyproject.toml               # Project metadata (uv)
└── README.md
```

---

## Quick Start (Docker — Recommended)

This is the easiest way to run the entire stack. Works on **Linux**, **macOS**, and **Windows**.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd myMQTT
```

### 2. Start Everything

```bash
docker compose up -d --build
```

This starts two containers:

| Container          | Service          | Port   |
|--------------------|------------------|--------|
| `mqtt_broker`      | Eclipse Mosquitto| `1883` (MQTT), `9001` (WebSocket) |
| `mqtt_manager_ui`  | Streamlit App    | `8501` |

### 3. Open the App

Open your browser and go to:

**http://localhost:8501**

### 4. Stop Everything

```bash
docker compose down
```

To also remove persisted broker data:

```bash
docker compose down -v
rm -rf mosquitto/data mosquitto/log
```

---

## Quick Start (Local Development)

If you prefer running without Docker (e.g., for development):

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### 1. Install Dependencies

```bash
uv sync
```

### 2. Start an MQTT Broker

Either start the Dockerized broker:

```bash
docker compose up mosquitto -d
```

Or use the public test broker (no setup needed) — the app defaults to `test.mosquitto.org`.

### 3. Run the App

```bash
uv run streamlit run app.py
```

The app opens at **http://localhost:8501**.

---

## Features

- **Dashboard** — Overview of subscriber status, message count, active topic, and broker info
- **Publisher** — Send messages to any MQTT topic with QoS (0/1/2) and retain options; supports plain text, JSON, and bulk publish
- **Subscriber** — Subscribe to topics with wildcard support (`+`, `#`); messages are collected in the background across page switches
- **Connection Test** — Verify broker connectivity from the sidebar
- **Branded UI** — Analog Data design system with Outfit font, amber/orange gradients, and responsive layout

## Broker Configuration

| Setting          | Default Value          |
|------------------|------------------------|
| Host             | `test.mosquitto.org`   |
| MQTT Port        | `1883`                 |
| WebSocket Port   | `9001`                 |
| Authentication   | Anonymous              |

The broker host and port can be changed from the sidebar on any page.

## Mosquitto Broker — Directory Structure

The `mosquitto/` directory contains all broker-related files. Docker Compose mounts these as volumes so data persists across container restarts.

```
mosquitto/
├── config/
│   └── mosquitto.conf    # Broker configuration (must exist before first run)
├── data/                 # Auto-created — stores retained messages & persistence DB
└── log/                  # Auto-created — stores mosquitto.log
```

### `mosquitto/config/mosquitto.conf`

This file **must exist** before running `docker compose up`. It configures the broker:

```conf
persistence true
persistence_location /mosquitto/data/

log_dest file /mosquitto/log/mosquitto.log
log_dest stdout

listener 1883
allow_anonymous true

listener 9001
protocol websockets
```

| Directive              | Description |
|------------------------|-------------|
| `persistence true`     | Enables message persistence — retained messages and subscriptions survive broker restarts |
| `persistence_location` | Path inside the container where persistence data is stored (mapped to `./mosquitto/data/` on host) |
| `log_dest file ...`    | Writes logs to a file inside the container (mapped to `./mosquitto/log/` on host) |
| `log_dest stdout`      | Also prints logs to Docker's stdout (viewable via `docker compose logs mosquitto`) |
| `listener 1883`        | Standard MQTT port for TCP connections |
| `allow_anonymous true` | Allows connections without username/password (disable in production) |
| `listener 9001` + `protocol websockets` | WebSocket listener for browser-based MQTT clients |

### `mosquitto/data/`

Auto-created on first run. Contains:
- `mosquitto.db` — persistence database (retained messages, subscriptions)

### `mosquitto/log/`

Auto-created on first run. Contains:
- `mosquitto.log` — broker log file

To view logs in real-time:

```bash
docker compose logs -f mosquitto
```

### First-Time Setup

If you're cloning fresh and the `data/` and `log/` directories don't exist, Docker will create them automatically. You only need to ensure the config file exists:

```bash
# Verify the config file is in place
cat mosquitto/config/mosquitto.conf
```

If it's missing, create it:

```bash
mkdir -p mosquitto/config
cat > mosquitto/config/mosquitto.conf << 'EOF'
persistence true
persistence_location /mosquitto/data/

log_dest file /mosquitto/log/mosquitto.log
log_dest stdout

listener 1883
allow_anonymous true

listener 9001
protocol websockets
EOF
```

Then start the stack:

```bash
docker compose up -d --build
```

## Documentation

See **[docs/USAGE.md](docs/USAGE.md)** for the full usage guide including:

- CLI publish & subscribe commands (`mosquitto_pub` / `mosquitto_sub`)
- Python publish & subscribe examples
- ESP8266 Arduino sketch with LED control and sensor publishing
- Topic design best practices
- Troubleshooting

---

## Built By

**[Analog Data](https://analogdata.io)** — Edge-to-Cloud Engineering
