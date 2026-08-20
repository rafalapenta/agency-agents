# Zero Context Bloat

> **Manifesto do Paradigma Registry-as-a-Tool**

## O Problema

LLMs modernos sofrem de **context bloat**: quanto mais ferramentas, memória e contexto são carregados, mais caro, lento e menos preciso o modelo se torna. A solução ingênua — "carregar tudo no prompt" — colide com limites de tokens e degrade a qualidade da saída.

## A Filosofia

**Registry-as-a-Tool** inverte a lógica: em vez de embutir contexto no prompt, expomos recursos como *registros* acessíveis sob demanda. O LLM vê apenas o *schema* da ferramenta (metadados leves), não o conteúdo bruto.

### Princípios

| Princípio | O Que Significa |
|-----------|-----------------|
| **Lazy Context Loading** | Dados só entram no contexto quando realmente necessários |
| **Tool Schema > Payload** | O LLM navega por metadados, não por blobs |
| **Stateless Router** | O roteador não acumula estado entre requisições |
| **Ephemeral Skills** | Skills são carregados sob demanda, não persistentes |
| **Token Budget** | Cada tool call paga seu preço em tokens — minimize |

## Implementação

### 1. FastMCP Tool Registration

```python
@mcp.tool()
def search_memory(query: str, limit: int = 3) -> list[dict]:
    """Search persistent memory graph for relevant facts."""
    # Returns lightweight summaries, not raw data
    return [{"id": ..., "summary": ..., "tokens_estimated": 50}]
```

### 2. Registry-First Discovery

O LLM primeiro consulta o *catálogo* de ferramentas (~200 tokens), não o código-fonte. Apenas ferramentas relevantes são instrumentadas.

### 3. Context Folding

Quando múltiplas ferramentas são combinadas, seus resultados são *dobrados* em resumos antes de entrar no contexto do LLM.

## Métricas de Sucesso

- **Token Efficiency Ratio**: tokens de contexto / tokens de output > 10:1
- **Tool Hit Rate**: % de tools chamadas vs. tools disponíveis > 40%
- **Bloat Score**: (contexto total - estrutura) / contexto total < 0.3

## Referência

Este documento inspira a arquitetura do AGency. Consulte [Roster C-Level](ROSTER_C_LEVEL.md) e [Paperclip State Engine](PAPERCLIP_STATE_ENGINE.md) para detalhes de implementação.
