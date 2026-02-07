import streamlit as st
import time
from branding import (
    render_header, render_footer, render_status_badge,
    render_message_card, CUSTOM_CSS,
)
from mqtt_client import get_subscriber, test_connection

render_header("MQTT Subscriber")

# ---------------------------------------------------------------------------
# Sidebar — Broker settings
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
# Subscriber controls
# ---------------------------------------------------------------------------
sub = get_subscriber()

col_ctrl, col_status = st.columns([3, 2], gap="large")

with col_ctrl:
    st.markdown("### Subscription Settings")

    sub_topic = st.text_input(
        "Topic",
        value=sub.topic if sub.topic else "test/#",
        key="sub_topic",
        help="Supports MQTT wildcards: `+` (single level), `#` (multi level)",
        disabled=sub.active,
    )

    btn1, btn2 = st.columns(2)
    with btn1:
        start_clicked = st.button(
            "▶ Start Listening",
            type="primary",
            use_container_width=True,
            disabled=sub.active,
        )
    with btn2:
        stop_clicked = st.button(
            "⏹ Stop Listening",
            use_container_width=True,
            disabled=not sub.active,
        )

    if start_clicked:
        if not sub_topic.strip():
            st.warning("Topic cannot be empty.")
        else:
            sub.start(broker_host, int(broker_port), sub_topic)
            time.sleep(0.3)
            st.rerun()

    if stop_clicked:
        sub.stop()
        st.rerun()

with col_status:
    st.markdown("### Status")
    if sub.active:
        render_status_badge(True, sub.topic)
        st.markdown(
            f"""
            <div class="stat-card" style="margin-top:0.5rem;">
                <div class="stat-value">{sub.get_message_count()}</div>
                <div class="stat-label">Messages Received</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"Broker: `{sub.broker_host}:{sub.broker_port}`")
    else:
        render_status_badge(False)
        if sub.error:
            st.error(sub.error)
        st.caption("Click **Start Listening** to begin collecting messages.")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Message controls
# ---------------------------------------------------------------------------
st.markdown("### Messages")

ctrl1, ctrl2, ctrl3 = st.columns([1, 1, 2])
with ctrl1:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
with ctrl2:
    if st.button("🗑 Clear All", use_container_width=True):
        sub.clear_messages()
        st.rerun()
with ctrl3:
    auto_refresh = False
    if sub.active:
        auto_refresh = st.checkbox("Auto-refresh every 2s", value=False, key="auto_refresh")

# ---------------------------------------------------------------------------
# Message display
# ---------------------------------------------------------------------------
messages = sub.get_messages()
msg_count = len(messages)

if msg_count > 0:
    st.caption(f"**{msg_count}** message(s) — newest first")

    # Filter option
    filter_topic = st.text_input("Filter by topic (contains)", value="", key="msg_filter",
                                  placeholder="e.g. sensors")

    displayed = 0
    for m in reversed(messages):
        if filter_topic and filter_topic.lower() not in m.topic.lower():
            continue
        render_message_card(m.topic, m.payload, m.qos, m.retain, m.timestamp)
        displayed += 1
        if displayed >= 100:
            st.caption(f"Showing first 100 of {msg_count} messages. Use filter to narrow down.")
            break

    if displayed == 0 and filter_topic:
        st.info(f"No messages matching **{filter_topic}**")
else:
    if sub.active:
        st.info("Listening… No messages received yet. Publish something to see it here.")
    else:
        st.info("Start the subscriber to begin collecting messages.")

# ---------------------------------------------------------------------------
# Auto-refresh
# ---------------------------------------------------------------------------
if auto_refresh and sub.active:
    time.sleep(2)
    st.rerun()

render_footer()
