from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload

from src.catalog.indexer import HashEmbeddingFunction
from src.database.models import Agent, AgentTool


class CatalogEmptyError(RuntimeError):
 pass


class RouterUnavailableError(RuntimeError):
 pass


class RouterDataError(RuntimeError):
 pass


class AuthorizedTool(BaseModel):
 model_config = ConfigDict(extra='forbid')

 tool_id: str
 name: str
 description: str
 tool_type: str
 read_only: bool
 input_schema: dict = Field(default_factory=dict)
 output_schema: dict = Field(default_factory=dict)
 permissions_override: dict | None = None


class RouteAgentResult(BaseModel):
 model_config = ConfigDict(extra='forbid')

 matched: bool
 score: float | None = None
 agent_id: str | None = None
 name: str | None = None
 macro_domain: str | None = None
 system_prompt: str | None = None
 tools: list[AuthorizedTool] = Field(default_factory=list)
 reason: str


def _read_prompt(source_root: Path, relative_path: str) -> str:
 root = source_root.resolve()
 prompt_path = (root / relative_path).resolve()
 try:
  prompt_path.relative_to(root)
 except ValueError as exc:
  raise RouterDataError('agent prompt path escapes catalog root') from exc
 try:
  return prompt_path.read_text(encoding='utf-8')
 except OSError as exc:
  raise RouterDataError(f'unable to read agent prompt: {relative_path}') from exc


def _authorized_tools(agent: Agent) -> list[AuthorizedTool]:
 tools: list[AuthorizedTool] = []
 for link in sorted(agent.tool_links, key=lambda item: item.tool_id):
  tool = link.tool
  tools.append(
   AuthorizedTool(
    tool_id=tool.tool_id,
    name=tool.name,
    description=tool.description,
    tool_type=tool.tool_type,
    read_only=tool.read_only,
    input_schema=tool.input_schema,
    output_schema=tool.output_schema,
    permissions_override=link.permissions_override,
   )
  )
 return tools


def route_agent(
 query: str,
 threshold: float,
 *,
 database_url: str,
 chroma_path: Path,
 source_root: Path,
 embedding_function: HashEmbeddingFunction | None = None,
) -> RouteAgentResult:
 query = query.strip()
 if not query:
  raise ValueError('query must not be empty')
 if not 0.0 <= threshold <= 1.0:
  raise ValueError('threshold must be between 0 and 1')

 try:
  import chromadb
  from chromadb.errors import NotFoundError

  client = chromadb.PersistentClient(path=str(chroma_path))
  try:
   collection = client.get_collection('agency_agents')
  except NotFoundError as exc:
   raise CatalogEmptyError('agency_agents collection does not exist') from exc
  count = collection.count()
  if count == 0:
   raise CatalogEmptyError('agency_agents collection is empty')
  embedder = embedding_function or HashEmbeddingFunction()
  result = collection.query(
   query_embeddings=embedder([query]),
   n_results=min(5, count),
   include=['distances'],
  )
 except CatalogEmptyError:
  raise
 except Exception as exc:
  raise RouterUnavailableError('ChromaDB query failed') from exc

 ids = result.get('ids') or [[]]
 distances = result.get('distances') or [[]]
 candidate_ids = ids[0]
 candidate_distances = distances[0]
 best_score: float | None = None

 engine = create_engine(database_url)
 with Session(engine) as session:
  for agent_id, distance in zip(candidate_ids, candidate_distances, strict=False):
   score = max(0.0, min(1.0, 1.0 - float(distance)))
   if best_score is None:
    best_score = score
   if score < threshold:
    continue
   statement = (
    select(Agent)
    .where(Agent.agent_id == agent_id, Agent.is_active.is_(True))
    .options(selectinload(Agent.tool_links).selectinload(AgentTool.tool))
   )
   agent = session.scalar(statement)
   if agent is None:
    continue
   return RouteAgentResult(
    matched=True,
    score=score,
    agent_id=agent.agent_id,
    name=agent.name,
    macro_domain=agent.macro_domain,
    system_prompt=_read_prompt(source_root, agent.system_prompt_path),
    tools=_authorized_tools(agent),
    reason='matched semantic candidate above threshold',
   )

 return RouteAgentResult(
  matched=False,
  score=best_score,
  tools=[],
  reason='no active candidate met the threshold',
 )
