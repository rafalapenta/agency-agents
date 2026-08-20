"""Context compression for orchestration handoffs.

Reduces payload size before passing context between domain agents
while preserving essential fields for downstream consumption.

The compressor removes verbose or redundant keys and truncates
oversized text fields to keep handoff payloads lean.
"""
from __future__ import annotations

import copy
from typing import Any

# Fields always preserved in compressed output
_ESSENTIAL_KEYS = frozenset({
    "task_id",
    "title",
    "status",
    "priority",
    "assignee",
    "macro_domain",
    "source_agent",
    "target_agent",
    "state_version",
    "created_at",
    "updated_at",
    "error",
    "result",
})

# Fields removed during compression (verbose/diagnostic)
_DROP_KEYS = frozenset({
    "full_log",
    "raw_response",
    "debug_trace",
    "intermediate_steps",
    "embedding_vector",
    "token_usage_details",
    "internal_metadata",
})

# Maximum length (in chars) for any single string value after compression
_MAX_STRING_LEN = 2000


def compress_context(
    context: dict[str, Any],
    *,
    essential_keys: frozenset[str] | None = None,
    drop_keys: frozenset[str] | None = None,
    max_string_len: int = _MAX_STRING_LEN,
) -> dict[str, Any]:
    """Return a compressed copy of *context*.

    Strategy:
      1. Remove keys in *drop_keys*.
      2. Truncate string values longer than *max_string_len*.
      3. Recursively compress nested dicts.
      4. Always preserve keys in *essential_keys*.

    Returns a new dict; the original is never mutated.
    """
    essentials = essential_keys or _ESSENTIAL_KEYS
    drops = drop_keys or _DROP_KEYS

    return _compress(context, essentials=essentials, drops=drops, max_len=max_string_len)


def _compress(
    obj: Any,
    *,
    essentials: frozenset[str],
    drops: frozenset[str],
    max_len: int,
) -> Any:
    if isinstance(obj, dict):
        result: dict[str, Any] = {}
        for key, value in obj.items():
            if key in drops and key not in essentials:
                continue
            result[key] = _compress(
                value, essentials=essentials, drops=drops, max_len=max_len
            )
        return result

    if isinstance(obj, list):
        return [
            _compress(item, essentials=essentials, drops=drops, max_len=max_len)
            for item in obj
        ]

    if isinstance(obj, str) and len(obj) > max_len:
        return obj[:max_len] + "… [truncated]"

    # Scalars pass through
    return copy.deepcopy(obj) if isinstance(obj, (dict, list)) else obj
