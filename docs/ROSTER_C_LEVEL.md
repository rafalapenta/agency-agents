# Roster C-Level

> **Governança Executiva do AGency**

## Macro-Diretores

O AGency opera sob governança de macro-diretores, cada um com domínio específico e CLI dedicada:

| Diretor | Função | Runtime CLI | Escopo |
|---------|--------|-------------|--------|
| `@tech_director` | Infraestrutura, segurança, CI/CD | Antigravity CLI (agy) | Código, containers, pipelines, auditoria |
| `@product_director` | Documentação, DX, arquitetura | Claude Code | README, docs/, estrutura de projeto |
| `@growth_director` | Branding, metadados, publicação | Antigravity CLI (agy) | Naming, SEO, release, git workflow |
| `@ops_director` (emergencial) | Monitoramento, saúde do sistema | Hermes Agent | Health checks, heartbeat, alertas |

## Protocolo de Governança

### Portões HITL (Human-in-the-Loop)

Todo lançamento passa por dois portões obrigatórios:

1. **HITL 1 — Plano Diretor**: Aprovação do DAG de execução e alocação de CLIs
2. **HITL 2 — Planos Técnicos**: Aprovação dos checklists de arquivos/comandos antes de escrita ou push

### Fluxo de Decisão

```
Diretor propõe → Consolida(Atlas) → HITL review → Aprovação → Execução
```

### Regras de Escalada

- Alterações destrutivas (push, delete, overwrite) exigem HITL
- Decisões de naming requerem consenso `@growth_director` + `@product_director`
- Bug em produção: `@ops_director` escalate para `@tech_director`

## Roster Dinâmico

O roster é definido em tempo de execução via `route_agent(query)`. Novo diretor pode ser provisionado adicionando entrada ao registry FastMCP — sem restart do sistema.
