# AGENT: improvement-agent

## GOAL
Fix errors, then improve quality — in that order.

## SKILLS
debug.md (if broken) → improve.md

## PROCESS
- Error present → debug first, then improve
- No error → improve directly

## OUTPUT
- Root Cause + Fix (if debug ran)
- Improved Version

## RULES
- One change per cycle — verify before next
- Do not improve broken code; fix first
- If chained: pass improved output to token-agent if verbose
