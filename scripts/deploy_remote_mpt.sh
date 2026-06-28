#!/usr/bin/env bash
set -euo pipefail

REMOTE="${1:-}"
REMOTE_DIR="${2:-}"
ENV_FILE="${3:-.env}"

if [[ -z "$REMOTE" || -z "$REMOTE_DIR" ]]; then
  echo "Usage: $0 <user>@<host> <remote-dir> [env-file]"
  exit 2
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCAL_ENV_PATH="${PROJECT_ROOT}/${ENV_FILE}"

if [[ ! -f "$LOCAL_ENV_PATH" ]]; then
  echo "Missing environment file: $LOCAL_ENV_PATH"
  echo "Run cp .env.example .env and fill values first."
  exit 1
fi

rsync -a \
  --exclude='.env' \
  --exclude='storage/' \
  --exclude='.venv/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='*.log' \
  "$PROJECT_ROOT/" "${REMOTE}:${REMOTE_DIR}/"

scp "$LOCAL_ENV_PATH" "${REMOTE}:${REMOTE_DIR}/.env"
ssh "$REMOTE" "chmod 600 '${REMOTE_DIR}/.env'"

ssh "$REMOTE" "mkdir -p '${REMOTE_DIR}/storage'"
ssh "$REMOTE" "cd '${REMOTE_DIR}' && docker compose -f docker-compose.release.yml down || true"
ssh "$REMOTE" "cd '${REMOTE_DIR}' && docker compose -f docker-compose.release.yml up -d --build"

echo "Deploy completed: ${REMOTE}:${REMOTE_DIR}"
