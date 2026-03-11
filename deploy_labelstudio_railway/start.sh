#!/usr/bin/env bash
set -euo pipefail

PORT_VALUE="${PORT:-8080}"
DATA_DIR="${LABEL_STUDIO_DATA_DIR:-/app/.data}"

mkdir -p "$DATA_DIR"

echo "Starting Label Studio on 0.0.0.0:${PORT_VALUE}"
echo "Data dir: ${DATA_DIR}"

EXTRA_ARGS=()
if [[ -n "${LABEL_STUDIO_USERNAME:-}" ]]; then
  EXTRA_ARGS+=("--username" "${LABEL_STUDIO_USERNAME}")
fi
if [[ -n "${LABEL_STUDIO_PASSWORD:-}" ]]; then
  EXTRA_ARGS+=("--password" "${LABEL_STUDIO_PASSWORD}")
fi

label-studio start \
  --internal-host 0.0.0.0 \
  --port "${PORT_VALUE}" \
  --data-dir "${DATA_DIR}" \
  --no-browser \
  --init \
  "${EXTRA_ARGS[@]}"
