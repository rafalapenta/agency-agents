<div align="center">
  <br/>
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115+-green.svg" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/agents-3-orange.svg" alt="3 Agents"/>
  <img src="https://img.shields.io/badge/skills-15-purple.svg" alt="15 Skills"/>
  <img src="https://img.shields.io/badge/version-v0.4.0-blueviolet.svg" alt="v0.4.0"/>
  <img src="https://img.shields.io/badge/status-stable-brightgreen.svg" alt="Status: Stable"/>
  <a href="https://dev.to/mihir_nmodi_14a06a4019e1/i-built-an-open-source-agent-os-2h30"><img src="https://img.shields.io/badge/dev.to-article-blue.svg" alt="dev.to article"/></a>
  <br/><br/>
</div>

# Agentic OS (agentic-os) 🧠 — Multi-Agent Orchestration Platform

A locally-hosted operating system for AI agents — an open-source GitHub repository — that coordinates **opencode**, **Hermes Agent**, and **agy CLI** into a unified dashboard with persistent memory, cron scheduling, skill execution, cost analytics, and disaster recovery.

> **Why Agentic OS?** Most agent tools work in isolation — a terminal for coding, a separate chat for research, another for memory. Agentic OS is the **control plane** that unifies them: one dashboard, one memory layer, one scheduler, one skill hub. Three agents, infinite capabilities.

---

## ✨ Features

| Category | Features |
|----------|----------|
| **🤖 3-Agent Engine** | opencode (code/DevOps), Hermes (memory/scheduling), agy (research/analysis) with intelligent routing |
| **🧩 15+ Skills** | Executable skill packs with eval scoring, learnings, and score history per run |
| **🧠 Persistent Memory** | SQLite FTS5 + `brain/` folder — shared context read by all agents at session start |
| **⏱ Cron Scheduler** | APScheduler-powered jobs — heartbeat, memory consolidation, daily standup, DevOps audit |
| **💰 Cost Analytics** | Track spending per provider, model, agent. Free-tier alerts prevent surprise bills |
| **📋 Audit Trail** | Every action logged — chat, skill runs, settings changes, backups |
| **💾 One-Click Backup** | Full tar.gz snapshot of all configs, skills, brain, agents, prompts |
| **📝 Prompt Library** | 10 reusable templates — code review, system audit, project plan, brainstorm, and more |
| **📐 Standards System** | Discover and inject coding conventions across your project |
| **🔌 Plugin Registry** | Marketplace-style plugin management (extensible via skills) |
| **🎨 Dark/Light Theme** | GitHub-style dark mode + clean light theme, toggle from sidebar |
| **⚡ Zero API Costs** | Built for free tiers — Antigravity (agy), OpenRouter free models, local opencode |
| **📋 Kanban Board** | Visual task management — drag-and-drop columns, priority/status filtering, block/unblock, detail view |
| **🎯 Goals** | Project targets with progress tracking, auto-syncs to `brain/active-projects.md` |
| **📓 Journal** | Daily markdown entries stored as `brain/journal/YYYY-MM-DD.md` with full-text search |
| **❤️ Agent Health** | Real-time monitoring of opencode, Hermes, and agy CLI availability |
| **🧭 Smart Router** | Keyword-based task routing with confidence scoring — suggests best agent for any task |
| **📊 Learning Analytics** | Skill evaluation scores, performance trends, and historical charts |
| **🎬 Session Replay** | Browse and replay past opencode sessions from the dashboard |
| **⚠ Error Dashboard** | Real-time error tracking with category filtering and circuit breaker status |
| **🔌 Circuit Breaker** | Auto-trip after N failures, auto-recovery after 300s, manual reset |
| **⏱ Event-Driven Scheduler** | File-watcher auto-reloads jobs on change, webhook receiver, execution history |
| **🔗 Webhook Receiver** | `/api/webhook` — trigger skill execution from external tools |
| **🧠 SQLite FTS5 Memory** | Full-text search across brain, skills, journal with entity extraction |
| **🤖 Auto-Skill Generator** | `POST /api/skills/generate` — create SKILL.md from natural language |
| **📱 Mobile PWA** | Bottom navigation bar, manifest.json, service worker, touch-friendly UI |

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                                AGENTIC OS DASHBOARD                                                 │
│                                  FastAPI + Tailwind SPA                                                      │
├──────────────────────────────────────────────────────────────┤
│                                                                                                                             │
│  ┌───────────────┐  ┌────────────────┐  ┌────────────────────┐    │
│  │    opencode            │  │    Hermes                │  │    agy CLI                      │    │
│  │  (Code/DevOps)     │  │ (Memory/Sched)    │  │   (Research/Analy)          │    │
│  │   File Ops)              │  │  /Channels)             │  │                                        │    │
│  └───────────────┘  └────────────────┘  └────────────────────┘    │
│                                                                                                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 7 CORE LAYERS (Stacked)                                                          │  │
│  │  Layer 7: Identity / Persona / Constitution                                                  │  │
│  │  Layer 6: Self-Evolution + Capability Manager                                              │  │
│  │  Layer 5: Scheduler + Awareness + Health Guardian                                    │  │
│  │  Layer 4: Memory Graph + Memory Consolidation                                         │  │
│  │  Layer 3: Skills Hub + Eval + Learnings Loop                                                 │  │
│  │  Layer 2: Business Brain + Context Folders                                                  │  │
│  │  Layer 1: Agent Router + Standards + Profiles                                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

