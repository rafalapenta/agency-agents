
## Phase 1 — Semantic Router Core: estado verificado em 2026-08-14

- [x] Contratos Pydantic v2 para agentes, ferramentas e associações.
- [x] SQLAlchemy para `agents`, `tools` e `agent_tools`, com cascata.
- [x] Parser do catálogo `agency-agents` e derivação determinística de trigger hooks.
- [x] `--dry-run` sem mutações.
- [x] `--reindex` idempotente em SQLite e ChromaDB cosine.
- [x] `route_agent` stateless com threshold estrito e allowlist relacional.
- [x] Tool FastMCP validada por `Client(mcp)` in-memory.
- [x] Suíte completa `pytest tests -q` com exit code 0.
- [x] P95 warm abaixo de 500 ms: 23,193 ms em 200 amostras.
- [ ] Integrar a cópia validada ao diretório oficial Windows com backup preservado.
- [ ] Indexar o catálogo completo `msitarzewski/agency-agents` e executar smoke test representativo.
- [ ] Configurar o servidor MCP no Hermes Desktop, Claude Code e `agy` quando o CLI estiver disponível.

Próximo marco: integração preservada no diretório oficial e reindexação do catálogo completo.

## Encerramento da integração Phase 1

- [x] Backup ZIP preservado antes do overlay.
- [x] 174 arquivos integrados com 0 divergências SHA-256.
- [x] Suíte completa e benchmark executados no diretório oficial.
- [x] `--help` e `--dry-run` verificados no diretório oficial.

O Router Core está pronto para a próxima etapa: ingestão do catálogo completo e configuração dos consumidores MCP.
