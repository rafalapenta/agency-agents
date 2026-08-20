# Router Core — evidências de aceitação

Data: 2026-08-14

## Ambiente isolado

- Python 3.11 em `%TEMP%\aggency-phase1-venv`.
- SQLAlchemy 2.0.52.
- ChromaDB 1.5.9.
- FastMCP 2.14.7.
- Dependências originais do `agentic-os` instaladas por `requirements.txt`.

## Testes

- Schemas Pydantic e ORM: exit code 0.
- Indexador dry-run/reindex/SQLite/Chroma cosine: exit code 0.
- Router e FastMCP in-memory: exit code 0.
- Suíte completa: `python -m pytest tests -q` → `PYTEST_EXIT=0`.
- Duração observada da suíte completa: 27.311 ms.

## Benchmark route_agent

Comando: `python -m scripts.benchmark_route_agent`

- Warmup: 20 chamadas.
- Amostras: 200 chamadas.
- Cold: 24,985 ms.
- P50: 15,713 ms.
- P95: 23,193 ms.
- P99: 29,848 ms.
- Máximo: 38,789 ms.
- Meta: P95 menor que 500 ms.
- Resultado: PASS, exit code 0.

O benchmark mede o caminho ChromaDB → SQLite → leitura do prompt → montagem da resposta. Inicialização/indexação não integra as amostras warm e é reportada separadamente.

## Limitações aceitas da Phase 1

- Feature hashing é local, determinístico e barato, mas tem qualidade semântica inferior a modelos densos; o provider permanece ponto de evolução configurável.
- SQLite e ChromaDB não compartilham transação distribuída. Falhas entre as duas escritas exigem nova execução explícita de `--reindex`.
- O warning `AuthlibDeprecationWarning` vem do FastMCP 2.14.7 e não altera os resultados.

## Verificação no diretório oficial

Destino: C:\Users\RAFAEL\Desktop\Projetos Hermes\AGgency

- Backup preservado: C:\Users\RAFAEL\Desktop\Projetos Hermes\AGgency-pre-layer1-20260814-155029.zip.
- Overlay: 174 arquivos copiados; 0 divergências SHA-256.
- Suíte completa oficial: PYTEST_EXIT=0.
- Benchmark oficial: 200 amostras, 20 warmups; cold 32,43 ms; P50 20,793 ms; P95 28,795 ms; P99 37,026 ms; máximo 42,349 ms; BENCHMARK_EXIT=0.
- Indexador oficial: HELP_EXIT=0.
- Fixture oficial dry-run: DRYRUN_EXIT=0; descobertos 0, válidos 0, inválidos 0, erros 0; SQLite e ChromaDB não foram criados.

A integração da Phase 1 está concluída no diretório oficial. O catálogo completo continua sendo uma etapa posterior de dados, não um bloqueio do Router Core.