| Agent | Role | Default Model | Provider | Cost |
|-------|------|---------------|----------|------|
| **opencode** | Code generation, DevOps, file operations | deepseek-v4-flash-free | opencode-zen | **$0** |
| **Hermes Agent** | Persistent memory, scheduling, messaging | Owl Alpha (1M ctx) | OpenRouter | **$0** |
| **agy CLI** | Web research, multi-modal analysis | Antigravity | agy CLI | **$0** |

### Routing Rules

- **Code/DevOps task?** → opencode
- **Memory/Channel/Schedule?** → Hermes Agent
- **Research/Analysis?** → agy CLI
- **Complex multi-step?** → Chain: agy researches → opencode implements → Hermes monitors/schedules

---

## 🚀 Quick Start

```bash
git clone https://github.com/modimihir07/agentic-os.git
cd agentic-os
chmod +x install.sh && ./install.sh
./start.sh
# Open http://127.0.0.1:8080
```

---

## 📋 Prerequisites

| Tool | Required? | Install |
|------|-----------|---------|
| Python 3.10+ | ✅ Required | Auto-installed via `uv` by `install.sh` |
| Node.js 18+ | ⚠ For opencode | `curl -fsSL https://deb.nodesource.com/setup_20.x \| sudo bash - && sudo apt install -y nodejs` |
| opencode | ⚠ For code tasks | `npm install -g @opencode/cli` |
| Hermes Agent | ⚠ For memory/scheduling | `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh \| bash` |
| agy CLI | ⚠ For research/analysis | `curl -fsSL https://antigravity.ai/install \| bash` |

> ⚠ = Optional — the dashboard works with any subset of installed agents.

---

## 🔧 Configuration

### Hermes (OpenRouter)
```bash
# Set your OpenRouter API key
echo 'OPENROUTER_API_KEY=sk-or-v1-your-key-here' > ~/.hermes/.env
```

### agy CLI (Antigravity)
```bash
agy login
# Authenticate to enable web research, analysis, and document understanding
```

### Dashboard Settings
Edit `data/settings.json`:
```json
{
  "dashboard": { "port": 8080 },
  "theme": "dark",
  "agents": { "opencode": true, "hermes": true, "agy": true }
}
```

---

## 📁 Project Structure

