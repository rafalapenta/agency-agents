
## Baseline v2 — agentic-os Layer 1 (2026-08-14)

O fork de `modimihir07/agentic-os` passa a ser a Layer 1. O caminho crítico é estritamente stateless:

```text
Hermes / Claude Code / Antigravity
 |
 v FastMCP
src/mcp_servers/semantic_router.py
 |
 v
src/router/semantic.py
 | |
 v v
ChromaDB cosine SQLite / SQLAlchemy
```

Decisões vigentes:

- Dashboard, tracking e self-evolving não participam do caminho de `route_agent`.
- SQLite mantém `agents`, `tools` e `agent_tools`; a associação N:N é a allowlist de ferramentas.
- ChromaDB indexa os trigger hooks com distância de cosseno.
- O catálogo Markdown é read-only no runtime; mutação exige reindexação explícita.
- `--dry-run` valida sem criar SQLite ou ChromaDB.
- Abaixo do threshold não existe fallback implícito: retorna `matched=false`.
- A resposta não expõe `connection_config`; retorna apenas ferramentas autorizadas.
- Caminhos de prompt são resolvidos dentro da raiz do catálogo, impedindo path traversal.
- Embedding Phase 1: feature hashing local determinístico de 256 dimensões, sem API externa.
- FastMCP é validado in-memory antes de qualquer transporte de rede.

Evidências detalhadas: `specs/002-router-core-evidence.md`.
