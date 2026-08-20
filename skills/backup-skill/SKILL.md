---
name: backup-skill
description: Creates and manages backup snapshots
version: 1.0.0
author: Agentic OS
tags: [backup, recovery, snapshot]
---

# Backup Skill

## Description
Creates compressed backup snapshots of brain/, skills/, registry/, standards/, and agents/. Supports scheduled auto-backup and manual on-demand backups.

## When to Use
- Daily scheduled backup
- Before making major changes
- On-demand from dashboard

## Process
1. Create tar.gz of brain/, skills/, agents/, registry/, standards/, prompts/
2. Exclude data/settings.json (contains API keys)
3. Name file with timestamp: agentic-os-YYYYMMDD_HHMMSS.tar.gz
4. Store in backups/ directory
5. Keep last 30 backups, remove older ones
6. Log to audit trail

## Output
Compressed archive file

## Agent Assignment
- Primary: opencode