```
agentic-os/
├── server.py              # FastAPI backend (REST API)
├── requirements.txt       # Python dependencies
├── install.sh             # One-command installer
├── start.sh               # Launch dashboard
├── backup.sh / restore.sh # Disaster recovery
│
├── dashboard/             # Web frontend (SPA)
│   ├── index.html         # Entry point + sidebar
│   ├── app.js             # SPA router + theme/sidebar toggle
│   ├── api.js             # API client (all endpoints)
│   ├── styles.css         # Full dark/light theme CSS
│   ├── utils.js           # Shared utilities
│   └── pages/             # 22 page modules (13 original + 7 v0.2.0 + 1 v0.3.0 + 1 v0.4.0)
│       ├── dashboard.js   # Overview with stats
│       ├── skills.js      # Skill grid/list/detail
│       ├── memory.js      # Brain file editor + Knowledge Graph
│       ├── chat.js        # Multi-agent chat + file attachments
│       ├── history.js     # ▸ Chat History Search (v0.4.0)
│       ├── scheduler.js   # Cron job manager
│       ├── audit.js       # Activity trail
│       ├── cost.js        # Cost analytics charts
│       ├── plugins.js     # Plugin marketplace
│       ├── backups.js     # Backup/restore UI
│       ├── prompts.js     # Template library
│       ├── standards.js   # Code conventions
│       ├── settings.js    # Config editor
│       ├── setup-wizard.js  # Guided setup
│       ├── kanban.js      # ▸ Kanban Board (v0.2.0)
│       ├── goals.js       # ▸ Goals (v0.2.0)
│       ├── journal.js     # ▸ Journal (v0.2.0)
│       ├── agent-health.js # ▸ Agent Health (v0.2.0)
│       ├── smart-router.js # ▸ Smart Router (v0.2.0)
│       ├── learning-analytics.js # ▸ Learning Analytics (v0.2.0)
│       ├── session-replay.js # ▸ Session Replay (v0.2.0)
│       └── errors.js       # ▸ Error Dashboard (v0.3.0)
│
├── brain/                 # Shared context (all agents read)
│   ├── memory_search.py   # ▸ SQLite FTS5 search (v0.3.0)
│   ├── business-brain.md  # Current project context
│   ├── memory.md          # Accumulated knowledge
│   ├── recent-decisions.md
│   ├── active-projects.md
│   ├── identity.md
│   ├── constitution.md
│   └── journal/           # Daily markdown entries (YYYY-MM-DD.md)
│
├── skills/                # 15 executable skills
│   ├── devops-audit/      # GCP/CloudMart infra audit
│   ├── heartbeat/         # 5-min health check
│   ├── content-draft/     # Blog/newsletter writing
│   ├── code-review/       # PR review checklist
│   ├── research-synthesis/ # agy research aggregator
│   ├── daily-standup/     # Morning briefing
│   ├── meeting-minutes/   # Notes processor
│   ├── project-planner/   # Step-by-step plans
│   ├── brainstorming/     # Socratic design
│   ├── systematic-debug/  # 4-phase root cause
│   ├── memory-consolidation/ # Weekly synthesis
│   ├── backup-skill/      # Snapshot creator
│   ├── cost-analytics/    # Multi-provider cost
│   ├── tdd-cycle/         # Red-green-refactor
│   ├── goal-planner/      # Goal → steps
│   └── _template/         # Starter template
│
├── agents/                # Per-agent configs (opencode, hermes, agy)
├── scheduler/jobs/        # Cron job definitions
├── registry/              # Plugin marketplace
├── standards/             # Discover/inject conventions
├── prompts/               # 10 reusable templates
├── data/                  # Runtime data (agent-routes.json tracked; settings/cost/chat/error/scheduler/memory/circuit/kanban/uploads gitignored)
├── audit/                 # Activity log (gitignored)
└── backups/               # Snapshots (gitignored)
```

---

## 🆕 What's New in v0.4.0

