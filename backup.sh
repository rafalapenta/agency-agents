#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/agentic-os-${TIMESTAMP}.tar.gz"

mkdir -p "${BACKUP_DIR}"

echo "Creating backup: ${BACKUP_FILE}"

tar -czf "${BACKUP_FILE}" \
    brain/ \
    skills/ \
    agents/ \
    data/ \
    registry/ \
    standards/ \
    prompts/ \
    --exclude="data/settings.json" \
    2>/dev/null

echo "Backup created: $(du -h "${BACKUP_FILE}" | cut -f1)"
echo "Path: ${BACKUP_FILE}"
