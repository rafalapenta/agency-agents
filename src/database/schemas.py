from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ToolType(StrEnum):
    MCP_SERVER = "mcp_server"
    FASTMCP = "fastmcp"
    PYTHON_SCRIPT = "python_script"
    WEBHOOK = "webhook"


class CatalogModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class AgentCreate(CatalogModel):
    agent_id: str = Field(min_length=1)
    macro_domain: str = Field(min_length=1)
    squad: str | None = None
    name: str = Field(min_length=1)
    system_prompt_path: str = Field(min_length=1)
    trigger_hooks: list[str] = Field(min_length=1)
    is_active: bool = True

    @field_validator("trigger_hooks")
    @classmethod
    def normalize_trigger_hooks(cls, values: list[str]) -> list[str]:
        normalized = [value.strip() for value in values if value.strip()]
        if not normalized:
            raise ValueError("at least one non-empty trigger hook is required")
        return list(dict.fromkeys(normalized))


class ToolCreate(CatalogModel):
    tool_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = ""
    tool_type: ToolType
    connection_config: dict[str, Any] = Field(default_factory=dict)
    read_only: bool = False
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)


class AgentToolCreate(CatalogModel):
    agent_id: str = Field(min_length=1)
    tool_id: str = Field(min_length=1)
    permissions_override: dict[str, Any] | None = None
