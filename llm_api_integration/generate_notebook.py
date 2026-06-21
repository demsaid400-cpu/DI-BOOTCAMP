import json
import os

# Simple generator that writes a runnable notebook demonstrating LLM integration with simulation fallback
nb = {
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}},
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# 🤖 LLM API Integration — Text Intelligence Pipeline\n",
        "This notebook demonstrates a reproducible pipeline that calls an LLM (Anthropic Claude) when an API key is provided, and uses a deterministic simulation fallback otherwise.\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {},
      "execution_count": null,
      "outputs": [],
      "source": [
        "import os\n",
        "import json\n",
        "from pathlib import Path\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "# Optional: anthropic client only used if API key is present\n",
        "try:\n",
        "    import anthropic\n",
        "except Exception:\n",
        "    anthropic = None\n",
        "\n",
        "ROOT = Path('llm_api_integration')\n",
        "OUT = ROOT / 'outputs'\n",
        "OUT.mkdir(parents=True, exist_ok=True)\n",
        "\n",
        "API_KEY = os.environ.get('ANTHROPIC_API_KEY')\n",
        "\n",
        "# deterministic simulation fallback (useful for CI and no-key runs)\n",
        "def simulate_analysis(text):\n",
        "    t = text.lower()\n",
        "    if any(w in t for w in ['good','excellent','super','love','great']):\n",
        "        sentiment = 'Positive'\n",
        "    elif any(w in t for w in ['bad','terrible','hate','poor','worst']):\n",
        "        sentiment = 'Negative'\n",
        "    else:\n",
        "        sentiment = 'Neutral'\n",
        "    topics = []\n",
        "    if 'delivery' in t or 'ship' in t or 'late' in t:\n",
        "        topics.append('logistics')\n",
        "    if 'battery' in t or 'screen' in t or 'charge' in t:\n",
        "        topics.append('product_quality')\n",
        "    if 'price' in t or 'expensive' in t or 'cheap' in t:\n",
        "        topics.append('price')\n",
        "    return {\n",
        "        'sentiment': sentiment,\n",
        "        'confidence': 0.85,\n",
        "        'topics': topics or ['general'],\n",
        "        'raw_text': text\n",
        "    }\n",
        "\n",
        "def call_llm(text):\n",
        "    # If anthropic is available and API key present, call the real API\n",
        "    if anthropic is not None and API_KEY:\n",
        "        client = anthropic.Client(api_key=API_KEY)\n",
        "        system = 'You are a JSON-outputting analyzer. Return JSON with keys: sentiment, confidence, topics.'\n",
        "        prompt = f'Analyze the following review and return JSON:\\n{text}'\n",
        "        try:\n",
        "            resp = client.completions.create(model='claude-sonnet-4-6', prompt=system + '\\n' + prompt, max_tokens=300, temperature=0.1)\n",
        "            # depending on the anthropic SDK version the field names differ; we attempt to parse safely\n",
        "            text_resp = getattr(resp, 'completion', None) or resp.get('completion') if isinstance(resp, dict) else str(resp)\n",
        "            # Try extracting JSON from the response body\n",
        "            import re\n",
        "            m = re.search(r'\{.*\}', text_resp, re.S)\n",
        "            if m:\n",
        "                return json.loads(m.group(0))\n",
        "        except Exception as e:\n",
        "            print('LLM call failed, falling back to simulation:', e)\n",
        "    # fallback\n",
        "    return simulate_analysis(text)\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {},
      "execution_count": null,
      "outputs": [],
      "source": [
        "# Create a small sample dataset to process\n",
        "REVIEWS = [\n",
        "    ('Super product, battery lasts long and screen is beautiful', 'Electronics'),\n",
        "    ('Delivery was late and package damaged', 'Electronics'),\n",
        "    ('Okay value for money', 'Clothing'),\n",
        "    ('Terrible quality, broke after one use', 'Sports'),\n",
        "    ('Excellent! Loved it', 'Books')\n",
        "]\n",
        "df = pd.DataFrame(REVIEWS, columns=['text','category'])\n",
        "df['id'] = range(1, len(df)+1)\n",
        "df.head()\n"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {},
      "execution_count": null,
      "outputs": [],
      "source": [
        "# Process reviews through LLM (real or simulated) and save results\n",
        "results = []\n",
        "for _, row in df.iterrows():\n",
        "    analysis = call_llm(row['text'])\n",
        "    analysis['id'] = int(row['id'])\n",
        "    analysis['category'] = row['category']\n",
        "    results.append(analysis)\n",
        "\n",
        "OUT_FILE = OUT / 'api_results.json'\n",
        "with open(OUT_FILE, 'w', encoding='utf-8') as f:\n",
        "    json.dump(results, f, ensure_ascii=False, indent=2)\n",
        "\n",
        "# Create simple features CSV (sentiment label)\n",
        "feat_df = pd.DataFrame([{'id': r['id'], 'sentiment': r['sentiment'], 'topics': ','.join(r.get('topics',[]))} for r in results])\n",
        "feat_df.to_csv(OUT / 'llm_features.csv', index=False, encoding='utf-8')\n",
        "print('Saved results to', OUT_FILE)\n",
        "feat_df.head()\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Notes\n",
        "- The notebook uses a deterministic simulation when ANTHROPIC_API_KEY is not set.\n",
        "- To call the real API set the environment variable ANTHROPIC_API_KEY and ensure the anthropic python package is installed.\n",
        "- This notebook is designed to be CI-friendly and reproducible.\n"
      ]
    }
  ]
}

os.makedirs('llm_api_integration/notebooks', exist_ok=True)
with open('llm_api_integration/notebooks/llm_api_integration.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Generated llm_api_integration/notebooks/llm_api_integration.ipynb')