| Feature | Description |
|---------|-------------|
| **🤖 agy (Antigravity) replaces Gemini CLI** | Full provider swap across backend, routing, frontend, skills, agents/, and docs. `data/agent-routes.json`, circuit breaker, health checks, chat all use `agy` |
| **🛡 Port Conflict Auto-Kill** | `start.sh` detects a stale dashboard process on the target port and kills it before starting |
| **📦 Auto-Install apscheduler** | `scheduler.py` auto-installs missing dependencies instead of failing on startup |
| **💬 Chat History Search** | `/api/chat/history` supports `q`, `agent`, `limit` filters + a dedicated History page with search, agent filter pills, and date grouping |
| **📎 Chat File Attachments** | `POST /api/chat/upload` (multipart) accepts text files up to 2 MB (validated allowlist), previews content to the agent, and stores under `data/uploads/` with 24h TTL cleanup |
| **🕸 Memory Knowledge Graph** | `GET /api/memory/graph` returns nodes (brain/skills/journal docs + extracted entities) and edges (shares_source / mentions), rendered as an interactive Canvas graph in the Memory page |
| **📜 Code Diff Viewer** | `GET /api/diff?file=&ref=` returns unified git diff with repo-relative path-traversal protection; "View Diff" button on the Skills page |
| **🧪 15 new tests** | Suite grows from 59 → 74 isolated tests covering chat history, uploads, memory graph, and diff viewer |
| **🛠 Stale-Cache Elimination** | `no-store` cache headers on all dashboard assets, `?v=` cache-busting, service-worker purge on load, root-level asset fallbacks so stale index.html never breaks the UI |
| **📐 Zoom-Proof Layout** | Content width capped at 1600px, responsive file-card grid, and `flex-shrink: 0` on tab bars — layout stays clean from 60% to 100% zoom |
| **🔢 Correct Skill Count** | Skills badge now counts skill directories (15) via the status endpoint instead of returning 0 |

During the v0.4.0 hardening pass the following **layout & caching bugs** were crushed: tab bars (Files/Knowledge Graph, Grid/List) collapsing to 1px under content at certain zooms, oversized cards stretching to 3500px+ at 50% zoom, cached index.html referencing dead asset URLs, and the sidebar Skills badge showing 0.

---

## 🆕 What's New in v0.3.0

| Feature | Description |
|---------|-------------|
| **🔒 Security Audit** | 23 vulnerabilities fixed: 3 CRITICAL (path traversal), 8 HIGH (XSS, command injection, missing headers), 7 MEDIUM. Security headers middleware added (CSP, HSTS, X-Frame-Options) |
| **⏱ Event-Driven Scheduler** | Rewritten with file-watcher auto-reload (watchdog-style), webhook receiver at `/api/webhook`, execution history, manual job triggers |
| **⚠ Error Dashboard** | New `/api/errors` endpoints with category filtering (agent/skill/api/system). Dedicated dashboard page with error log + circuit breaker status cards |
| **🔌 Circuit Breaker** | Auto-trip after 3 failures, half-open recovery after 300s. Per-agent state tracking with manual reset. Prevents cascading failures to offline agents |
| **🧠 Persistent Memory (SQLite FTS5)** | Full-text search across `brain/*.md`, `skills/*/*.md`, `brain/journal/`. Entity extraction (persons, emails, URLs, acronyms, IPs). Reindex endpoint |
| **🤖 Auto-Skill Generator** | `POST /api/skills/generate` takes natural language description → creates full SKILL.md with eval.json and context folder |
| **🔗 Webhook Receiver** | Generic webhook at `/api/webhook/generic` plus skill-targeted webhooks. Integrates with GitHub, CI/CD, external tools |
| **📱 Mobile PWA** | Bottom navigation bar, `manifest.json`, service worker (offline fallback), PWA meta tags, touch-friendly 16px inputs, responsive grid collapse |

