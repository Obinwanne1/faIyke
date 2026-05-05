import streamlit as st
from dotenv import load_dotenv
import os
from agents import AGENT_META, run_agent

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="faIyke Agent Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state ─────────────────────────────────────────────────────────────
if "histories" not in st.session_state:
    st.session_state.histories = {k: [] for k in AGENT_META}
if "active_agent" not in st.session_state:
    st.session_state.active_agent = "master-agent"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark = st.session_state.dark_mode

# ── Theme vars ────────────────────────────────────────────────────────────────
if dark:
    css_vars = """
    --green:       #2eaa0e;
    --green2:      #38cc10;
    --white:       #e8f5e3;
    --bg:          #111612;
    --surface:     #1a2118;
    --border:      #2a3d24;
    --text:        #e8f5e3;
    --text-muted:  #7a9870;
    --bubble-agent-bg:   #1e2b1a;
    --bubble-agent-text: #e8f5e3;
    """
else:
    css_vars = """
    --green:       #227309;
    --green2:      #2e9a0c;
    --white:       #FFFFFF;
    --bg:          #f4f7f3;
    --surface:     #ffffff;
    --border:      #c5d9c0;
    --text:        #1a1a1a;
    --text-muted:  #555;
    --bubble-agent-bg:   #ffffff;
    --bubble-agent-text: #1a1a1a;
    """

st.markdown(f"""
<style>
:root {{ {css_vars} }}

html, body, [class*="css"] {{
    font-family: 'Segoe UI', sans-serif;
    color: var(--text);
}}
.stApp {{ background: var(--bg) !important; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: var(--green) !important;
    border-right: 3px solid var(--green2);
}}
[data-testid="stSidebar"] * {{ color: #ffffff !important; }}
[data-testid="stSidebar"] .stRadio label {{
    background: rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0;
    cursor: pointer;
    transition: background 0.2s;
    display: block;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(255,255,255,0.20);
}}

/* Agent header */
.agent-header {{
    background: var(--green);
    color: #ffffff;
    padding: 16px 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 14px;
}}
.agent-header h2 {{ margin: 0; font-size: 1.4rem; }}
.agent-header p  {{ margin: 2px 0 0; opacity: 0.82; font-size: 0.88rem; }}

/* Chat bubbles */
.msg-user {{
    background: var(--green);
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 12px 12px 4px 12px;
    margin: 8px 0;
    max-width: 80%;
    margin-left: auto;
    word-break: break-word;
}}
.msg-agent {{
    background: var(--bubble-agent-bg);
    color: var(--bubble-agent-text);
    padding: 12px 16px;
    border-radius: 12px 12px 12px 4px;
    margin: 8px 0;
    max-width: 85%;
    border: 1px solid var(--border);
    word-break: break-word;
    white-space: pre-wrap;
}}
.msg-label {{
    font-size: 0.70rem;
    font-weight: 700;
    color: var(--green);
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
.chat-wrap {{ padding: 6px 0; }}

/* Buttons */
.stButton > button {{
    background: var(--green) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: background 0.2s !important;
}}
.stButton > button:hover {{ background: var(--green2) !important; }}

/* Input */
.stTextArea textarea {{
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
}}
.stTextArea textarea:focus {{
    border-color: var(--green) !important;
    box-shadow: 0 0 0 2px rgba(34,115,9,0.18) !important;
}}

/* API warning */
.api-warn {{
    background: {'#1e1a0a' if dark else '#fff8e1'};
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 16px;
    font-size: 0.88rem;
    color: {'#f5c842' if dark else '#78350f'};
}}

/* Empty chat placeholder */
.chat-empty {{
    text-align: center;
    color: var(--text-muted);
    padding: 40px 0;
}}

#MainMenu, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 faIyke Agents")
    st.markdown("---")

    options = list(AGENT_META.keys())
    labels  = [f"{AGENT_META[k]['icon']}  {AGENT_META[k]['label']}" for k in options]
    choice  = st.radio("Select Agent", labels, index=options.index(st.session_state.active_agent))
    st.session_state.active_agent = options[labels.index(choice)]

    st.markdown("---")

    # Dark mode toggle
    toggle_label = "☀️  Light mode" if dark else "🌙  Dark mode"
    if st.button(toggle_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("---")

    key_status = "✅ API key loaded" if API_KEY else "⚠️ No API key found"
    st.markdown(f"<div style='font-size:0.8rem;opacity:0.85'>{key_status}</div>", unsafe_allow_html=True)
    if not API_KEY:
        st.markdown(
            "<div style='font-size:0.75rem;opacity:0.7;margin-top:4px'>"
            "Add ANTHROPIC_API_KEY to dashboard/.env</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;opacity:0.55;text-align:center'>"
        "faIyke Multi-Agent System<br>Powered by Claude</div>",
        unsafe_allow_html=True,
    )


# ── Main ──────────────────────────────────────────────────────────────────────
agent_key  = st.session_state.active_agent
agent_info = AGENT_META[agent_key]
history    = st.session_state.histories[agent_key]

if not API_KEY:
    st.markdown("""
<div class="api-warn">
    <strong>API key required.</strong> Claude Code Pro and the Anthropic API are separate products.
    Add your key to <code>dashboard/.env</code>:<br><br>
    <code>ANTHROPIC_API_KEY=sk-ant-your-key-here</code><br><br>
    Get a key at <strong>console.anthropic.com</strong>, then restart the dashboard.
</div>
""", unsafe_allow_html=True)

# Agent header
st.markdown(f"""
<div class="agent-header">
    <div style="font-size:2rem">{agent_info['icon']}</div>
    <div>
        <h2>{agent_info['label']}</h2>
        <p>{agent_info['desc']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Skills + clear
col1, col2 = st.columns([4, 1])
with col1:
    skills = AGENT_META[agent_key]["skills"]
    if skills:
        tags = " ".join([
            f"<span style='background:var(--green2);color:#fff;padding:2px 10px;"
            f"border-radius:20px;font-size:0.74rem;margin-right:4px'>{s}</span>"
            for s in skills
        ])
        st.markdown(f"<div style='margin-bottom:12px'>Skills: {tags}</div>", unsafe_allow_html=True)
with col2:
    if st.button("🗑 Clear"):
        st.session_state.histories[agent_key] = []
        st.rerun()

# Chat history
with st.container():
    if not history:
        st.markdown(
            f"<div class='chat-empty'>Start a conversation with <strong>{agent_info['label']}</strong></div>",
            unsafe_allow_html=True,
        )
    else:
        for msg in history:
            if msg["role"] == "user":
                st.markdown(
                    f"<div class='chat-wrap'>"
                    f"<div class='msg-label' style='text-align:right'>You</div>"
                    f"<div class='msg-user'>{msg['content']}</div></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='chat-wrap'>"
                    f"<div class='msg-label'>{agent_info['icon']} {agent_info['label']}</div>"
                    f"<div class='msg-agent'>{msg['content']}</div></div>",
                    unsafe_allow_html=True,
                )

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Message",
        placeholder=f"Ask {agent_info['label']} something...",
        height=100,
        label_visibility="collapsed",
        disabled=not API_KEY,
    )
    submitted = st.form_submit_button(
        "Send ➤",
        use_container_width=True,
        disabled=not API_KEY,
    )

if submitted and user_input.strip() and API_KEY:
    history.append({"role": "user", "content": user_input.strip()})
    with st.spinner(f"{agent_info['icon']} {agent_info['label']} thinking..."):
        try:
            reply = run_agent(agent_key, history, API_KEY)
            history.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")
    st.rerun()
