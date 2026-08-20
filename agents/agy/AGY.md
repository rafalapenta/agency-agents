# agy (Antigravity) — Agentic OS Config

The **agy** CLI (Antigravity) replaces the deprecated `gemini` CLI as the
research/analysis agent in Agentic OS (v0.4.0).

- Use the `agy` binary from the CLI
- Non-interactive mode: `agy --print "<query>"`
- Handles web research, multi-modal analysis, document understanding, data
  analysis, and reasoning tasks

## Integration
- Invoked via `execute_agent("agy", message)` in `server.py`
- Registered in `data/agent-routes.json` under `agent_capabilities`
- Status checked via `shutil.which("agy")` in `check_agent()`

## Install
```
curl -fsSL https://antigravity.ai/install | bash
```

## Usage
```
agy --print "Research the latest AI agent trends"
```
