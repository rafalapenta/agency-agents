from __future__ import annotations

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.database.models import Agent, AgentTool, Base, Tool


def test_models_persist_agent_tool_allowlist_and_cascade() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    with engine.connect() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        agent = Agent(
            agent_id="engineering-frontend-developer",
            macro_domain="engineering",
            name="Frontend Developer",
            system_prompt_path="engineering/engineering-frontend-developer.md",
            trigger_hooks=["frontend applications"],
        )
        tool = Tool(
            tool_id="repo-search",
            name="Repository Search",
            tool_type="fastmcp",
            connection_config={},
            input_schema={},
            output_schema={},
        )
        session.add_all([agent, tool])
        session.flush()
        session.add(
            AgentTool(
                agent_id=agent.agent_id,
                tool_id=tool.tool_id,
                permissions_override={"paths": ["src/**"]},
            )
        )
        session.commit()

        stored = session.scalar(select(Agent).where(Agent.agent_id == agent.agent_id))
        assert stored is not None
        assert stored.trigger_hooks == ["frontend applications"]
        assert [item.tool_id for item in stored.tool_links] == ["repo-search"]
        assert stored.tool_links[0].permissions_override == {"paths": ["src/**"]}

        session.delete(tool)
        session.commit()
        assert session.scalar(select(AgentTool)) is None
