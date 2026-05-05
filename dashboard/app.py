import streamlit as st
from dotenv import load_dotenv
import os
from agents import AGENT_META, run_agent

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="faIyke Agent Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Brand variables */
:root {
    --green:  #4B5320;
    --green2: #6B7B3A;
    --white:  #FFFFFF;
    --bg:     #F5F6F0;
    --border: #D4D9C4;
}

/* Global */
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
.stApp { background: var(--bg); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--green) !important;
    border-right: 2px solid var(--green2);
}
[data-testid="stSidebar"] * { color: var(--white) !important; }
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0;
    cursor: pointer;
    transition: background 0.2s;
    display: block;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.18);
}

/* Header bar */
.agent-header {
    background: var(--green);
    color: var(--white);
    padding: 16px 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.agent-header h2 { margin: 0; font-size: 1.4rem; }
.agent-header p  { margin: 2px 0 0; opacity: 0.8; font-size: 0.9rem; }

/* Chat messages */
.msg-user {
    background: var(--green);
    color: var(--white);
    padding: 12px 16px;
    border-radius: 12px 12px 4px 12px;
    margin: 8px 0;
    max-width: 80%;
    margin-left: auto;
    word-break: break-word;
}
.msg-agent {
    background: var(--white);
    color: #1a1a1a;
    padding: 12px 16px;
    border-radius: 12px 12px 12px 4px;
    margin: 8px 0;
    max-width: 85%;
    border: 1px solid var(--border);
    word-break: break-word;
}
.msg-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--green2);
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.chat-wrap { padding: 8px 0; }

/* Input area */
.stTextArea textarea {
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 2px rgba(75,83,32,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: var(--green) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 10px 28px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: var(--green2) !important;
}

/* Clear button */
.clear-btn > button {
    background: transparent !important;
    color: var(--green) !important;
    border: 2px solid var(--green) !important;
}
.clear-btn > button:hover {
    background: var(--green) !important;
    color: var(--white) !important;
}

/* API key input */
.stTextInput input {
    border: 2px solid var(--border) !important;
    border-radius: 8px !important;
}

/* Hide Streamlit branding */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "histories" not in st.session_state:
    st.session_state.histories = {k: [] for k in AGENT_META}
if "active_agent" not in st.session_state:
    st.session_state.active_agent = "master-agent"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 faIyke Agents")
    st.markdown("---")

    options = list(AGENT_META.keys())
    labels  = [f"{AGENT_META[k]['icon']}  {AGENT_META[k]['label']}" for k in options]
    choice  = st.radio("Select Agent", labels, index=options.index(st.session_state.active_agent))
    st.session_state.active_agent = options[labels.index(choice)]

    st.markdown("---")
    st.markdown("**API Key**")
    api_key_input = st.text_input(
        "Anthropic API Key",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        type="password",
        label_visibility="collapsed",
        placeholder="sk-ant-...",
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;opacity:0.6;text-align:center'>"
        "faIyke Multi-Agent System<br>Powered by Claude</div>",
        unsafe_allow_html=True,
    )


# ── Main ──────────────────────────────────────────────────────────────────────
agent_key  = st.session_state.active_agent
agent_info = AGENT_META[agent_key]
history    = st.session_state.histories[agent_key]

# Header
st.markdown(f"""
<div class="agent-header">
    <div style="font-size:2rem">{agent_info['icon']}</div>
    <div>
        <h2>{agent_info['label']}</h2>
        <p>{agent_info['desc']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Top row: skills tags + clear button
col1, col2 = st.columns([4, 1])
with col1:
    skills = AGENT_META[agent_key]["skills"]
    if skills:
        tags = " ".join([
            f"<span style='background:var(--green2);color:#fff;padding:2px 10px;"
            f"border-radius:20px;font-size:0.75rem;margin-right:4px'>{s}</span>"
            for s in skills
        ])
        st.markdown(f"<div style='margin-bottom:12px'>Skills: {tags}</div>", unsafe_allow_html=True)
with col2:
    if st.button("🗑 Clear chat"):
        st.session_state.histories[agent_key] = []
        st.rerun()

# Chat history
chat_container = st.container()
with chat_container:
    if not history:
        st.markdown(
            f"<div style='text-align:center;color:#888;padding:40px 0'>"
            f"Start a conversation with <strong>{agent_info['label']}</strong></div>",
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

# Input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Message",
        placeholder=f"Ask {agent_info['label']} something...",
        height=100,
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("Send ➤", use_container_width=True)

if submitted and user_input.strip():
    if not api_key_input:
        st.error("Add your Anthropic API key in the sidebar.")
    else:
        history.append({"role": "user", "content": user_input.strip()})
        with st.spinner(f"{agent_info['icon']} {agent_info['label']} thinking..."):
            try:
                reply = run_agent(agent_key, history, api_key_input)
                history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
        st.rerun()
