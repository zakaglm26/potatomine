#!/usr/bin/env bash
set -euo pipefail

PORT_VALUE="${PORT:-8080}"
DATA_DIR="${LABEL_STUDIO_DATA_DIR:-/var/lib/label-studio}"

mkdir -p "$DATA_DIR"

echo "Starting Label Studio on 0.0.0.0:${PORT_VALUE}"
echo "Data dir: ${DATA_DIR}"

# Optional: bootstrap admin user if credentials are provided.
# These flags are supported by Label Studio CLI in recent versions.
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
