from pathlib import Path
import anthropic
import os

ROOT = Path(__file__).parent.parent
AGENTS_DIR = ROOT / ".claude" / "agents"
SKILLS_DIR = ROOT / ".claude" / "skills"

AGENT_META = {
    "master-agent": {
        "label": "Master Agent",
        "desc": "Complex multi-step tasks across domains",
        "icon": "👑",
        "skills": [],
    },
    "research-agent": {
        "label": "Research Agent",
        "desc": "Structured research & analysis",
        "icon": "🔍",
        "skills": ["research"],
    },
    "job-agent": {
        "label": "Job Agent",
        "desc": "Job matching & fit scoring (Germany/IT)",
        "icon": "💼",
        "skills": ["job-search", "token-optimizer"],
    },
    "shopify-agent": {
        "label": "Shopify Agent",
        "desc": "E-commerce store generation",
        "icon": "🛍️",
        "skills": ["shopify-builder"],
    },
    "automation-agent": {
        "label": "Automation Agent",
        "desc": "Workflow & automation design",
        "icon": "⚙️",
        "skills": ["automation-flow"],
    },
    "improvement-agent": {
        "label": "Improvement Agent",
        "desc": "Debug & improve code, text, systems",
        "icon": "🔧",
        "skills": ["debug", "improve"],
    },
    "token-agent": {
        "label": "Token Agent",
        "desc": "Compress & optimize output",
        "icon": "⚡",
        "skills": ["token-optimizer"],
    },
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def build_system_prompt(agent_key: str) -> str:
    agent_md = _read(AGENTS_DIR / f"{agent_key}.md")
    skill_blocks = []
    for skill in AGENT_META[agent_key]["skills"]:
        content = _read(SKILLS_DIR / f"{skill}.md")
        if content:
            skill_blocks.append(f"--- SKILL: {skill} ---\n{content}")
    global_rules = _read(ROOT / ".claude" / "CLAUDE.md")
    parts = [global_rules, agent_md] + skill_blocks
    return "\n\n".join(filter(None, parts))


def run_agent(agent_key: str, messages: list, api_key: str) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    system = build_system_prompt(agent_key)
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        system=system,
        messages=messages,
    )
    return response.content[0].text
