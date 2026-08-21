# Roster C-Level

> **Governança Executiva do AGency — v2.0**
> last_updated: 2026-08-21

## Macro-Diretores

O AGency opera sob governança de 6 macro-diretores, cada um com domínio específico e perfil de skills isolado:

| Diretor | Função | Runtime | Escopo |
|---------|--------|---------|--------|
| `@ceo` (Atlas) | CEO & Orquestrador Geral | Hermes Agent | Estratégia, governança, orquestração cross-domain |
| `@tech_director` (Vulcan) | CTO / Tech & Infrastructure | opencode | Código, arquitetura, segurança, CI/CD, testes |
| `@product_director` (Aura) | CPO / Product & Spatial | Claude Code | PRDs, UX/UI, design system, product strategy |
| `@growth_director` (Vesper) | CMO/CRO / Growth & Sales | agy CLI | Market intelligence, branding, content, pricing |
| `@business_director` (Sterling) | COO/CFO / Business & Finance | Hermes Agent | FP&A, due diligence, MVP planning, workflows |
| `@research_director` (Lyra) | Head of Research & Spatial Data | agy CLI | Research, data analysis, experiments, synthesis |

## Arquitetura de Skills

### Paradigma Registry-as-a-Tool

Cada diretor possui:
- **Skills Ativas** (5-8): Carregadas no contexto base, estimativas ≤ 2.000 tokens
- **Skills Efêmeras** (on-demand): Registradas no catálogo, invocadas via `route_agent`

```
┌─────────────────────────────────────────────────────────┐
│                    LLM Context Window                   │
│  (Skill schemas + identity + constraints)               │
└──────────────────────┬──────────────────────────────────┘
                       │ reference
                       ▼
┌─────────────────────────────────────────────────────────┐
│              src/bots_config/                           │
│  ├── atlas/SOUL.md         (8 ativas, 6 efêmeras)      │
│  ├── vulcan/SOUL.md        (8 ativas, 11 efêmeras)     │
│  ├── aura/SOUL.md          (8 ativas, 11 efêmeras)     │
│  ├── vesper/SOUL.md        (7 ativas, 8 efêmeras)      │
│  ├── sterling/SOUL.md      (7 ativas, 11 efêmeras)     │
│  ├── lyra/SOUL.md          (7 ativas, 10 efêmeras)     │
│  └── catalog/                                            │
│      ├── active_skills_manifest.json                   │
│      └── ephemeral_tools.json (52 tools)               │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FastMCP Semantic Router                    │
│  route_agent(query) → matches director + skills         │
└─────────────────────────────────────────────────────────┘
```

## Protocolo de Governança

### Portões HITL (Human-in-the-Loop)

Todo lançamento passa por dois portões obrigatórios:

1. **HITL 1 — Plano Diretor**: Aprovação do DAG de execução e alocação de CLIs
2. **HITL 2 — Planos Técnicos**: Aprovação dos checklists de arquivos/comandos antes de escrita ou push

### Fluxo de Decisão

```
Diretor propõe → Atlas consolda → HITL review → Aprovação → Execução
```

### Regras de Escalada

- Alterações destrutivas (push, delete, overwrite) exigem HITL + @ceo
- Decisões de naming requerem consenso @growth_director + @product_director
- Bug em produção: @ops_director escalate para @tech_director
- Decisões estratégicas: @ceo decide com input dos diretores

## Roster Dinâmico

O roster é definido em tempo de execução via `route_agent(query)`. Novo diretor pode ser provisionado adicionando:
1. Diretório em `src/bots_config/<nome>/SOUL.md`
2. Entrada no `active_skills_manifest.json`
3. Registro na tabela `agents` do SQLite
4. Reindexação do ChromaDB

Sem restart do sistema.

## Métricas de Saúde

| Métrica | Target |
|---------|--------|
| Context budget por diretor | ≤ 2.000 tokens |
| Skills ativas por diretor | 5-8 |
| Skill hit rate | > 40% |
| Bloat score | < 0.3 |

## Referência

- [Zero Context Bloat](ZERO_CONTEXT_BLOAT.md)
- [Paperclip State Engine](PAPERCLIP_STATE_ENGINE.md)
- [Macro Agents Spec](../specs/004-macro-agents.md)
