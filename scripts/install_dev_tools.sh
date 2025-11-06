#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN=${PYTHON_BIN:-python3}

"${PYTHON_BIN}" -m pip install --upgrade pip
"${PYTHON_BIN}" -m pip install \
  "ruff>=0.1.0" \
  "pytest>=7.0.0,<8.0.0" \
  "pytest-asyncio>=0.21.0" \
  "pytest-cov>=4.0.0" \
  "respx>=0.20.0" \
  "tiktoken>=0.5.0"
