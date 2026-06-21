#!/usr/bin/env bash
set -euo pipefail

# run_nbconvert.sh
# Usage: ./scripts/run_nbconvert.sh <notebook-filename>
# Runs nbconvert in a robust way using relative paths.

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 notebooks/LLM_Powered_Customer_Insights.ipynb"
  exit 2
fi

NOTEBOOK_PATH="$1"
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
NOTEBOOKS_DIR="${NOTEBOOKS_DIR:-$REPO_ROOT/notebooks}"

# Normalize path
if [[ "$NOTEBOOK_PATH" != /* ]]; then
  FULL_PATH="$REPO_ROOT/$NOTEBOOK_PATH"
else
  FULL_PATH="$NOTEBOOK_PATH"
fi

if [ ! -f "$FULL_PATH" ]; then
  echo "Error: Notebook not found: $FULL_PATH"
  exit 3
fi

cd "$(dirname "$FULL_PATH")"
NOTEBOOK_FILE="$(basename "$FULL_PATH")"
OUTPUT_NAME="$(basename "$NOTEBOOK_FILE" .ipynb)_executed.ipynb"

python3 -m nbconvert --to notebook --execute "$NOTEBOOK_FILE" --output "$OUTPUT_NAME" --ExecutePreprocessor.timeout=600 --ExecutePreprocessor.kernel_name=python3

echo "✅ Executed notebook written to: $(pwd)/$OUTPUT_NAME"
