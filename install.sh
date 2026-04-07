#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="cf"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but not found in PATH."
  exit 1
fi

if [ ! -d "${VENV_DIR}" ]; then
  python3 -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip
python -m pip install playwright
python -m playwright install chromium

deactivate

echo "Done. Virtual environment is in ./${VENV_DIR}"