### Security Hardening
- **Path traversal**: All file endpoints validate `..` and `/` in user-supplied names
- **XSS elimination**: 19 violations fixed across 7 JS files — all `onclick` handlers use `encodeURIComponent`, all text uses `escapeHtml()`
- **Security headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- **CORS restricted**: Only `http://127.0.0.1:8080` and `http://localhost:8080`
- **API keys masked**: `/api/settings` returns keys as masked values (e.g., `sk-o****`)
- **Input validation**: Chat messages limited to 10K chars, brain/skill names reject special chars
- **Session replay**: Content limited to 2000 chars, path traversal prevented
- **Runtime data gitignored**: `error-log.json`, `circuit-breaker.json`, `scheduler-history.json`, `memory.db`, `kanban/*.json`

---

## 🆕 What's New in v0.2.0

| Feature | Description |
|---------|-------------|
| **📋 Kanban Board** | Visual task management with 6 columns (triage → todo → ready → in_progress → blocked → done), drag-and-drop, priority labels, filtering, and detail modals with complete/block/unblock actions |
| **🎯 Goals** | Create and track project targets with progress bars, categories, and target dates. Auto-syncs to `brain/active-projects.md` for agent awareness |
| **📓 Journal** | Daily markdown journal entries stored as `brain/journal/YYYY-MM-DD.md`. Full-text search, day streak tracking, word count |
| **❤️ Agent Health** | Real-time dashboard showing online/offline status for all 3 agents (opencode, Hermes, agy CLI). Auto-refresh every 5 seconds |
| **🧭 Smart Router** | Keyword-based routing engine — type a task description and get an AI-suggested agent with confidence score. Manual override available |
| **📊 Learning Analytics** | Skill evaluation scores, performance trends, and per-skill detail breakdowns with mini bar charts |
| **🎬 Session Replay** | Browse and replay past opencode sessions directly from the dashboard. View message content and timestamps |

### UI Modernization
- **Glass morphism cards** with subtle backdrop blur
- **Glow borders** and gradient accents on interactive elements
- **Skeleton loaders** with shimmer animation for async content
- **Empty states** with icons and contextual messages
- **All CSS additions are zero-breaking** — existing 13 pages and 28 endpoints unchanged

---

## 🎮 Usage

### AI Chat
Select an agent from the sidebar → type your message → get response.

| Agent | Best for | Example |
|-------|----------|---------|
| **opencode** | "Check system status", "Deploy to GKE" | Code + terminal automation |
| **Hermes** | "What did I work on recently?", "Schedule a daily backup" | Memory recall, scheduling |
| **agy** | "Research latest AI agent trends", "Analyze this image" | Web research, multi-modal |

### Skills
Browse 15 skills from Skills Hub → click Run → monitor eval scores over time.

### Scheduler
Create cron jobs: heartbeat (5 min), memory consolidation (weekly), daily standup, DevOps audit.

### Cost Analytics
Track spending per provider/model/agent. Free-tier alerts warn when nearing limits.

### Kanban Board (v0.2.0)
Drag tasks across columns, filter by priority/category, click to view details. Block tasks when blocked, mark complete when done.

### Goals (v0.2.0)
Create goals with categories and target dates. Progress tracked via +25% increments. Completed goals auto-sync to brain context.

### Journal (v0.2.0)
Write daily entries with markdown support. Auto-saves after 2 seconds. Search across all entries from the dashboard.

### Smart Router (v0.2.0)
Describe a task in plain English — the router analyzes keywords and suggests the best agent. Route manually or let AI decide.

### Agent Health (v0.2.0)
Monitor online status of all 3 agents in real time with 5-second auto-refresh. Health checks are filesystem-based (no subprocess calls).

### Learning Analytics (v0.2.0)
View evaluation scores for all 15 skills. Trends chart shows score progression over time. Top skills ranked by performance.

