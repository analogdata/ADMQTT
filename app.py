import streamlit as st

LOGO_URL = "https://cdn.analogdata.ai/static/images/logo/ad_logo.png"

# ---------------------------------------------------------------------------
# Navigation entrypoint — defines sidebar page names and icons
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MQTT Manager | Analog Data",
    page_icon=LOGO_URL,
    layout="wide",
)

dashboard = st.Page("pages/0_dashboard.py", title="Dashboard", icon="📊", default=True)
publisher = st.Page("pages/1_publisher.py", title="Publisher", icon="📤")
subscriber = st.Page("pages/2_subscriber.py", title="Subscriber", icon="📥")

nav = st.navigation([dashboard, publisher, subscriber])
nav.run()
