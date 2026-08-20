from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml
from pydantic import ValidationError
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from src.database.models import Agent, AgentTool, Base
from src.database.schemas import AgentCreate

_COLLECTION_NAME = 'agency_agents'
_IGNORED_FILENAMES = {
 'README.md',
 'CONTRIBUTING.md',
 'CLAUDE.md',
 'AGENTS.md',
 'LICENSE.md',
}
_ROLE_PATTERN = re.compile(r'(?mi)^\s*-\s*\*\*Role\*\*:\s*(.+?)\s*$')
_TOKEN_PATTERN = re.compile(r'(?u)\b[\w-]+\b')


@dataclass(frozen=True, slots=True)
class IndexingReport:
 discovered: int
 valid: int
 invalid: int
 written: int
 errors: list[str] = field(default_factory=list)


class HashEmbeddingFunction:
 def __init__(self, dimensions: int = 256) -> None:
  if dimensions < 16:
   raise ValueError('embedding dimensions must be at least 16')
  self.dimensions = dimensions

 def __call__(self, input: list[str]) -> list[list[float]]:
  vectors: list[list[float]] = []
  for document in input:
   vector = [0.0] * self.dimensions
   for token in _TOKEN_PATTERN.findall(document.casefold()):
    digest = hashlib.blake2b(token.encode('utf-8'), digest_size=8).digest()
    index = int.from_bytes(digest[:4], 'little') % self.dimensions
    sign = 1.0 if digest[4] & 1 else -1.0
    vector[index] += sign
   norm = math.sqrt(sum(value * value for value in vector)) or 1.0
   vectors.append([value / norm for value in vector])
  return vectors


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
 if not text.startswith('---'):
  raise ValueError('missing YAML frontmatter')
 lines = text.splitlines()
 try:
  closing = lines.index('---', 1)
 except ValueError as exc:
  raise ValueError('unterminated YAML frontmatter') from exc
 raw = '\n'.join(lines[1:closing])
 metadata = yaml.safe_load(raw) or {}
 if not isinstance(metadata, dict):
  raise ValueError('YAML frontmatter must be a mapping')
 return metadata, '\n'.join(lines[closing + 1 :])


def _non_empty_string(value: Any) -> str | None:
 if not isinstance(value, str):
  return None
 value = value.strip()
 return value or None


def _trigger_hooks(metadata: dict[str, Any], body: str) -> list[str]:
 candidates: list[str | None] = [
  _non_empty_string(metadata.get('description')),
  _non_empty_string(metadata.get('vibe')),
 ]
 role_match = _ROLE_PATTERN.search(body)
 candidates.append(role_match.group(1).strip() if role_match else None)
 return list(dict.fromkeys(value for value in candidates if value))


def parse_agent_markdown(path: Path, source_root: Path) -> AgentCreate:
 source_root = source_root.resolve()
 path = path.resolve()
 try:
  relative = path.relative_to(source_root)
 except ValueError as exc:
  raise ValueError(f'agent path is outside source root: {path}') from exc
 if len(relative.parts) < 2:
  raise ValueError('agent Markdown must live inside a macro-domain directory')

 metadata, body = _split_frontmatter(path.read_text(encoding='utf-8'))
 macro_domain = relative.parts[0]
 squad = relative.parts[-2] if len(relative.parts) > 2 else None

 return AgentCreate(
  agent_id=path.stem,
  macro_domain=macro_domain,
  squad=squad,
  name=metadata.get('name'),
  system_prompt_path=relative.as_posix(),
  trigger_hooks=_trigger_hooks(metadata, body),
  is_active=True,
 )


def discover_agent_files(source_root: Path) -> Iterable[Path]:
 for path in sorted(source_root.rglob('*.md')):
  if path.name in _IGNORED_FILENAMES or any(part.startswith('.') for part in path.parts):
   continue
  if path.parent == source_root:
   continue
  yield path


def _persist_relational(agents: list[AgentCreate], database_url: str, reindex: bool) -> None:
 engine = create_engine(database_url)
 Base.metadata.create_all(engine)
 with Session(engine) as session, session.begin():
  if reindex:
   session.execute(delete(AgentTool))
   session.execute(delete(Agent))
  for item in agents:
   session.merge(
    Agent(
     agent_id=item.agent_id,
     macro_domain=item.macro_domain,
     squad=item.squad,
     name=item.name,
     system_prompt_path=item.system_prompt_path,
     trigger_hooks=item.trigger_hooks,
     is_active=item.is_active,
    )
   )


def _persist_vectors(
 agents: list[AgentCreate],
 chroma_path: Path,
 reindex: bool,
 embedding_function: HashEmbeddingFunction,
) -> None:
 import chromadb

 client = chromadb.PersistentClient(path=str(chroma_path))
 names = {
  item.name if hasattr(item, 'name') else str(item)
  for item in client.list_collections()
 }
 if reindex and _COLLECTION_NAME in names:
  client.delete_collection(_COLLECTION_NAME)
 collection = client.get_or_create_collection(
  name=_COLLECTION_NAME,
  metadata={'hnsw:space': 'cosine'},
 )
 if not agents:
  return
 documents = ['\n'.join(item.trigger_hooks) for item in agents]
 collection.upsert(
  ids=[item.agent_id for item in agents],
  documents=documents,
  metadatas=[
   {
    'agent_id': item.agent_id,
    'macro_domain': item.macro_domain,
    'squad': item.squad or '',
   }
   for item in agents
  ],
  embeddings=embedding_function(documents),
 )


def run_indexing(
 *,
 source_root: Path,
 database_url: str,
 chroma_path: Path,
 dry_run: bool,
 reindex: bool,
 embedding_function: HashEmbeddingFunction | None = None,
) -> IndexingReport:
 if not dry_run and not reindex:
  raise ValueError('persistent catalog changes require reindex=True')
 files = list(discover_agent_files(source_root))
 agents: list[AgentCreate] = []
 errors: list[str] = []
 for path in files:
  try:
   agents.append(parse_agent_markdown(path, source_root))
  except (OSError, ValueError, ValidationError, yaml.YAMLError) as exc:
   errors.append(f'{path}: {exc}')

 if dry_run or errors:
  return IndexingReport(
   discovered=len(files),
   valid=len(agents),
   invalid=len(errors),
   written=0,
   errors=errors,
  )

 embedder = embedding_function or HashEmbeddingFunction()
 _persist_relational(agents, database_url, reindex)
 _persist_vectors(agents, chroma_path, reindex, embedder)
 return IndexingReport(
  discovered=len(files),
  valid=len(agents),
  invalid=0,
  written=len(agents),
  errors=[],
 )


def build_parser() -> argparse.ArgumentParser:
 parser = argparse.ArgumentParser(description='Validate and index the agency-agents catalog')
 parser.add_argument('source_root', type=Path, help='Path to the read-only agency-agents checkout')
 parser.add_argument('--database-url', default='sqlite:///data/catalog.db')
 parser.add_argument('--chroma-path', type=Path, default=Path('data/chroma'))
 parser.add_argument('--dry-run', action='store_true', help='Validate without writing SQLite or ChromaDB')
 parser.add_argument('--reindex', action='store_true', help='Explicitly rebuild the persisted catalog')
 return parser


def main(argv: list[str] | None = None) -> int:
 args = build_parser().parse_args(argv)
 report = run_indexing(
  source_root=args.source_root,
  database_url=args.database_url,
  chroma_path=args.chroma_path,
  dry_run=args.dry_run,
  reindex=args.reindex,
 )
 print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
 return 0 if report.invalid == 0 else 2


if __name__ == '__main__':
 raise SystemExit(main())
