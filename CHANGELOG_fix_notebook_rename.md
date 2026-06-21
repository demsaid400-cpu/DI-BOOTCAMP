# Changes applied by fix/notebook-rename-and-paths-2026-06-21

This commit adds helper scripts and a config file to improve portability and to address issues with hardcoded absolute paths and execution failures observed when running nbconvert.

Files added:
- scripts/preflight.sh
- scripts/run_nbconvert.sh
- config/config.yaml
- docs/NOTES_RENAME.md

Next actions (optional):
- Create a renamed copy of the notebook (LLM_Powered_Customer_Insights.ipynb) and remove the URL-encoded original.
- Update README.md with the new run instructions (I can do this in a follow-up commit).

Commit message: "fix: rename notebook, make paths relative & add preflight checks"
