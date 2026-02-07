"""
Thread-safe MQTT client module shared across all Streamlit pages.
Uses a global singleton pattern so the background subscriber persists
across Streamlit reruns and page switches.
"""

import paho.mqtt.client as mqtt
import threading
import time
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class MQTTMessage:
    topic: str
    payload: str
    qos: int
    retain: bool
    timestamp: str


class MQTTSubscriber:
    """Persistent background MQTT subscriber with thread-safe message storage."""

    def __init__(self):
        self._client: mqtt.Client | None = None
        self._messages: list[MQTTMessage] = []
        self._lock = threading.Lock()
        self._active = False
        self._topic = ""
        self._error: str | None = None
        self._broker_host = ""
        self._broker_port = 1883

    @property
    def active(self) -> bool:
        return self._active

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def error(self) -> str | None:
        return self._error

    @property
    def broker_host(self) -> str:
        return self._broker_host

    @property
    def broker_port(self) -> int:
        return self._broker_port

    def get_messages(self) -> list[MQTTMessage]:
        with self._lock:
            return list(self._messages)

    def get_message_count(self) -> int:
        with self._lock:
            return len(self._messages)

    def clear_messages(self):
        with self._lock:
            self._messages.clear()

    def start(self, broker_host: str, broker_port: int, topic: str):
        """Start subscribing to a topic in the background."""
        self.stop()

        self._broker_host = broker_host
        self._broker_port = broker_port
        self._topic = topic
        self._error = None

        with self._lock:
            self._messages.clear()

        def on_connect(_client, _userdata, _flags, reason_code, _properties=None):
            if reason_code == 0 or str(reason_code) == "Success":
                _client.subscribe(topic)
                self._active = True
            else:
                self._error = f"Connect failed: {reason_code}"
                self._active = False

        def on_message(_client, _userdata, msg, _properties=None, _reason_code=None):
            m = MQTTMessage(
                topic=msg.topic,
                payload=msg.payload.decode("utf-8", errors="replace"),
                qos=msg.qos,
                retain=bool(msg.retain),
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            )
            with self._lock:
                self._messages.append(m)

        def on_disconnect(_client, _userdata, _flags, reason_code, _properties=None):
            if self._active:
                self._active = False

        try:
            self._client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=f"ad-subscriber-{int(time.time() * 1000) % 100000}",
                clean_session=True,
            )
            self._client.on_connect = on_connect
            self._client.on_message = on_message
            self._client.on_disconnect = on_disconnect
            self._client.connect(broker_host, broker_port, keepalive=60)
            self._client.loop_start()
            self._active = True
        except Exception as e:
            self._error = str(e)
            self._active = False

    def stop(self):
        """Stop the background subscriber."""
        if self._client is not None:
            try:
                self._client.loop_stop()
                self._client.disconnect()
            except Exception:
                pass
            self._client = None
        self._active = False


def publish_message(
    broker_host: str,
    broker_port: int,
    topic: str,
    payload: str,
    qos: int = 0,
    retain: bool = False,
):
    """Publish a single MQTT message (blocking, short-lived client)."""
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=f"ad-publisher-{int(time.time() * 1000) % 100000}",
        clean_session=True,
    )
    client.connect(broker_host, broker_port, keepalive=60)
    client.loop_start()
    info = client.publish(topic, payload, qos=qos, retain=retain)
    info.wait_for_publish()
    client.loop_stop()
    client.disconnect()


def test_connection(broker_host: str, broker_port: int) -> tuple[bool, str]:
    """Test broker connectivity. Returns (success, message)."""
    try:
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id="ad-test",
        )
        client.connect(broker_host, broker_port, keepalive=5)
        client.disconnect()
        return True, "Connected successfully!"
    except Exception as e:
        return False, f"Connection failed: {e}"


# ---------------------------------------------------------------------------
# Global singleton — survives Streamlit reruns and page navigation
# ---------------------------------------------------------------------------
_subscriber_instance: MQTTSubscriber | None = None
_subscriber_lock = threading.Lock()


def get_subscriber() -> MQTTSubscriber:
    """Return the global subscriber singleton."""
    global _subscriber_instance
    with _subscriber_lock:
        if _subscriber_instance is None:
            _subscriber_instance = MQTTSubscriber()
        return _subscriber_instance
