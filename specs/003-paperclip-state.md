# 003 — State Management (RFC 7396)

> Status: Implemented (Phase 2)

## Overview

The state layer provides persistent, auditable task and orchestration state
management using RFC 7396 JSON Merge Patch semantics.

## Components

### `src/state/merge_patch.py`

Pure-Python implementation of [RFC 7396](https://datatracker.ietf.org/doc/html/rfc7396):

- **Null removal**: patch key with `null` value → remove from target.
- **Recursive dict merge**: nested dicts are merged recursively.
- **Atomic scalar/array replacement**: non-dict patches replace the target entirely.
- **Immutable**: returns a new dict; never mutates the input.

### `src/state/manager.py`

Persistent `StateManager` with:

- **Monotonic versioning**: `state_version` increments on every `apply()`.
- **Append-only journal**: `journal.jsonl` records every patch with timestamp and source.
- **Atomic persistence**: `os.replace()` ensures no partial writes on crash.
- **Cross-platform locking**: `fcntl` on POSIX, `msvcrt` on Windows.
- **Thread-safety**: `threading.Lock` for in-process concurrency.

## Invariants

1. `state_version` is strictly monotonic and never decreases.
2. `state_version` cannot be overridden by external patches.
3. Every mutation is recorded in the journal before the state file is written.
4. The state file is never partially written (atomic via temp + replace).

## Evidence

- Unit tests validate merge-patch RFC compliance.
- State invariant checked in the macro orchestration quality gates.
