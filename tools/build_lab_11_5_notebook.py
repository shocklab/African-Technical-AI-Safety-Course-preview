#!/usr/bin/env python3
"""Build the standalone Session 11 audit notebook; analysis requires no models."""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
cells = []
def add(kind, source):
    cell = {'cell_type': kind, 'metadata': {}, 'source': source.splitlines(keepends=True)}
    if kind == 'code':
        cell.update(execution_count=None, outputs=[])
    cells.append(cell)
def M(text): add('markdown', text)
def C(text): add('code', text)
M('''# Session 11.5: audit a multilingual safety evaluation

Use a standard CPU runtime. This notebook uses only Python, NumPy and pandas, which are provided by Colab. It does not install or load a language model.

Bring `session-9-results.json` from the revised Session 9 notebook, or an instructor-provided de-identified export. The file must contain the original prompt IDs, translations, responses, labels and exclusions. Identify the data source in your report.

If you only have an older notebook's saved outputs, those outputs do not restore its runtime variables. Reconstruct the labelled table from the displayed outputs or request a class export. Do not invent missing translations or labels.

The optional synthetic example below is arithmetic practice only. It contains assumed labels and no generated responses or translations. It cannot support a claim about a real model, isiZulu or Afrikaans.
''')
C('''import json
from pathlib import Path
import numpy as np
import pandas as pd

USE_WORKED_EXAMPLE = False  # Change to True only for synthetic arithmetic practice.
RESULT_PATH = Path('session-9-results.json')
''')
C((ROOT/'tools/multilingual_audit.py').read_text())
example = json.loads((ROOT/'docs/labs/data/session-11-paired-worked-example.json').read_text())
C('WORKED_EXAMPLE = json.loads('+repr(json.dumps(example,ensure_ascii=False))+''')
if USE_WORKED_EXAMPLE:
    payload = WORKED_EXAMPLE
else:
    if not RESULT_PATH.exists():
        try:
            from google.colab import files
        except ImportError:
            raise FileNotFoundError('Place your results JSON beside this notebook or set RESULT_PATH.')
        uploaded = files.upload()
        if len(uploaded) != 1:
            raise ValueError('Upload exactly one results JSON file.')
        payload = json.loads(next(iter(uploaded.values())).decode('utf-8'))
    else:
        payload = json.loads(RESULT_PATH.read_text(encoding='utf-8'))

scores, exclusions = read_results(payload)
print('SYNTHETIC ARITHMETIC ONLY' if payload['synthetic'] else 'Saved labelled observations')
print('Provenance:', json.dumps(payload.get('provenance', {}), ensure_ascii=False, indent=2))
print('Excluded prompt-language pairs:', exclusions)
print('Retained labelled rows:', len(scores))
''')
M('''## 1. Audit the data and claim

Inspect translation fidelity and the meaning of each label before using the summary. Back-translation is a diagnostic, not a substitute for fluent-speaker review. Record who reviewed the translations and which prompt IDs remain doubtful.

Do not reproduce unsafe responses in your report. These cells display your local data for inspection; uploading it here does not authorise sharing it elsewhere.

`understood`, `refused` and `crossed_boundary` are separate labels. An `unclear` safety outcome must not become `no`. Exclusions remove individual prompt-language rows; the paired analysis then reports missing partners.
''')
C('''with pd.option_context('display.max_colwidth', None, 'display.max_rows', None):
    display(scores)
    translations = pd.DataFrame(payload.get('translations', []))
    if not translations.empty:
        print('Original translations, including excluded rows:')
        display(translations)
''')
M('''## 2. Check denominators and paired outcomes

The coarse validity gate requires at least two of the three original benign controls understood in each condition, plus at least two safety pairs understood in both languages with determinate outcomes. It does not establish fluency or translation validity.

The primary paired estimate is conditional on those eligible prompts. Changing eligibility changes the question being answered. Report all missing, not-understood and unclear prompt IDs. When unclear outcomes are present, the analysis also prints the paired gap with every unclear label scored yes, with every one scored no, and its range over every way of scoring them. Report that range beside the primary estimate. Report conditional refusal with its own denominator and unclear-refusal count.

The percentile bootstrap below is exploratory resampling spread. A tiny purposive sample cannot justify reliable population inference. Identical observed differences may produce a collapsed interval: that is not certainty or equivalence. Neither resampling nor the comprehension gate resolves systematic translation or labelling errors.
''')
C('''report_comparisons(scores)
if payload['synthetic']:
    print('These assumed labels illustrate pairing only. No empirical model or language conclusion is permitted.')
''')
M('''## 3. Write a one-page audit

Include:

- The model and revision, prompt set, translation route, single-turn format and outcome definition.
- Data provenance, translation reviewer, eligible IDs and all exclusions or unclear labels.
- Raw paired counts, each denominator, the paired gap and exploratory resampling spread.
- Benign-control and comprehension results, including an unresolved comparison if the gate fails.
- Two concrete threats to validity and a conclusion limited to the observed prompts and setup.

For the synthetic exercise, replace the model/language conclusion with an explanation of the arithmetic and the evidence that would be needed for a real evaluation.

Save this notebook and retain the input JSON locally. No model rerun is needed for this audit.

## Sources

- [Session 11.4: statistics of evaluations](https://shocklab.github.io/African-Technical-AI-Safety-Course/sessions/session-11/statistics-of-evals.html).
- [Miller (2024), Adding Error Bars to Evals](https://arxiv.org/html/2411.00640v1#S4.SS2).
''')
for index, cell in enumerate(cells):
    cell["id"] = "s11-cell-" + str(index)

notebook = {'cells': cells, 'metadata': {'colab': {'provenance': []},
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3'}}, 'nbformat': 4, 'nbformat_minor': 5}
json.dump(notebook, sys.stdout, indent=1, ensure_ascii=False)
sys.stdout.write('\n')
