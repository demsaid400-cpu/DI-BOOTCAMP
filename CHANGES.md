# Changes applied on branch fix/notebook-filenames

- Added .gitignore to exclude outputs, .env and caches.
- Added .env.example with ANTHROPIC_API_KEY and BASE_DIR placeholders.
- Added scripts/normalize_notebook.py which creates a cleaned copy of the notebook:
  - Converts shell-like code cells to bash cells (adds %%bash)
  - Replaces absolute /home/claude paths with a BASE_DIR placeholder
  - Prepends a cell that defines BASE_DIR from environment variable

Next steps (run locally or CI):

1. In your local clone, check out the branch:
   git fetch origin
   git checkout fix/notebook-filenames

2. Run the normalization script to generate the cleaned notebook:
   python3 scripts/normalize_notebook.py

   This will read the encoded-name notebook "%22LLM_Powered_Customer_Insights%22.ipynb" in the repo root and write the cleaned file LLM_Powered_Customer_Insights.ipynb

3. Inspect the produced notebook, commit it if everything looks good, and open a PR to merge into main.

If you want, I can (in a follow-up) open the PR for you after generating and committing the cleaned notebook.
