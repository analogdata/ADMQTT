"""
Analog Data branding — shared CSS and UI helpers for all pages.
Official design guidelines from https://analogdata.io
Font: Google Outfit
Theme: Light with amber/orange gradient accents
"""

import streamlit as st

# Brand colors — official Analog Data design guidelines
AMBER_500 = "#f59e0b"       # Primary gradient start
ORANGE_400 = "#fb923c"      # Gradient middle
AMBER_300 = "#fcd34d"       # Gradient end
AMBER_700 = "#b45309"       # Link hover, dark amber

SLATE_900 = "#0f172a"       # Primary text, dark backgrounds
SLATE_800 = "#1e293b"       # Secondary dark
SLATE_700 = "#334155"       # Tertiary dark
SLATE_600 = "#475569"       # Body text
SLATE_500 = "#64748b"       # Muted text
SLATE_400 = "#94a3b8"       # Placeholder text
SLATE_200 = "#e2e8f0"       # Light borders
SLATE_100 = "#f1f5f9"       # Light borders / bg
SLATE_50 = "#f8fafc"        # Light backgrounds

BRAND_DARK = "#0b0f19"      # Footer, dark hero
BRAND_LIGHT = "#f8fafc"     # Light sections

GREEN_500 = "#22c55e"       # Success
RED_500 = "#ef4444"         # Error
BLUE_500 = "#3b82f6"        # Info


