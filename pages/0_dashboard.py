import streamlit as st
from branding import render_header, render_footer, render_stat_card, render_action_card, render_status_badge, render_message_card, CUSTOM_CSS
from mqtt_client import get_subscriber, test_connection

render_header("MQTT Topic Manager")

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
# Dashboard
# ---------------------------------------------------------------------------
sub = get_subscriber()

# Stat cards row
c1, c2, c3, c4 = st.columns(4)
with c1:
    status_text = "Active" if sub.active else "Inactive"
    render_stat_card(status_text, "Subscriber")
with c2:
    render_stat_card(str(sub.get_message_count()), "Messages")
with c3:
    render_stat_card(sub.topic if sub.topic else "None", "Topic")
with c4:
    render_stat_card(f"{broker_host}:{int(broker_port)}", "Broker")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# Quick actions
st.markdown("### Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    render_action_card(
        "publish", "Publisher",
        "Publish messages to any MQTT topic with QoS and retain options. Supports plain text, JSON, and bulk publish.",
    )

with col2:
    render_action_card(
        "subscribe", "Subscriber",
        "Subscribe to topics with wildcard support. Messages are collected in the background across page switches.",
    )

with col3:
    render_action_card(
        "guide", "Topic Guide",
        "Use / as hierarchy separator, + for single-level wildcard, # for multi-level. Example: home/+/temperature",
    )

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# Recent messages preview
st.markdown("### Recent Messages")

messages = sub.get_messages()
if messages:
    for m in reversed(messages[-5:]):
        render_message_card(m.topic, m.payload, m.qos, m.retain, m.timestamp)
    if len(messages) > 5:
        st.caption(f"Showing last 5 of {len(messages)} messages. Open the Subscriber page for full view.")
else:
    st.info("No messages yet. Start the subscriber from the Subscriber page, then publish something.")

render_footer()
