import streamlit as st
import json
from branding import render_header, render_footer, render_status_badge, CUSTOM_CSS
from mqtt_client import publish_message, get_subscriber, test_connection

render_header("MQTT Publisher")

# ---------------------------------------------------------------------------
# Sidebar — Broker settings + subscriber status
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown("### Broker Settings")
    broker_host = st.text_input("Broker Host", value="test.mosquitto.org", key="broker_host")
    broker_port = st.number_input("Broker Port", value=1883, min_value=1, max_value=65535, key="broker_port")

    if st.button("Test Connection", use_container_width=True):
        ok, msg = test_connection(broker_host, int(broker_port))
        if ok:
            st.success(msg)
        else:
            st.error(msg)

    st.divider()
    sub = get_subscriber()
    if sub.active:
        render_status_badge(True, sub.topic)
        st.caption(f"{sub.get_message_count()} messages collected")
    else:
        render_status_badge(False)

# ---------------------------------------------------------------------------
# Publish form
# ---------------------------------------------------------------------------
col_form, col_history = st.columns([3, 2], gap="large")

with col_form:
    st.markdown("### Send a Message")

    pub_topic = st.text_input("Topic", value="test/topic", key="pub_topic",
                              help="MQTT topic path, e.g. `sensors/temperature`")

    opt1, opt2 = st.columns(2)
    with opt1:
        pub_qos = st.selectbox("QoS Level", options=[0, 1, 2], index=0, key="pub_qos",
                                format_func=lambda x: {0: "0 — At most once", 1: "1 — At least once", 2: "2 — Exactly once"}[x])
    with opt2:
        pub_retain = st.checkbox("Retain message", value=False, key="pub_retain",
                                 help="Broker stores the last retained message for new subscribers")

    pub_payload_type = st.radio("Payload type", ["Plain Text", "JSON"], horizontal=True, key="pub_type")

    if pub_payload_type == "JSON":
        pub_payload = st.text_area(
            "Payload (JSON)",
            value='{"temperature": 25.5, "unit": "C"}',
            height=150,
            key="pub_payload_json",
        )
    else:
        pub_payload = st.text_area(
            "Payload",
            value="Hello from Analog Data!",
            height=150,
            key="pub_payload_text",
        )

    if st.button("🚀 Publish", type="primary", use_container_width=True):
        if not pub_topic.strip():
            st.warning("Topic cannot be empty.")
        else:
            if pub_payload_type == "JSON":
                try:
                    json.loads(pub_payload)
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON: {e}")
                    st.stop()
            try:
                publish_message(broker_host, int(broker_port), pub_topic, pub_payload,
                                qos=pub_qos, retain=pub_retain)
                st.success(f"Published to **{pub_topic}**")
                # Track in history
                if "pub_history" not in st.session_state:
                    st.session_state.pub_history = []
                st.session_state.pub_history.insert(0, {
                    "topic": pub_topic,
                    "payload": pub_payload[:80],
                    "qos": pub_qos,
                    "retain": pub_retain,
                })
                # Keep last 20
                st.session_state.pub_history = st.session_state.pub_history[:20]
            except Exception as e:
                st.error(f"Publish failed: {e}")

with col_history:
    st.markdown("### Publish History")
    if "pub_history" in st.session_state and st.session_state.pub_history:
        for i, h in enumerate(st.session_state.pub_history):
            retain_tag = " 📌" if h["retain"] else ""
            st.markdown(
                f"""
                <div class="msg-card">
                    <div class="msg-topic">{h["topic"]}{retain_tag}</div>
                    <div class="msg-payload">{h["payload"]}</div>
                    <div class="msg-meta">QoS {h["qos"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if st.button("🗑 Clear History", use_container_width=True):
            st.session_state.pub_history = []
            st.rerun()
    else:
        st.caption("No messages published yet in this session.")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Bulk publish (collapsible)
# ---------------------------------------------------------------------------
with st.expander("📦 Bulk Publish — Send multiple messages at once"):
    bulk_default = json.dumps([
        {"topic": "sensors/temp", "payload": '{"value": 22.1}', "qos": 0, "retain": False},
        {"topic": "sensors/humidity", "payload": '{"value": 60}', "qos": 0, "retain": False},
        {"topic": "alerts/fire", "payload": "ALERT: smoke detected", "qos": 1, "retain": True},
    ], indent=2)

    bulk_json = st.text_area("Messages (JSON array)", value=bulk_default, height=200, key="bulk_json")

    if st.button("🚀 Bulk Publish", type="primary", use_container_width=True):
        try:
            items = json.loads(bulk_json)
            if not isinstance(items, list):
                st.error("Payload must be a JSON array.")
                st.stop()
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {e}")
            st.stop()

        progress = st.progress(0, text="Publishing…")
        success_count = 0
        for idx, item in enumerate(items):
            topic = item.get("topic", "")
            payload = item.get("payload", "")
            qos = item.get("qos", 0)
            retain = item.get("retain", False)
            if not topic:
                continue
            try:
                publish_message(broker_host, int(broker_port), topic, str(payload), qos=qos, retain=retain)
                success_count += 1
            except Exception as e:
                st.error(f"Item {idx + 1} ({topic}): {e}")
            progress.progress((idx + 1) / len(items), text=f"Published {idx + 1}/{len(items)}")

        st.success(f"Done — **{success_count}/{len(items)}** messages published.")

render_footer()
