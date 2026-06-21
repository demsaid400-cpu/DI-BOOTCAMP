#!/usr/bin/env bash
set -euo pipefail

# Preflight script for the LLM API Integration project
# Creates expected directories, checks for required tools and API key.

REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
NOTEBOOKS_DIR="${NOTEBOOKS_DIR:-$REPO_ROOT/notebooks}"
OUTPUTS_DIR="${OUTPUTS_DIR:-$REPO_ROOT/outputs}"
DATA_DIR="${DATA_DIR:-$REPO_ROOT/data}"
CONFIG_DIR="${CONFIG_DIR:-$REPO_ROOT/config}"
SCRIPTS_DIR="${SCRIPTS_DIR:-$REPO_ROOT/scripts}"

mkdir -p "$NOTEBOOKS_DIR" "$OUTPUTS_DIR" "$DATA_DIR" "$CONFIG_DIR" "$SCRIPTS_DIR"

echo "✅ Directories ensured:"
echo "  - $NOTEBOOKS_DIR"
echo "  - $OUTPUTS_DIR"
echo "  - $DATA_DIR"
echo "  - $CONFIG_DIR"

# Check for ANTHROPIC_API_KEY
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "⚠️  ANTHROPIC_API_KEY not found in environment."
  echo "   The project will run in SIMULATION mode unless you export ANTHROPIC_API_KEY."
  echo "   To run with a real key: export ANTHROPIC_API_KEY=sk-..."
  echo "   Exporting MODE=simulation for current shell session."
  export MODE=simulation
else
  echo "✅ ANTHROPIC_API_KEY found — running in LIVE mode."
  export MODE=live
fi

# Check for jupyter / nbconvert availability
if command -v jupyter >/dev/null 2>&1; then
  echo "✅ jupyter found: $(command -v jupyter)"
else
  echo "⚠️  'jupyter' not found in PATH."
  echo "   You can install it by running:"
  echo "     pip install jupyter nbconvert"
fi

# Check python nbconvert module
if python3 -c "import nbconvert" >/dev/null 2>&1; then
  echo "✅ nbconvert python module available"
else
  echo "⚠️  nbconvert python module not importable. Try: pip install nbconvert"
fi

echo "\nPreflight checks completed. MODE=$MODE"
