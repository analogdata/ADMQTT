# MQTT Usage Guide

Complete guide for publishing, subscribing, and integrating with the MQTT broker — via CLI, Python, Streamlit UI, and ESP8266.

---

## Table of Contents

- [1. Prerequisites](#1-prerequisites)
- [2. Start the Broker](#2-start-the-broker)
- [3. CLI — Publish & Subscribe](#3-cli--publish--subscribe)
- [4. Python — Publish & Subscribe](#4-python--publish--subscribe)
- [5. Streamlit UI](#5-streamlit-ui)
- [6. ESP8266 Arduino Sketch](#6-esp8266-arduino-sketch)
- [7. Topic Design Best Practices](#7-topic-design-best-practices)
- [8. Troubleshooting](#8-troubleshooting)

---

## 1. Prerequisites

| Tool | Purpose |
|------|---------|
| Docker & Docker Compose | Run the Mosquitto MQTT broker |
| `mosquitto_pub` / `mosquitto_sub` | CLI publish & subscribe (install via `sudo apt install mosquitto-clients`) |
| Python 3.13+ & `uv` | Run the Streamlit app and Python scripts |
| Arduino IDE | Flash ESP8266 sketches |

### Install Mosquitto CLI clients

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y mosquitto-clients

# macOS
brew install mosquitto

# Verify
mosquitto_pub --help
mosquitto_sub --help
```

---

## 2. Start the Broker

```bash
# Start Mosquitto in the background
docker compose up -d

# Verify it's running
docker ps | grep mqtt_broker

# View broker logs
docker logs -f mqtt_broker
```

**Broker defaults:**

| Setting | Value |
|---------|-------|
| Host | `localhost` (or your machine's IP for remote devices) |
| MQTT Port | `1883` |
| WebSocket Port | `9001` |
| Auth | Anonymous (no username/password) |

---

## 3. CLI — Publish & Subscribe

### 3.1 Subscribe to a topic

Open a terminal and start listening:

```bash
# Subscribe to a single topic
mosquitto_sub -h localhost -p 1883 -t "sensors/temperature"

# Subscribe with wildcard — all topics under sensors/
mosquitto_sub -h localhost -p 1883 -t "sensors/#"

# Subscribe to ALL topics on the broker
mosquitto_sub -h localhost -p 1883 -t "#"

# Subscribe with verbose output (shows topic name with each message)
mosquitto_sub -h localhost -p 1883 -t "sensors/#" -v
```

### 3.2 Publish a message

Open another terminal:

```bash
# Publish a simple text message
mosquitto_pub -h localhost -p 1883 -t "sensors/temperature" -m "25.5"

# Publish a JSON payload
mosquitto_pub -h localhost -p 1883 -t "sensors/temperature" -m '{"value": 25.5, "unit": "C"}'

# Publish with QoS 1 (at least once delivery)
mosquitto_pub -h localhost -p 1883 -t "sensors/temperature" -m "25.5" -q 1

# Publish with QoS 2 (exactly once delivery)
mosquitto_pub -h localhost -p 1883 -t "alerts/fire" -m "SMOKE DETECTED" -q 2

# Publish a retained message (new subscribers get the last retained message immediately)
mosquitto_pub -h localhost -p 1883 -t "device/status" -m "online" -r

# Clear a retained message (publish empty payload with retain flag)
mosquitto_pub -h localhost -p 1883 -t "device/status" -m "" -r
```

### 3.3 QoS Levels Explained

| QoS | Name | Guarantee |
|-----|------|-----------|
| 0 | At most once | Fire and forget — fastest, no acknowledgment |
| 1 | At least once | Acknowledged delivery — may receive duplicates |
| 2 | Exactly once | Four-step handshake — slowest, guaranteed single delivery |

### 3.4 Wildcards

| Wildcard | Meaning | Example |
|----------|---------|---------|
| `+` | Single level | `sensors/+/temperature` matches `sensors/room1/temperature` |
| `#` | Multi level (must be last) | `sensors/#` matches `sensors/temperature`, `sensors/room1/humidity`, etc. |

### 3.5 Docker Exec — No Host Install Needed

If you don't have `mosquitto_pub` / `mosquitto_sub` installed on your host machine, you can run them **directly inside the Docker container**. The container name is `mqtt_broker` (defined in `docker-compose.yaml`).

#### Subscribe via Docker

```bash
# Subscribe to a single topic
docker compose exec mosquitto mosquitto_sub -h localhost -p 1883 -t "sensors/temperature"

# Subscribe with wildcard — all topics under sensors/
docker compose exec mosquitto mosquitto_sub -h localhost -p 1883 -t "sensors/#"

# Subscribe to ALL topics (verbose)
docker compose exec mosquitto mosquitto_sub -h localhost -p 1883 -t "#" -v
```

#### Publish via Docker

```bash
# Publish a simple text message
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "sensors/temperature" -m "25.5"

# Publish a JSON payload
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "sensors/temperature" -m '{"value": 25.5, "unit": "C"}'

# Publish with QoS 1
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "sensors/temperature" -m "25.5" -q 1

# Publish with QoS 2
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "alerts/fire" -m "SMOKE DETECTED" -q 2

# Publish a retained message
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "device/status" -m "online" -r

# Clear a retained message
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "device/status" -m "" -r
```

#### Robot control example (via Docker)

```bash
# Send forward command to a robot
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "robot/F" -m "S"

# Send other movement commands
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "robot/direction" -m "FORWARD"
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "robot/direction" -m "LEFT"
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "robot/direction" -m "STOP"
docker compose exec mosquitto mosquitto_pub -h localhost -p 1883 -t "robot/speed" -m '{"value": 150}'

# Subscribe to robot status from the container
docker compose exec mosquitto mosquitto_sub -h localhost -p 1883 -t "robot/#" -v
```

> **Note:** Inside the container, `localhost` refers to the container itself (where Mosquitto is running), so `-h localhost` works correctly. You can also use the container service name `mosquitto` as the host.

### 3.6 Full example session

```bash
# Terminal 1 — Subscribe
mosquitto_sub -h localhost -p 1883 -t "home/#" -v

# Terminal 2 — Publish multiple messages
mosquitto_pub -h localhost -p 1883 -t "home/livingroom/temp" -m '{"value": 23.1}'
mosquitto_pub -h localhost -p 1883 -t "home/bedroom/temp" -m '{"value": 19.8}'
mosquitto_pub -h localhost -p 1883 -t "home/kitchen/humidity" -m '{"value": 55}'
mosquitto_pub -h localhost -p 1883 -t "home/door/status" -m "locked" -r
```

Terminal 1 output:

```
home/livingroom/temp {"value": 23.1}
home/bedroom/temp {"value": 19.8}
home/kitchen/humidity {"value": 55}
home/door/status locked
```

---

## 4. Python — Publish & Subscribe

### 4.1 Install dependencies

```bash
uv sync
```

### 4.2 Publish from Python

```python
import paho.mqtt.client as mqtt
import json
import time

# --- Configuration ---
BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Create an MQTT client (paho-mqtt v2 API)
client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"python-pub-{int(time.time())}",
)

# Connect to the broker
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

# --- Publish a plain text message ---
client.publish("sensors/temperature", "25.5", qos=0)

# --- Publish a JSON message ---
payload = json.dumps({"temperature": 25.5, "humidity": 60, "unit": "C"})
client.publish("sensors/environment", payload, qos=1)

# --- Publish a retained message ---
client.publish("device/esp01/status", "online", qos=1, retain=True)

# Disconnect
client.disconnect()
print("Messages published.")
```

### 4.3 Subscribe from Python

```python
import paho.mqtt.client as mqtt
import time

# --- Configuration ---
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "sensors/#"  # Subscribe to all sensor topics

# --- Callback: fires when connected ---
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result: {reason_code}")
    # Subscribe after connecting (auto-resubscribe on reconnect)
    client.subscribe(TOPIC)
    print(f"Subscribed to: {TOPIC}")

# --- Callback: fires when a message is received ---
def on_message(client, userdata, msg):
    print(f"[{msg.topic}] (QoS {msg.qos}) → {msg.payload.decode()}")

# Create client
client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"python-sub-{int(time.time())}",
)

# Attach callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect and start the loop (blocking)
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

try:
    # loop_forever() blocks and handles reconnects automatically
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDisconnecting...")
    client.disconnect()
```

### 4.4 Run the scripts

```bash
# In one terminal — start the subscriber
uv run python subscribe_example.py

# In another terminal — publish
uv run python publish_example.py
```

---

## 5. Streamlit UI

```bash
uv run streamlit run app.py
```

Opens at **http://localhost:8501** with three tabs:

| Tab | What it does |
|-----|-------------|
| **Publish** | Send a message to any topic (plain text or JSON), choose QoS (0/1/2), toggle retain |
| **Subscribe** | Listen on a topic (wildcards supported) for N seconds, view received messages |
| **Bulk Publish** | Paste a JSON array of messages and publish them all at once |

Use the **sidebar** to change broker host/port and test connectivity.

---

## 6. ESP8266 Arduino Sketch

This sketch connects an ESP8266 (e.g., NodeMCU, Wemos D1 Mini) to your MQTT broker. It:

- Publishes temperature and humidity readings every 5 seconds
- Subscribes to a command topic to receive LED on/off commands
- Reconnects automatically if the connection drops

### 6.1 Arduino IDE Setup

1. **Add ESP8266 board support** — In Arduino IDE, go to `File > Preferences` and add this URL to *Additional Board Manager URLs*:

   ```
   http://arduino.esp8266.com/stable/package_esp8266com_index.json
   ```

2. **Install the board** — Go to `Tools > Board > Boards Manager`, search for `esp8266`, and install **esp8266 by ESP8266 Community**.

3. **Install PubSubClient library** — Go to `Sketch > Include Library > Manage Libraries`, search for `PubSubClient` by Nick O'Leary, and install it.

4. **Select your board** — `Tools > Board > ESP8266 Boards > NodeMCU 1.0 (ESP-12E Module)` (or your specific board).

### 6.2 Full Sketch

```cpp
/*
 * ESP8266 MQTT Client
 * --------------------
 * Publishes sensor data and subscribes to commands.
 *
 * Hardware:
 *   - ESP8266 (NodeMCU / Wemos D1 Mini)
 *   - Built-in LED on GPIO2 (D4 on NodeMCU)
 *
 * Libraries:
 *   - ESP8266WiFi (built-in with ESP8266 board package)
 *   - PubSubClient by Nick O'Leary (install via Library Manager)
 *
 * Topics:
 *   PUBLISH:   home/esp8266/temperature   → simulated temp reading
 *              home/esp8266/humidity       → simulated humidity reading
 *              home/esp8266/status         → "online" (retained, on connect)
 *   SUBSCRIBE: home/esp8266/led/command   → "ON" or "OFF" to control LED
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// ======================== CONFIGURATION ========================
// WiFi credentials
const char* WIFI_SSID     = "YOUR_WIFI_SSID";      // <-- Change this
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";   // <-- Change this

// MQTT broker settings
// Use your computer's local IP (not "localhost" — ESP8266 is a separate device)
// Find it with: hostname -I (Linux) or ipconfig (Windows) or ifconfig (macOS)
const char* MQTT_BROKER   = "192.168.1.100";        // <-- Change this to your PC's IP
const int   MQTT_PORT     = 1883;
const char* MQTT_CLIENT_ID = "esp8266-client-01";

// MQTT topics
const char* TOPIC_TEMPERATURE = "home/esp8266/temperature";
const char* TOPIC_HUMIDITY    = "home/esp8266/humidity";
const char* TOPIC_STATUS      = "home/esp8266/status";
const char* TOPIC_LED_CMD     = "home/esp8266/led/command";

// Publish interval (milliseconds)
const unsigned long PUBLISH_INTERVAL = 5000;  // 5 seconds

// LED pin (built-in LED on most ESP8266 boards)
const int LED_PIN = LED_BUILTIN;  // GPIO2 (D4 on NodeMCU) — active LOW
// ===============================================================

WiFiClient espClient;
PubSubClient mqttClient(espClient);

unsigned long lastPublishTime = 0;

// ---------------------------------------------------------------
// Connect to WiFi
// ---------------------------------------------------------------
void setupWifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);           // Station mode (client)
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Wait until connected
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("WiFi connected — IP: ");
  Serial.println(WiFi.localIP());
}

// ---------------------------------------------------------------
// MQTT message callback — fires when a subscribed message arrives
// ---------------------------------------------------------------
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  // Convert payload bytes to a String
  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Message received [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(message);

  // Handle LED commands
  if (String(topic) == TOPIC_LED_CMD) {
    if (message == "ON") {
      digitalWrite(LED_PIN, LOW);   // Active LOW — LED turns ON
      Serial.println("LED → ON");
    } else if (message == "OFF") {
      digitalWrite(LED_PIN, HIGH);  // Active LOW — LED turns OFF
      Serial.println("LED → OFF");
    } else {
      Serial.println("Unknown command. Use ON or OFF.");
    }
  }
}

// ---------------------------------------------------------------
// Connect (or reconnect) to the MQTT broker
// ---------------------------------------------------------------
void reconnectMqtt() {
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT broker...");

    // Attempt connection with a Last Will and Testament (LWT)
    // If the ESP8266 disconnects unexpectedly, the broker publishes "offline"
    bool connected = mqttClient.connect(
      MQTT_CLIENT_ID,
      NULL,                    // username (NULL = anonymous)
      NULL,                    // password
      TOPIC_STATUS,            // LWT topic
      1,                       // LWT QoS
      true,                    // LWT retain
      "offline"                // LWT message
    );

    if (connected) {
      Serial.println(" connected!");

      // Publish online status (retained)
      mqttClient.publish(TOPIC_STATUS, "online", true);

      // Subscribe to the LED command topic
      mqttClient.subscribe(TOPIC_LED_CMD);
      Serial.print("Subscribed to: ");
      Serial.println(TOPIC_LED_CMD);

    } else {
      Serial.print(" failed (rc=");
      Serial.print(mqttClient.state());
      Serial.println("). Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

// ---------------------------------------------------------------
// Simulate sensor readings (replace with real sensor code)
// ---------------------------------------------------------------
float readTemperature() {
  // Simulated: random value between 20.0 and 30.0
  return 20.0 + (random(0, 100) / 10.0);
}

float readHumidity() {
  // Simulated: random value between 40.0 and 70.0
  return 40.0 + (random(0, 300) / 10.0);
}

// ---------------------------------------------------------------
// Arduino setup — runs once
// ---------------------------------------------------------------
void setup() {
  Serial.begin(115200);

  // Configure LED pin
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);  // Start with LED off (active LOW)

  // Connect to WiFi
  setupWifi();

  // Configure MQTT
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
}

// ---------------------------------------------------------------
// Arduino loop — runs repeatedly
// ---------------------------------------------------------------
void loop() {
  // Reconnect if disconnected
  if (!mqttClient.connected()) {
    reconnectMqtt();
  }

  // Process incoming messages and maintain the connection
  mqttClient.loop();

  // Publish sensor data at the defined interval
  unsigned long now = millis();
  if (now - lastPublishTime >= PUBLISH_INTERVAL) {
    lastPublishTime = now;

    // Read sensors
    float temperature = readTemperature();
    float humidity    = readHumidity();

    // Build JSON payloads
    char tempPayload[64];
    snprintf(tempPayload, sizeof(tempPayload),
             "{\"value\": %.1f, \"unit\": \"C\"}", temperature);

    char humPayload[64];
    snprintf(humPayload, sizeof(humPayload),
             "{\"value\": %.1f, \"unit\": \"%%\"}", humidity);

    // Publish
    mqttClient.publish(TOPIC_TEMPERATURE, tempPayload);
    mqttClient.publish(TOPIC_HUMIDITY, humPayload);

    Serial.print("Published — Temp: ");
    Serial.print(tempPayload);
    Serial.print(" | Humidity: ");
    Serial.println(humPayload);
  }
}
```

### 6.3 Configuration Checklist

Before uploading, update these three values in the sketch:

```cpp
const char* WIFI_SSID     = "YOUR_WIFI_SSID";      // Your WiFi network name
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";   // Your WiFi password
const char* MQTT_BROKER   = "192.168.1.100";        // Your PC's local IP address
```

Find your PC's local IP:

```bash
# Linux
hostname -I

# macOS
ipconfig getifaddr en0

# Windows
ipconfig
```

### 6.4 Test the ESP8266

After uploading the sketch, open the Arduino Serial Monitor (115200 baud) to see connection status and published data.

**Subscribe to ESP8266 data from your PC:**

```bash
# See all ESP8266 messages
mosquitto_sub -h localhost -p 1883 -t "home/esp8266/#" -v
```

Expected output:

```
home/esp8266/status online
home/esp8266/temperature {"value": 24.3, "unit": "C"}
home/esp8266/humidity {"value": 55.2, "unit": "%"}
home/esp8266/temperature {"value": 23.8, "unit": "C"}
home/esp8266/humidity {"value": 57.1, "unit": "%"}
```

**Send LED commands to the ESP8266:**

```bash
# Turn the LED on
mosquitto_pub -h localhost -p 1883 -t "home/esp8266/led/command" -m "ON"

# Turn the LED off
mosquitto_pub -h localhost -p 1883 -t "home/esp8266/led/command" -m "OFF"
```

### 6.5 Using a Real DHT11/DHT22 Sensor

To use a real temperature/humidity sensor instead of simulated values:

1. Install the **DHT sensor library** by Adafruit from the Library Manager.
2. Replace the simulated functions:

```cpp
#include <DHT.h>

#define DHT_PIN D2          // GPIO4 — data pin of the DHT sensor
#define DHT_TYPE DHT22      // DHT11 or DHT22

DHT dht(DHT_PIN, DHT_TYPE);

// Call dht.begin() in setup()

float readTemperature() {
  float t = dht.readTemperature();  // Celsius
  if (isnan(t)) {
    Serial.println("DHT read error (temp)");
    return -1;
  }
  return t;
}

float readHumidity() {
  float h = dht.readHumidity();
  if (isnan(h)) {
    Serial.println("DHT read error (humidity)");
    return -1;
  }
  return h;
}
```

---

## 7. Topic Design Best Practices

```
<domain>/<device-or-location>/<measurement-or-action>
```

| Example Topic | Use Case |
|---------------|----------|
| `home/livingroom/temperature` | Room temperature sensor |
| `home/livingroom/light/command` | Control a smart light |
| `home/livingroom/light/status` | Light reports its state |
| `factory/line1/motor/rpm` | Industrial motor speed |
| `fleet/truck-42/gps` | Vehicle GPS coordinates |

**Rules:**

- Use `/` as a hierarchy separator
- Keep topics lowercase
- Avoid leading `/` (e.g., use `home/temp` not `/home/temp`)
- Use `command` suffix for control topics, `status` for state reports
- Use `#` wildcard sparingly — subscribing to `#` on a busy broker can flood your client

---

## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `Connection refused` | Is the broker running? Check `docker ps` |
| ESP8266 can't connect | Use your PC's **local IP** (not `localhost`). Ensure both are on the same WiFi network |
| No messages received | Verify the topic matches exactly (topics are case-sensitive). Check wildcards |
| `mosquitto_pub: command not found` | Install clients: `sudo apt install mosquitto-clients` |
| Retained messages won't clear | Publish an empty message with retain: `mosquitto_pub -t "topic" -m "" -r` |
| Broker logs show errors | Check: `docker logs mqtt_broker` |
| ESP8266 disconnects frequently | Increase `keepalive`, check WiFi signal strength, ensure stable power supply |
