"""Execute the full original experiment and export reports only after success.

Run from the repository with the configured global-lnn-sci Python environment:
    python artifacts/run_notebook.py
"""
from pathlib import Path
import json
import os
import traceback

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts'
os.chdir(ROOT)
os.environ.setdefault('OMP_NUM_THREADS', '2')
os.environ.setdefault('MKL_NUM_THREADS', '2')
nb = nbformat.read(ROOT / 'SCI_v1_4_WALKFORWARD.ipynb', as_version=4)
for cell in nb.cells:
    if cell.cell_type == 'code':
        cell.outputs = []
        cell.execution_count = None

nb.cells.append(nbformat.v4.new_markdown_cell(
    '## 실행 결과 내보내기 및 Persistence 비교\n'
    '원본 실험의 모델·seed·loss·epoch 설정을 유지합니다. '
    '아래 표의 차이는 Test Balanced Accuracy 기준이며 통계적 유의성을 의미하지 않습니다.'
))
nb.cells.append(nbformat.v4.new_code_cell('''
from pathlib import Path
from itertools import product
output_dir = Path('artifacts')
output_dir.mkdir(exist_ok=True)
learned = global_results[global_results['Seed'].astype(str) != 'BASELINE'].copy()
baseline = global_results[global_results['Seed'].astype(str) == 'BASELINE'].copy()
expected = set(product(RUN_MARKETS, RUN_FEATURE_SETS, RUN_MODELS, RUN_LOSS_MODES, SEEDS))
keys = ['Market', 'Feature_Set', 'Model', 'Loss', 'Seed']
assert set(learned[keys].itertuples(index=False, name=None)) == expected
assert len(learned) == len(expected), 'Missing or duplicate runs'
metrics = ['Accuracy', 'Balanced_Accuracy', 'Macro_F1', 'F1', 'Recall', 'Precision',
           'Pred_Pos_Rate', 'WF_Val_BA', 'WF_Val_Macro_F1', 'Threshold']
assert np.isfinite(learned[metrics].to_numpy(dtype=float)).all()
summary = learned.groupby(['Market', 'Feature_Set', 'Model', 'Loss'])[metrics].agg(['mean', 'std'])
summary.columns = ['_'.join(c) for c in summary.columns]
summary = summary.reset_index()
persistence = baseline[baseline['Model'] == 'Persistence'][
    ['Market', 'Feature_Set', 'Balanced_Accuracy', 'Macro_F1', 'Accuracy']
].rename(columns={m: 'Persistence_' + m for m in ['Balanced_Accuracy', 'Macro_F1', 'Accuracy']})
comparison = learned.merge(persistence, on=['Market', 'Feature_Set'], validate='many_to_one')
for metric in ['Balanced_Accuracy', 'Macro_F1', 'Accuracy']:
    comparison['Delta_' + metric] = comparison[metric] - comparison['Persistence_' + metric]
summary = summary.merge(persistence, on=['Market', 'Feature_Set'], validate='many_to_one')
summary['Delta_Balanced_Accuracy_mean'] = summary['Balanced_Accuracy_mean'] - summary['Persistence_Balanced_Accuracy']
summary['Seeds_Beating_Persistence'] = [
    int(((comparison['Market'] == row.Market) & (comparison['Feature_Set'] == row.Feature_Set)
         & (comparison['Model'] == row.Model) & (comparison['Loss'] == row.Loss)
         & (comparison['Delta_Balanced_Accuracy'] > 0)).sum())
    for row in summary.itertuples()
]
global_results.to_csv(output_dir / 'seed_results.csv', index=False, encoding='utf-8-sig')
global_summary.to_csv(output_dir / 'formatted_summary.csv', index=False, encoding='utf-8-sig')
summary.to_csv(output_dir / 'final_results.csv', index=False, encoding='utf-8-sig')
comparison.to_csv(output_dir / 'persistence_comparison.csv', index=False, encoding='utf-8-sig')
baseline.to_csv(output_dir / 'baselines.csv', index=False, encoding='utf-8-sig')
display(summary)
display(baseline)
report = '# S&P500 COMMON_LOCAL + walk-forward results\\n\\n'
report += summary.to_string(index=False) + '\\n\\nPersistence and other baselines:\\n'
report += baseline.to_string(index=False)
report += '\\n\\nChanges: appended reporting/export cells only; original experiment settings unchanged.\\n'
(output_dir / 'results_report.md').write_text(report, encoding='utf-8')
print('Verified', len(learned), 'learned runs; reports exported to', output_dir.resolve())
'''))

client = NotebookClient(
    nb, timeout=None, kernel_name='global-lnn-sci', record_timing=True,
    resources={'metadata': {'path': str(ROOT)}},
)


def checkpoint(cell, cell_index, **kwargs):
    nbformat.write(nb, OUT / 'SCI_v1_4_WALKFORWARD.in_progress.ipynb')
    print(f'Completed cell {cell_index}', flush=True)


client.on_cell_executed = checkpoint
status = {'status': 'running', 'configuration': 'original full experiment plus reporting cells'}
try:
    client.execute()
    status['status'] = 'completed'
except Exception as exc:
    status.update(status='failed', error_type=type(exc).__name__, error=str(exc))
    (OUT / 'execution_error.txt').write_text(traceback.format_exc())
finally:
    filename = ('SCI_v1_4_WALKFORWARD.completed.ipynb' if status['status'] == 'completed'
                else 'SCI_v1_4_WALKFORWARD.execution_attempt.ipynb')
    nbformat.write(nb, OUT / filename)
    status['executed_code_cells'] = sum(c.cell_type == 'code' and c.execution_count is not None for c in nb.cells)
    status['error_cells'] = [i for i, c in enumerate(nb.cells)
                           if c.cell_type == 'code' and any(o.output_type == 'error' for o in c.outputs)]
    (OUT / 'execution_status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2))
if status['status'] != 'completed':
    raise SystemExit(1)
