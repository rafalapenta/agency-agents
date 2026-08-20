-- 135_agent_tool_catalog.sql
-- Database schema for managing Agent Profiles, Tools (MCP/Skills),
-- and N:N Agent-Tool Associations for context isolation and semantic routing.

CREATE TABLE IF NOT EXISTS agents (
  agent_id TEXT PRIMARY KEY,
  macro_domain TEXT NOT NULL,
  squad TEXT, -- Permite nulo para agentes globais de orquestração
  name TEXT NOT NULL,
  system_prompt_path TEXT NOT NULL,
  trigger_hooks TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(trigger_hooks)), -- JSON array of strings
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tools (
  tool_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '', -- Ajuda a LLM/Agente a entender o papel da tool
  tool_type TEXT NOT NULL CHECK(tool_type IN ('mcp_server', 'fastmcp', 'python_script', 'webhook')),
  connection_config TEXT NOT NULL DEFAULT '{}' CHECK(json_valid(connection_config)), -- JSON object
  read_only INTEGER NOT NULL DEFAULT 0,
  input_schema TEXT NOT NULL DEFAULT '{}' CHECK(json_valid(input_schema)), -- JSON Schema object
  output_schema TEXT NOT NULL DEFAULT '{}' CHECK(json_valid(output_schema)), -- JSON Schema object
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS agent_tools (
  agent_id TEXT NOT NULL,
  tool_id TEXT NOT NULL,
  permissions_override TEXT CHECK(permissions_override IS NULL OR json_valid(permissions_override)), -- JSON object (optional)
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (agent_id, tool_id),
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id) ON DELETE CASCADE,
  FOREIGN KEY (tool_id) REFERENCES tools(tool_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_agents_macro_domain ON agents(macro_domain);
CREATE INDEX IF NOT EXISTS idx_agents_squad ON agents(squad);
CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active);
CREATE INDEX IF NOT EXISTS idx_tools_type ON tools(tool_type);
CREATE INDEX IF NOT EXISTS idx_agent_tools_agent_id ON agent_tools(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_tools_tool_id ON agent_tools(tool_id);
