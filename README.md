# faIyke — Multi-Agent AI System

Modular AI system built for Claude Code. Company-style architecture with specialized agents and reusable skills.

## Structure

```
.claude/
├── CLAUDE.md              # Global behavior rules + task routing
├── skills/                # Atomic capabilities (single responsibility)
│   ├── improve.md
│   ├── research.md
│   ├── debug.md
│   ├── explain.md
│   ├── build.md
│   ├── job-search.md
│   ├── shopify-builder.md
│   ├── automation-flow.md
│   └── token-optimizer.md
└── agents/                # Department agents (orchestrate skills)
    ├── master-agent.md
    ├── research-agent.md
    ├── job-agent.md
    ├── shopify-agent.md
    ├── automation-agent.md
    ├── improvement-agent.md
    └── token-agent.md

skills/                    # Original SKILL.md source files
```

## Agents

| Agent | Role | Skills Used |
|-------|------|-------------|
| master-agent | Orchestrator — routes all tasks | All agents |
| research-agent | Structured research and analysis | research |
| job-agent | Job matching, fit scoring | job-search, token-optimizer |
| shopify-agent | E-commerce store generation | shopify-builder |
| automation-agent | Workflow and automation design | automation-flow |
| improvement-agent | Fix + improve code/text/systems | debug, improve |
| token-agent | Compress and optimize output | token-optimizer |

## Skills

| Skill | Trigger |
|-------|---------|
| improve | "improve this", "make better" |
| research | "research", "analyze", "deep dive" |
| debug | "fix this", "debug", "what's wrong" |
| explain | "explain", "ELI5", "how does X work" |
| build | "build", "create", "generate" |
| job-search | "find jobs", "match this job" |
| shopify-builder | "build shopify", "create store" |
| automation-flow | "automate", "n8n", "zapier", "make" |
| token-optimizer | "reduce tokens", "compress", "make shorter" |

## Usage

Drop `.claude/` into any project. Claude Code loads `CLAUDE.md` automatically. Reference agents and skills by name in prompts.

## Setup

```bash
git clone https://github.com/Obinwanne1/faIyke.git
cp -r faIyke/.claude /your-project/
```
