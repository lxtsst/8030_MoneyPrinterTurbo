#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_PATH="${MPT_CONFIG_PATH:-/MoneyPrinterTurbo/config.toml}"

if [[ "${1:-}" == "streamlit" && -n "${MPT_WEBUI_BASE_PATH:-}" ]]; then
  BASE_URL_PATH="${MPT_WEBUI_BASE_PATH%%/}"
  if [[ -n "$BASE_URL_PATH" ]]; then
    set -- "$@" "--server.baseUrlPath=$BASE_URL_PATH"
  fi
fi

python3 "$SCRIPT_DIR/render-mpt-config.py" "$CONFIG_PATH"
exec "$@"
