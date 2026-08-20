# AGency

> **Registry-as-a-Tool · Zero Context Bloat** — A multi-agent orchestration platform that routes tasks to the right agent, manages persistent memory, and evolves capabilities over time.

[![CI](https://github.com/AGency/agency/actions/workflows/ci.yml/badge.svg)](https://github.com/AGency/agency/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-alpha-v0.1.0-orange)](https://github.com/AGency/agency/releases)

---

## 🚀 Quickstart

```bash
# Clone & setup
git clone https://github.com/AGency/agency.git
cd agency
cp .env.example .env
# Edit .env with your API keys

# Run with Docker (recommended)
docker compose up -d

# Or run directly
pip install -r requirements.txt
python server.py
```

Dashboard disponível em `http://localhost:8080`

---

## 🏗️ DAG Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     WEB DASHBOARD                           │
│                  (FastAPI + Tailwind SPA)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │  opencode   │  │  Hermes     │  │   agy CLI        │   │
│  │  (Code/Dev) │  │ (Memory/    │  │ (Research/       │   │
│  │             │  │  Schedule)  │  │  Analysis)       │   │
│  └──────┬──────┘  └──────┬──────┘  └────────┬─────────┘   │
│         │                │                   │             │
│         └────────────────┴───────────────────┘             │
│                          │                                 │
│              ┌───────────▼───────────┐                     │
│              │   AGENT ROUTER        │                     │
│              │   (FastMCP / Stateless)│                    │
│              └───────────┬───────────┘                     │
│                          │                                 │
│         ┌────────────────┼────────────────┐                │
│         ▼                ▼                ▼                │
│   ┌──────────┐   ┌──────────┐   ┌──────────────┐          │
│   │ Memory   │   │ Scheduler│   │ Skills Hub   │          │
│   │ Graph    │   │ (APSA)   │   │ (Registry)   │          │
│   └──────────┘   └──────────┘   └──────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 FastMCP Integration

AGency exposes tools via FastMCP for zero-context-bloat integration:

```python
from fastmcp import FastMCP

mcp = FastMCP("agency")

@mcp.tool()
def route_agent(query: str, threshold: float = 0.25) -> dict:
    """Route a query to the best-matching agent."""
    return {
        "agent_id": "...",
        "prompt": "...",
        "tool_ids": [...]
    }
```

**Paradigma:** Cada ferramenta é um registry entry. O LLM não carrega todo o contexto — apenas o tool schema relevante.

---

## 📚 Architecture Docs

| Document | Description |
|----------|-------------|
| [Zero Context Bloat](docs/ZERO_CONTEXT_BLOAT.md) | O manifesto do paradigma — por que e como evitar context bloat |
| [Roster C-Level](docs/ROSTER_C_LEVEL.md) | Governança executiva e papéis dos macro-diretores |
| [Paperclip State Engine](docs/PAPERCLIP_STATE_ENGINE.md) | Motor de estados persistentes para sessão agêntica |

---

## 📦 Project Structure

```
AGency/
├── .github/workflows/ci.yml    # GitHub Actions CI
├── .gitignore                  # Blindado: .env, *.db, chroma_data, logs
├── .env.example                # Template de variáveis de ambiente
├── Dockerfile                  # Multi-stage, non-root
├── docker-compose.yml          # Portável, agnóstico
├── LICENSE                     # MIT
├── README.md
├── docs/
│   ├── ZERO_CONTEXT_BLOAT.md
│   ├── ROSTER_C_LEVEL.md
│   └── PAPERCLIP_STATE_ENGINE.md
├── src/
│   ├── mcp_servers/            # FastMCP tool definitions
│   ├── agents/                 # Agent implementations
│   └── router/                 # Stateless routing logic
├── brain/                      # Persistent memory
├── skills/                     # Skills hub
└── server.py                   # FastAPI entrypoint
```

---

## 🛡️ Security & Privacy

- **Zero hard-coded secrets**: Todas as credenciais via variáveis de ambiente
- **Gitignore blindado**: `.env`, `*.db`, `chroma_data`, `*.log` são excluídos
- **CI security scan**: Verificação preventiva de segredos em commits
- **Non-root container**: Executa como usuário `appuser`

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contribuições são bem-vindas! Leia [docs/ZERO_CONTEXT_BLOAT.md](docs/ZERO_CONTEXT_BLOAT.md) antes de propor mudanças para alinhar com o paradigma do projeto.

---

*Registry-as-a-Tool · Zero Context Bloat · Built with Hermes Agent*
