#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="backups"

if [ $# -eq 0 ]; then
    echo "Available backups:"
    ls -1t "${BACKUP_DIR}"/*.tar.gz 2>/dev/null || echo "  No backups found in ${BACKUP_DIR}/"
    echo ""
    echo "Usage: ./restore.sh <backup-file>"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "ERROR: Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

echo "Restoring from: ${BACKUP_FILE}"
echo "WARNING: This will overwrite current brain/, skills/, agents/, data/, registry/, standards/, prompts/"

read -p "Continue? (y/N): " CONFIRM
if [ "${CONFIRM}" != "y" ] && [ "${CONFIRM}" != "Y" ]; then
    echo "Cancelled."
    exit 0
fi

tar -xzf "${BACKUP_FILE}" 2>/dev/null

echo "Restore complete!"
