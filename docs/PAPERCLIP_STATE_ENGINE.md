# Paperclip State Engine

> **Motor de Estados Persistentes para Sessão Agêntica**

## Conceito

O **Paperclip State Engine** é o sistema que mantém o estado da sessão agêntica persistente entre turnos, sem inflar o contexto do LLM com dados históricos desnecessários.

## Princípios

1. **State as Reference**: O LLM vê referências (IDs, hashes), não payloads completos
2. **Clipped Persistence**: Apenas estados relevantes são persistidos; o ruído é descartado
3. **Paperclip Analogy**: Assim como um grampeador mantém páginas juntas sem colá-las, o engine conecta estados sem fundi-los em um blob monolítico

## Arquitetura

```
┌─────────────────────────────────────────┐
│         LLM Context Window              │
│  (Tool schemas + current state refs)    │
└──────────────┬──────────────────────────┘
               │ reference
               ▼
┌─────────────────────────────────────────┐
│      Paperclip State Engine             │
│  ┌───────────┐  ┌───────────┐          │
│  │ Session   │  │  Memory   │          │
│  │ Graph     │  │  FTS5     │          │
│  └───────────┘  └───────────┘          │
│  ┌───────────┐  ┌───────────┐          │
│  │ Eval      │  │  Scheduler│          │
│  │ Scores    │  │  Jobs     │          │
│  └───────────┘  └───────────┘          │
└─────────────────────────────────────────┘
               │
               ▼ persistent
┌─────────────────────────────────────────┐
│         SQLite + ChromaDB              │
└─────────────────────────────────────────┘
```

## API de Estado

```python
# Save state reference (lightweight)
state.save("session_abc123", {"last_task": "x", "tokens_used": 4500})

# Load state reference (returns ID, not full payload)
ref = state.load("session_abc123")  # → "ref:abc123:last_task"

# Dump full state (only when needed)
full = state.dump("ref:abc123:last_task")
```

## Integração com FastMCP

O estado é exposto como ferramentas registry:

```python
@mcp.tool()
def get_state_ref(session_id: str) -> str:
    """Returns a lightweight reference to session state."""
    return state.resolve(session_id)
```

O LLM usa o reference para queries posteriores, sem carregar o estado completo no prompt.

## Verão de Performance

- **Estado referenciado**: ~50 tokens por entrada
- **Estado completo**: ~500-2000 tokens por entrada
- **Economia média**: 90% de redução no contexto de sessão
