# Patch Notes — Matrix de Skills do Roster C-Level v1.0

> **Data**: 2026-08-21
> **Autor**: Atlas (@ceo)
> **Status**: Implementado

---

## Resumo

Reestruturação completa da matriz de skills dos 6 perfis executivos no AGency, blindando o ecossistema contra Context Bloat e ativando estritamente 5-8 skills críticas por diretor.

---

## Mudanças

### 1. Novo Diretório: `src/bots_config/`

Criada estrutura dedicada para configuração dos macro-diretores:

```
src/bots_config/
├── atlas/         # CEO & Orquestrador Geral
├── vulcan/        # CTO / Tech & Infrastructure
├── aura/          # CPO / Product & Spatial
├── vesper/        # CMO/CRO / Growth & Sales
├── sterling/      # COO/CFO / Business & Finance
├── lyra/          # Head of Research & Spatial Data
└── catalog/
    ├── active_skills_manifest.json
    └── ephemeral_tools.json
```

### 2. Substituições de Skills

| Diretor | Removido | Adicionado | Razão |
|---------|----------|-----------|-------|
| Atlas | `handoff` | `agent-handoff-protocols` | Protocolo mais específico e documentado |
| Atlas | — | `context-budget-optimizer` | Blindagem contra context bloat |
| Vulcan | `implement` | `incremental-builder` | TDD atômico com build incremental |
| Vulcan | — | `backend-architecture` (efêmero) | Design de API sob demanda |
| Aura | — | `pm-product-strategy` | PRDs e user stories formais |
| Aura | `od-ui-ux-pro-max` | Descartado | Pacote inflado, rejeitado estruturalmente |
| Aura | `od-brainstorming` | Descartado | Pacote inflado, rejeitado estruturalmente |
| Aura | `od-canvas-design` | Descartado | Pacote inflado, rejeitado estruturalmente |
| Sterling | `xlsx` | `xlsx-modeler` | Modelagem contábil e FP&A profissional |
| Sterling | — | `data-visualization` (efêmero) | Visualização de dados sob demanda |
| Lyra | — | `data-visualization` (efêmero) | Visualização de dados sob demanda |

### 3. Novos Diretores

| Diretor | Paperclip ID | Domain |
|---------|--------------|--------|
| Atlas | `atlas` | governance |
| Vulcan | `vulcan` | engineering |
| Aura | `aura` | business |
| Vesper | `vesper` | business |
| Sterling | `sterling` | business |
| Lyra | `lyra` | research |

### 4. Catálogo Efêmero

52 skills registradas como ferramentas efêmeras no `ephemeral_tools.json`, acessíveis via `route_agent` com gatilhos por keyword e budget token definido.

### 5. Sistema de Evals & QA

- `llm-eval-harness` alocado estritamente na suíte de testes/CI (Loop 09)
- Skills de metagerenciamento (`find-skills`, `hermes-*`) desativadas dos perfis ativos
- Automação residencial e músicas removidas do contexto executivo

---

## Métricas

| Métrica | Antes | Depois |
|---------|-------|--------|
| Diretores no roster | 4 | 6 |
| Skills ativas totais | ~60 | 45 |
| Skills efêmeras | 0 | 52 |
| Context budget max/diretor | N/A | 2.000 tokens |
| Arquivos de persona | 1 (hermes) | 6 (bots_config/) |

---

## Arquivos Criados/Modificados

| Arquivo | Ação |
|---------|------|
| `src/bots_config/atlas/SOUL.md` | Criado |
| `src/bots_config/vulcan/SOUL.md` | Criado |
| `src/bots_config/aura/SOUL.md` | Criado |
| `src/bots_config/vesper/SOUL.md` | Criado |
| `src/bots_config/sterling/SOUL.md` | Criado |
| `src/bots_config/lyra/SOUL.md` | Criado |
| `src/bots_config/catalog/ephemeral_tools.json` | Criado |
| `src/bots_config/catalog/active_skills_manifest.json` | Criado |
| `docs/ROSTER_C_LEVEL.md` | Atualizado |
| `scripts/validate_context_budget.py` | Criado |

---

## Próximos Passos

1. Popular tabela `agents` no SQLite com os 6 macro-diretores
2. Popular tabela `agent_tools` com associações N:N
3. Reindexar ChromaDB com novos trigger hooks
4. Executar `scripts/validate_context_budget.py` para validação
5. Deploy para ambiente de staging

---

*Patch approved by @ceo — 2026-08-21*
