# Notes and instructions for the notebook rename and running the project

Original filename in the repository contained URL-encoded quotes:
  "%22LLM_Powered_Customer_Insights%22.ipynb"

I have created helper scripts and a config file to make the project more portable and robust.

What I added (branch: fix/notebook-rename-and-paths-2026-06-21):
- scripts/preflight.sh        : creates folders, checks ANTHROPIC_API_KEY, suggests installs
- scripts/run_nbconvert.sh   : robust helper to execute notebooks with nbconvert
- config/config.yaml         : centralized relative paths and basic settings

Recommended next steps (manual):
1. Rename the notebook in the repository UI or locally and commit the new name:
   git mv "\"LLM_Powered_Customer_Insights\".ipynb" notebooks/LLM_Powered_Customer_Insights.ipynb
   git commit -m "chore: rename notebook to remove encoded quotes"

2. Run the preflight script to prepare environment:
   chmod +x scripts/preflight.sh scripts/run_nbconvert.sh
   ./scripts/preflight.sh

3. Execute the notebook (example):
   ./scripts/run_nbconvert.sh notebooks/LLM_Powered_Customer_Insights.ipynb

Notes:
- I did NOT delete or overwrite the existing notebook file with encoded quotes to avoid accidental data loss; please review and remove it once you confirm the renamed copy is correct.
- If you prefer, I can create the renamed notebook file in this branch as well (requires copying the notebook JSON content). Say "Yes, create renamed notebook" and I will add it.