CUSTOM_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* --- Apply Outfit globally --- */
    html, body, [class*="css"],
    .stMarkdown, .stMarkdown *, .stTextInput label, .stSelectbox label,
    .stNumberInput label, .stTextArea label, .stCheckbox label,
    .stRadio label, .stButton button, .stCaption,
    h1, h2, h3, h4, h5, h6, p, div, li, a, td, th,
    [data-testid="stSidebar"],
    [data-testid="stMainMenu"] {
        font-family: 'Outfit', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    /* --- Global background --- */
    .stApp {
        background: linear-gradient(to bottom right, #f8fafc, #ffffff, #fffbeb30);
    }

    /* --- Header bar --- */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 0;
        padding: 0.6rem 0 1.2rem 0;
        border-bottom: 2px solid #f1f5f9;
        margin-bottom: 1.8rem;
    }
    .brand-header .brand-logo-img {
        height: 36px;
        width: auto;
        flex-shrink: 0;
    }
    .brand-header .brand-separator {
        display: inline-block;
        width: 4px;
        height: 36px;
        border-radius: 9999px;
        background: linear-gradient(to bottom, #f59e0b, #fb923c, #fcd34d);
        transform: skewX(-15deg);
        box-shadow: 0 0 10px rgba(251, 146, 60, 0.6);
        margin: 0 12px;
        flex-shrink: 0;
    }
    .brand-header .brand-text {
        display: flex;
        flex-direction: column;
        gap: 0;
    }
    .brand-header .brand-name {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }
    .brand-header .brand-tagline {
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 400;
        letter-spacing: 0.5px;
        line-height: 1;
    }
    .brand-header .brand-page-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.85rem;
        color: #94a3b8;
        margin-left: auto;
        font-weight: 400;
        letter-spacing: 0.3px;
    }

    /* --- Stat cards --- */
    .stat-card {
        background: #ffffff;
        border: 1px solid #f1f5f9;
        border-top: 3px solid #f59e0b;
        border-radius: 16px;
        padding: 1.3rem 1rem;
        text-align: center;
        box-shadow: 0 4px 24px rgba(15, 23, 42, 0.06);
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        border-color: #fcd34d;
        box-shadow: 0 8px 30px rgba(245, 158, 11, 0.12);
        transform: translateY(-2px);
    }
    .stat-card .stat-value {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.3;
        word-break: break-all;
        overflow-wrap: break-word;
    }
    .stat-card .stat-label {
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 6px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* --- Message card --- */
    .msg-card {
        background: #ffffff;
        border: 1px solid #f1f5f9;
        border-left: 3px solid #f59e0b;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 2px 12px rgba(15, 23, 42, 0.04);
        transition: all 0.3s ease;
    }
    .msg-card:hover {
        border-left-color: #fb923c;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.1);
    }
    .msg-card .msg-topic {
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.9rem;
        color: #0f172a;
        font-weight: 600;
        letter-spacing: 0.2px;
    }
    .msg-card .msg-payload {
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
        font-size: 0.82rem;
        color: #334155;
        background: #f8fafc;
        padding: 8px 12px;
        border-radius: 8px;
        margin-top: 8px;
        word-break: break-all;
        border: 1px solid #f1f5f9;
    }
    .msg-card .msg-meta {
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.72rem;
        color: #94a3b8;
        margin-top: 6px;
        font-weight: 400;
    }

    /* --- Status badges (pill-brand style) --- */
    .badge-active {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f0fdf4;
        color: #16a34a;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'Outfit', sans-serif !important;
        border: 1px solid #bbf7d0;
        box-shadow: 0 1px 4px rgba(22, 163, 74, 0.08);
    }
    .badge-stopped {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #fef2f2;
        color: #dc2626;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'Outfit', sans-serif !important;
        border: 1px solid #fecaca;
        box-shadow: 0 1px 4px rgba(220, 38, 38, 0.06);
    }

    /* --- Topic chip (pill-brand) --- */
    .topic-chip {
        display: inline-flex;
        align-items: center;
        background: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
        padding: 4px 14px;
        border-radius: 9999px;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        margin: 2px 4px 2px 0;
        box-shadow: 0 1px 3px rgba(245, 158, 11, 0.08);
    }

    /* --- Section divider --- */
    .section-divider {
        border: none;
        border-top: 1px solid #f1f5f9;
        margin: 1.8rem 0;
    }

    /* --- Footer (dark section) --- */
    .brand-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.75rem;
        font-family: 'Outfit', sans-serif !important;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid #f1f5f9;
        margin-top: 2.5rem;
    }
    .brand-footer a {
        color: #b45309;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    .brand-footer a:hover {
        color: #f59e0b;
    }

    /* Hide default Streamlit footer */
    footer {visibility: hidden;}

    /* --- Sidebar --- */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #f1f5f9;
    }


    /* --- Streamlit button overrides --- */
    .stButton > button[kind="primary"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600;
        background: linear-gradient(to right, #f59e0b, #fb923c, #fcd34d) !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button[kind="primary"]:hover {
        filter: brightness(1.1);
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
    }
    .stButton > button:not([kind="primary"]) {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600;
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        color: #334155 !important;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    .stButton > button:not([kind="primary"]):hover {
        border-color: #f59e0b !important;
        color: #0f172a !important;
        transform: scale(1.02);
    }

    /* --- Input fields --- */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        font-family: 'Outfit', sans-serif !important;
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        color: #0f172a !important;
        border-radius: 12px !important;
        transition: all 0.2s ease;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 0 1px #f59e0b !important;
    }

    /* --- Selectbox --- */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }

    /* --- Expander --- */
    .streamlit-expanderHeader {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600;
        color: #0f172a;
        background-color: #ffffff;
        border-radius: 12px;
    }

    /* --- Headings --- */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #0f172a;
    }
    .stMarkdown h1 { font-weight: 700; }
    .stMarkdown h2 { font-weight: 700; }
    .stMarkdown h3 {
        font-weight: 600;
        font-size: 1.2rem;
        color: #0f172a;
    }

    /* --- Captions --- */
    .stCaption, [data-testid="stCaptionContainer"] {
        font-family: 'Outfit', sans-serif !important;
        color: #64748b !important;
        font-size: 0.85rem;
    }

    /* --- Info / success / error boxes --- */
    .stAlert {
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* --- Body text readability --- */
    .stMarkdown p, .stMarkdown li {
        font-family: 'Outfit', sans-serif !important;
        color: #475569;
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.7;
    }

    /* --- Labels --- */
    .stTextInput label p, .stTextArea label p,
    .stNumberInput label p, .stSelectbox label p,
    .stCheckbox label p, .stRadio label p {
        font-family: 'Outfit', sans-serif !important;
        color: #334155 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }

    /* --- Sidebar text --- */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        font-family: 'Outfit', sans-serif !important;
        color: #334155 !important;
    }

    /* --- Sidebar nav links --- */
    [data-testid="stSidebarNav"] a {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* --- Action card (for dashboard) --- */
    .action-card {
        background: #ffffff;
        border: 1px solid #f1f5f9;
        border-radius: 16px;
        padding: 1.5rem 1.2rem;
        box-shadow: 0 4px 24px rgba(15, 23, 42, 0.06);
        transition: all 0.3s ease;
        text-align: center;
    }
    .action-card:hover {
        border-color: #fcd34d;
        box-shadow: 0 8px 30px rgba(245, 158, 11, 0.12);
        transform: translateY(-2px);
    }
    .action-card .action-icon-wrap {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 12px;
        margin-bottom: 0.8rem;
    }
    .action-card .action-icon-wrap.publish {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
    }
    .action-card .action-icon-wrap.subscribe {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
    }
    .action-card .action-icon-wrap.guide {
        background: linear-gradient(135deg, #f3e8ff, #e9d5ff);
    }
    .action-card .action-icon-wrap svg {
        width: 22px;
        height: 22px;
    }
    .action-card .action-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.05rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .action-card .action-desc {
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.82rem;
        color: #64748b;
        margin-top: 4px;
        font-weight: 400;
        line-height: 1.6;
    }
</style>
"""


LOGO_URL = "https://cdn.analogdata.ai/static/images/logo/ad_logo.png"


def render_header(subtitle: str = "MQTT Topic Manager"):
    """Render the Analog Data branded header matching analogdata.io style."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="brand-header">
            <img src="{LOGO_URL}" alt="Analog Data" class="brand-logo-img" />
            <span class="brand-separator"></span>
            <div class="brand-text">
                <span class="brand-name">Analog Data</span>
                <span class="brand-tagline">IoT &amp; Embedded</span>
            </div>
            <div class="brand-page-title">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_logo():
    """Render the Analog Data logo at the top of the sidebar."""
    st.image(LOGO_URL, width=120)
    st.markdown('<hr class="section-divider" style="margin:0.5rem 0 1rem 0;">', unsafe_allow_html=True)


def render_footer():
    """Render the branded footer."""
    st.markdown(
        """
        <div class="brand-footer">
            Built by <a href="https://analogdata.io" target="_blank">Analog Data</a>
            &nbsp;·&nbsp; Edge-to-Cloud Engineering
            &nbsp;·&nbsp; © 2026
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(value: str, label: str):
    """Render a stat card with gradient value text."""
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# SVG icons for action cards (inline, no external dependencies)
_ACTION_ICONS = {
    "publish": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#b45309"><path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" /></svg>',
    "subscribe": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#1d4ed8"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 0 1 2.012 1.244l.256.512a2.25 2.25 0 0 0 2.013 1.244h3.218a2.25 2.25 0 0 0 2.013-1.244l.256-.512a2.25 2.25 0 0 1 2.013-1.244h3.859m-19.5.338V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 0 0-2.15-1.588H6.911a2.25 2.25 0 0 0-2.15 1.588L2.35 13.177a2.25 2.25 0 0 0-.1.661Z" /></svg>',
    "guide": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#7c3aed"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" /></svg>',
}


def render_action_card(icon_key: str, title: str, description: str):
    """Render a dashboard action card with SVG icon."""
    svg = _ACTION_ICONS.get(icon_key, "")
    icon_class = icon_key if icon_key in _ACTION_ICONS else "publish"
    st.markdown(
        f"""
        <div class="action-card">
            <div class="action-icon-wrap {icon_class}">{svg}</div>
            <div class="action-title">{title}</div>
            <div class="action-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_message_card(topic: str, payload: str, qos: int, retain: bool, timestamp: str):
    """Render a single MQTT message card."""
    retain_badge = " · 📌 retained" if retain else ""
    st.markdown(
        f"""
        <div class="msg-card">
            <div class="msg-topic">{topic}</div>
            <div class="msg-payload">{payload}</div>
            <div class="msg-meta">QoS {qos}{retain_badge} · {timestamp}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_badge(active: bool, topic: str = ""):
    """Render an active/stopped status badge (pill style)."""
    if active:
        st.markdown(
            f'<span class="badge-active">● Listening on {topic}</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="badge-stopped">● Stopped</span>',
            unsafe_allow_html=True,
        )


def render_topic_chip(topic: str):
    """Render a topic as a styled pill chip."""
    st.markdown(
        f'<span class="topic-chip">{topic}</span>',
        unsafe_allow_html=True,
    )
