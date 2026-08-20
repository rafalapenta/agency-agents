# 004 — Macro Agents

> Status: Implemented (Phase 2)

## Overview

The macro orchestration layer coordinates the full lifecycle of a task
across the AGgency pipeline, from creation through routing, handoff,
and completion with quality gate validation.

## Components

### `src/macro_agents/orchestrator.py`

`MacroOrchestrator` executes a 7-step lifecycle:

1. **Create task** → `KanbanBoard.add()` with metadata.
2. **Persist state** → `StateManager.apply()` with phase=routing.
3. **Route** → `route_agent()` with threshold-based matching.
4. **Compress context** → `compress_context()` strips verbose fields.
5. **Handoff** → Dispatches to the matched domain agent (or simulates in dry-run).
6. **Update state** → Records handoff result and route score.
7. **Quality Gates** → Validates state invariants and completion.

### Quality Gates

| Gate | Validates |
|------|-----------|
| GATE1 | Task was created successfully |
| GATE2 | Router found a matching agent above threshold |
| GATE3 | Context compression executed without data loss |
| GATE4 | State invariant: version > 0 and phase == "completed" |

### Domain System Prompts (`prompts/domains/`)

Five domain-specific system prompts (v2.0.0):

| Domain | File |
|--------|------|
| Engineering | `prompts/domains/engineering.md` |
| Operations | `prompts/domains/operations.md` |
| Business | `prompts/domains/business.md` |
| Research | `prompts/domains/research.md` |
| Governance | `prompts/domains/governance.md` |

Each prompt includes:
- YAML frontmatter with version and domain metadata.
- Canonical context injection: `{{ task }}`, `{{ context | json }}`, `{{ state_version }}`.
- Five control tokens: `[CONTROL:PLAN]`, `[CONTROL:DELEGATE]`, `[CONTROL:VERIFY]`, `[CONTROL:COMMIT]`, `[CONTROL:ABORT]`.

### Orchestration Support

| Module | Purpose |
|--------|---------|
| `src/orchestration/context.py` | Context compression preserving essential fields |
| `src/orchestration/kanban.py` | Deterministic Kanban state machine with audit trail |

## Evidence

- E2E smoke test validates all 4 gates pass (exit code 0).
- Kanban transitions are validated against a strict state machine.
- Context compression achieves >40% reduction on typical payloads.
