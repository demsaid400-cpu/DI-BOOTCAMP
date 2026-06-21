#!/usr/bin/env python3
"""
Sanitize and prepare the notebook:
- rename if original contains quotes
- inject a simulation/API wrapper as first cell
- replace absolute /home/claude paths by relative ones
- convert JSON-like output cells into Markdown code blocks
- remove code outputs (clean commit)
"""
import nbformat, re, sys
from nbformat import v4
from pathlib import Path

orig_names = ['"LLM_Powered_Customer_Insights".ipynb', '%22LLM_Powered_Customer_Insights%22.ipynb', 'LLM_Powered_Customer_Insights.ipynb']
target_name = "LLM_Powered_Customer_Insights.ipynb"

def looks_like_output_json(src):
    s = "".join(src) if isinstance(src, list) else str(src)
    return '"returncode"' in s or '"stdout"' in s or '"stderr"' in s or re.search(r'^\s*{\s*"', s)

def find_notebook():
    for n in orig_names:
        p = Path(n)
        if p.exists():
            return p
    for f in Path(".").glob("*LLM*Customer*Insights*.ipynb"):
        return f
    return None

def main():
    p = find_notebook()
    if p is None:
        print("Aucun notebook trouvé. Placez le notebook à la racine du repo et relancez.")
        sys.exit(1)

    print(f"Chargement du notebook : {p}")
    nb = nbformat.read(p, as_version=4)

    # Simulation wrapper cell (code)
    sim_code = """
# SIMULATION / SAFE API WRAPPER
import os, random
API_KEY = os.getenv("ANTHROPIC_API_KEY")
SIMULATE = API_KEY is None
if SIMULATE:
    print("SIMULATION mode (no ANTHROPIC_API_KEY).")
else:
    print("LIVE API mode (ANTHROPIC_API_KEY present).")

def call_api_or_simulate(text):
    if SIMULATE:
        random.seed(len(text))
        sentiment = random.choice(["Positive","Neutral","Negative"])
        return {"text": text, "sentiment": sentiment, "confidence": round(random.uniform(0.6,0.99),2), "topics": []}
    else:
        # Implement real API call in notebook when ready
        return {"_note": "API mode - implement real call using ANTHROPIC_API_KEY"}
""".strip()

    first_cell = v4.new_code_cell(source=sim_code)
    if nb.cells and "ANTHROPIC_API_KEY" in "".join(nb.cells[0].get("source","")):
        nb.cells[0] = first_cell
    else:
        nb.cells.insert(0, first_cell)

    for cell in nb.cells:
        src = "".join(cell.get("source","")) if isinstance(cell.get("source"), list) else str(cell.get("source",""))
        # replace absolute paths
        src = src.replace("/home/claude/llm_api_integration", "./llm_api_integration").replace("/home/claude/llm_api_integration/notebooks", "./notebooks")
        # convert output-like code to markdown
        if cell.get("cell_type") == "code" and looks_like_output_json(cell.get("source","")):
            md = "```json\n" + src + "\n```"
            cell["cell_type"] = "markdown"
            cell["source"] = md
            cell["outputs"] = []
            cell["execution_count"] = None
        else:
            cell["source"] = src
            if cell.get("cell_type") == "code":
                cell["outputs"] = []
                cell["execution_count"] = None

    target_path = Path(target_name)
    print(f"Écriture du notebook nettoyé : {target_path}")
    nbformat.write(nb, target_path)
    if p.name != target_name:
        print(f"Le fichier original {p.name} est conservé en l'état (vous pouvez le supprimer manuellement).")

if __name__ == "__main__":
    main()
