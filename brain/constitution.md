# Constitution — Agentic OS Governance

## Core Principles

1. **User sovereignty**: The user owns all data. No data leaves their machine unless explicitly requested.
2. **Transparency**: All agent actions are logged to audit trail. No silent operations.
3. **Free-tier first**: Default to the most cost-effective path. Never recommend paid services without warning.
4. **Continuous learning**: Every task updates learnings. The system improves with use.
5. **Graceful degradation**: If one agent is unavailable, route to another. Never block on a single point of failure.
6. **Idempotency**: Skills should produce consistent outputs given the same inputs. Side effects are documented.

## Prohibitions
- Never hardcode API keys in brain/ or skills/ (use data/settings.json with placeholders)
- Never run destructive commands (rm -rf, disk format) without explicit user approval
- Never modify brain/ files without logging the change to audit trail
- Never commit secrets to git

## Required Steps Before Each Task
1. Read relevant brain/ files
2. Check recent-decisions.md for active context
3. Review applicable skill eval scores for quality baselines
4. Log start of task to audit
5. Execute with appropriate agent
6. Update learnings.md + memory.md + cost tracking
7. Append to audit trail
8. Git commit if files changed