### Session Replay (v0.2.0)
Browse opencode session logs by date and size. Click "Replay" to view all messages in a chat-like interface.

### Error Dashboard (v0.3.0)
View system errors grouped by category (agent, skill, API, system). Filter by category, clear all errors. Circuit breaker cards show per-agent failure state — reset from the dashboard.

### Event-Driven Scheduler (v0.3.0)
Jobs auto-reload when JSON files in `scheduler/jobs/` change. Trigger skills via webhooks at `POST /api/webhook` with `{"skill": "skill-name", "payload": {...}}`. Manual trigger at `/api/scheduler/trigger/{job_id}`.

### Persistent Memory Search (v0.3.0)
Full-text search across all brain files, skills, and journal entries via SQLite FTS5. Query at `GET /api/memory/search?q=...` with highlighted snippets. Reindex at `POST /api/memory/reindex`. Entities (persons, emails, URLs) auto-extracted.

### Auto-Skill Generator (v0.3.0)
Create new skills from natural language: `POST /api/skills/generate` with `{"name": "my-skill", "description": "Does X by doing Y"}`. Generates SKILL.md, eval.json, learnings.md, and context folder.

### Webhooks (v0.3.0)
`POST /api/webhook` — trigger any skill by name. `POST /api/webhook/generic` — catch-all for external tool integration (GitHub, CI/CD, etc.).

### Mobile PWA (v0.3.0)
Open Agentic OS on your phone — bottom nav bar replaces sidebar, touch targets are 44px+, service worker caches assets. Add to home screen for app-like experience.

---

## 📊 Comparison: Agentic OS vs Claude Agent OS (Julian Goldie)

| Feature | Claude Agent OS (Video) | Agentic OS (This Project) |
|---------|------------------------|---------------------------|
| **Core Agents** | Claude + OpenClaw + Hermes | opencode + Hermes + agy CLI |
| **Cost** | $20/mo (Claude subscription) | **$0 — all free tiers** |
| **Stack** | Next.js + Tailwind | FastAPI + vanilla JS SPA |
| **Architecture** | 4 layers | **7 layers** |
| **Skills System** | Plugin marketplace (2,000+ from Hermes) | 15 curated skills + eval scoring + learnings |
| **Memory** | Obsidian vault (external) | Built-in brain/ + SQLite FTS5 |
| **Scheduler** | Not shown | APScheduler cron jobs |
| **Cost Tracking** | Not shown | Built-in per-provider analytics |
| **Backup/Restore** | Not shown | One-click tar.gz snapshots |
| **Audit Trail** | Not shown | Full activity log |
| **Standards System** | Not shown | Discover/inject conventions |
| **Client Timeout** | Not shown | 200s AbortController |
| **Kanban Board** | Yes | **Yes — built-in** with drag-and-drop, priority, block/unblock, filters |
| **Open Source** | No (tutorial only) | **MIT License** |

---

## 🧪 Tested On

- **OS**: Linux (Ubuntu 22.04+), macOS
- **Python**: 3.10, 3.11, 3.12
- **Browsers**: Chrome, Firefox, Edge
- **Agents**: opencode v0.8+, Hermes Agent v1.0+, agy CLI (Antigravity)

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See `data/agent-routes.json` for routing rules and `skills/_template/` for creating new skills.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
  <p><strong>Agentic OS</strong> — Built with ❤️ by <a href="https://github.com/modimihir07">Mihir Modi</a></p>
  <p>
    <a href="https://dev.to/mihir_nmodi_14a06a4019e1/i-built-an-open-source-agent-os-2h30">📖 Read the dev.to article</a>
    ·
    <a href="https://github.com/modimihir07/agentic-os/issues">Report Bug</a>
    ·
    <a href="https://github.com/modimihir07/agentic-os/discussions">Discussions</a>
    ·
    <a href="https://github.com/modimihir07/agentic-os">GitHub</a>
  </p>
</div>
