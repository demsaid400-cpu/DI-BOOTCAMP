"""normalize_notebook.py

Script to normalize and clean the notebook named with encoded quotes:
"%22LLM_Powered_Customer_Insights%22.ipynb -> LLM_Powered_Customer_Insights.ipynb

What it does:
- Loads the original notebook (encoded name) from repo root
- Prepends a cell that sets BASE_DIR from environment or default
- Replaces absolute paths (/home/claude/...) with Path(BASE_DIR)/... in code cell strings
- Converts code cells that contain shell commands (mkdir, cd, pip install, jupyter nbconvert, cat >, echo, etc.) into bash cells by adding a leading "%%bash\n" line
- Writes the cleaned notebook to LLM_Powered_Customer_Insights.ipynb at repo root

Run:
python3 scripts/normalize_notebook.py

"""
import nbformat
from pathlib import Path
import os
import re

ORIG = '%22LLM_Powered_Customer_Insights%22.ipynb'
TARGET = 'LLM_Powered_Customer_Insights.ipynb'

# Heuristics for shell-like lines
SHELL_PATTERNS = [
    r'^\s*(mkdir|cd|pip\s+install|python3?\s+-m\s+jupyter|jupyter|cat\s+>|echo\s+|rm\s+|mv\s+|cp\s+)'
]
SHELL_RE = re.compile('(' + '|'.join(p.strip('^\s*') for p in SHELL_PATTERNS) + ')', re.IGNORECASE)

def is_shell_cell(source_lines):
    # source_lines can be a single string or list
    if isinstance(source_lines, list):
        lines = source_lines
    else:
        lines = source_lines.splitlines()
    for ln in lines[:6]:
        if SHELL_RE.search(ln):
            return True
    return False


def replace_absolute_paths(text):
    # Replace common absolute path prefixes used in the notebook
    text = text.replace('/home/claude/llm_api_integration', "{BASE_DIR}/llm_api_integration")
    text = text.replace('/home/claude', '{BASE_DIR}')
    return text


def main():
    p = Path(ORIG)
    if not p.exists():
        print(f'Original notebook not found at {ORIG}. Please ensure the encoded-name notebook exists in the repo root.')
        return

    nb = nbformat.read(str(p), as_version=4)

    # Prepend a python cell that defines BASE_DIR
    base_cell = nbformat.v4.new_code_cell(source=[
        "import os\n",
        "from pathlib import Path\n",
        "BASE_DIR = os.environ.get('BASE_DIR', './llm_api_integration')\n",
        "BASE_DIR = str(Path(BASE_DIR))\n",
        "print('BASE_DIR =', BASE_DIR)\n",
    ])

    new_cells = [base_cell]

    for cell in nb.cells:
        if cell.cell_type == 'code':
            src = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
            # Replace absolute paths with {BASE_DIR} placeholder
            new_src = replace_absolute_paths(src)

            # If seems like shell, convert to bash magic
            if is_shell_cell(new_src):
                # Ensure the cell starts with bash magic
                if not new_src.lstrip().startswith('%%bash') and not new_src.lstrip().startswith('%%shell'):
                    new_src = '%%bash\n' + new_src
                # Also replace occurrences of {BASE_DIR} with $BASE_DIR for bash cells
                new_src = new_src.replace('{BASE_DIR}', '$BASE_DIR')
                new_cell = nbformat.v4.new_code_cell(source=new_src)
            else:
                # For python cells, replace {BASE_DIR} with f-string using BASE_DIR variable
                new_src = new_src.replace('{BASE_DIR}', "os.path.join(BASE_DIR)")
                # A safer approach: replace patterns like os.path.join(BASE_DIR)/... is not perfect, but we keep a simple substitution
                new_cell = nbformat.v4.new_code_cell(source=new_src)
            new_cells.append(new_cell)
        else:
            # keep markdown as-is
            new_cells.append(cell)

    nb.cells = new_cells

    target_path = Path(TARGET)
    nbformat.write(nb, str(target_path))
    print(f'Wrote cleaned notebook to {target_path}')

if __name__ == '__main__':
    main()
