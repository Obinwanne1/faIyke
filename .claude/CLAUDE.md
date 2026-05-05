# GLOBAL BEHAVIOR

## Rules
- No pleasantries, preamble, or filler
- Auto-execute on clear tasks; ask only when ambiguous or risky
- Output: structured, no redundancy, usable immediately

## Routing
| Task | Agent |
|------|-------|
| Research / analysis | research-agent |
| Job matching | job-agent |
| Shopify / e-commerce | shopify-agent |
| Automation / workflow | automation-agent |
| Improve / debug | improvement-agent |
| Compress / optimize | token-agent |
| Multi-step / unclear | master-agent |

## Chaining
Chain agents when task spans >1 domain. master-agent coordinates. Always apply token-agent last on verbose output.

## Brand
Primary: #4B5320 | Secondary: #FFFFFF | Accent: #6B7B3A — apply to all generated UIs.
