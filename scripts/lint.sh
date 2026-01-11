#!/usr/bin/env bash
set -euo pipefail

# Lint/format with auto-fix:
# - Applies safe fixes/formatting
# - Warns if it modified files
# - Fails only if issues remain after fixing

if ! command -v ruff >/dev/null 2>&1; then
  echo "ruff is not installed." >&2
  echo "Install with one of:" >&2
  echo "  - uv sync --extra dev" >&2
  echo "  - pip install -e '.[dev]'" >&2
  exit 2
fi

# Apply formatting + fixes
ruff format
ruff check --fix

# Warn if any changes were applied
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if ! git diff --quiet HEAD; then
    echo "WARNING: ruff applied auto-fixes/formatting. Review and commit changes." >&2
    git --no-pager diff --name-only HEAD >&2 || true
  fi
fi

# Gate: ensure the resulting tree is clean w.r.t. lint rules/formatting
ruff format --check
ruff check
