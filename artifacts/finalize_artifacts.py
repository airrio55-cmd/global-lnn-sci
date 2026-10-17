"""Validate and package a completed full run, optionally waiting for its PID."""
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import sys
import time
import zipfile

import nbformat
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
if len(sys.argv) == 2:
    pid = int(sys.argv[1])
    while Path(f'/proc/{pid}').exists():
        time.sleep(5)

status = json.loads((OUT / 'execution_status.json').read_text())
if status['status'] != 'completed':
    (OUT / 'completion_check.json').write_text(json.dumps({
        'status': 'not_completed', 'execution_status': status['status'],
        'error_type': status.get('error_type'),
    }, indent=2))
    raise SystemExit('Full experiment did not complete; see execution_error.txt')

seed = pd.read_csv(OUT / 'seed_results.csv')
summary = pd.read_csv(OUT / 'final_results.csv')
comparison = pd.read_csv(OUT / 'persistence_comparison.csv')
baseline = pd.read_csv(OUT / 'baselines.csv')
learned = seed[seed['Seed'].astype(str) != 'BASELINE']
assert len(learned) == 45 and len(baseline) == 3 and len(seed) == 48
assert len(summary) == 9 and len(comparison) == 45
assert not learned.duplicated(['Market', 'Feature_Set', 'Model', 'Loss', 'Seed']).any()
assert set(learned['Seed'].astype(int)) == {42, 52, 62, 72, 82}
assert set(learned['Model']) == {'LNN', 'LSTM', 'Transformer'}
assert set(learned['Loss']) == {'CE', 'MILD_WCE', 'MILD_FOCAL'}
assert np.isfinite(learned[['Balanced_Accuracy', 'Macro_F1', 'WF_Val_BA', 'Threshold']]).all().all()
nb = nbformat.read(OUT / 'SCI_v1_4_WALKFORWARD.completed.ipynb', as_version=4)
assert all(c.execution_count is not None for c in nb.cells if c.cell_type == 'code')
assert not any(o.output_type == 'error' for c in nb.cells if c.cell_type == 'code' for o in c.outputs)
nbformat.validate(nb)

pers = baseline[baseline['Model'] == 'Persistence'].iloc[0]
lines = [
    '# S&P500 COMMON_LOCAL + walk-forward 최종 결과', '',
    '전체 실험 완료: 모델 3개 × 손실함수 3개 × seed 5개 = 45개 학습 결과, baseline 3개.', '',
    f'Persistence Test Balanced Accuracy: {pers.Balanced_Accuracy:.6f}; Macro F1: {pers.Macro_F1:.6f}.', '',
    '| Model | Loss | Test BA mean ± SD | Macro F1 mean ± SD | Δ BA vs Persistence | Seeds above Persistence |',
    '|---|---|---:|---:|---:|---:|',
]
for r in summary.sort_values('Balanced_Accuracy_mean', ascending=False).itertuples():
    lines.append(f'| {r.Model} | {r.Loss} | {r.Balanced_Accuracy_mean:.6f} ± {r.Balanced_Accuracy_std:.6f} '
                 f'| {r.Macro_F1_mean:.6f} ± {r.Macro_F1_std:.6f} '
                 f'| {r.Delta_Balanced_Accuracy_mean:+.6f} | {int(r.Seeds_Beating_Persistence)}/5 |')
lines += ['', '## 저장 파일', '',
          '- SCI_v1_4_WALKFORWARD.completed.ipynb: 처음부터 끝까지 실행한 노트북과 결과 출력',
          '- final_results.csv: 모델·손실함수별 평균·표준편차 및 baseline 차이',
          '- seed_results.csv: 45개 학습 결과와 baseline 3개',
          '- persistence_comparison.csv: seed별 Persistence 대비 성능 차이',
          '- baselines.csv, formatted_summary.csv: baseline 및 원본 형식 요약표',
          '- run_manifest.json: 환경·원본 해시·실험 설정', '',
          '## 변경 내용', '',
          '원본 노트북의 모델, seed, 손실함수, epoch, 데이터 구간, threshold 선택 방식은 변경하지 않았습니다. '
          '완료 노트북에는 결과 검증·Persistence 비교·CSV 저장 셀을 추가했습니다. '
          'nbformat이 누락된 cell ID를 보완했습니다. 이전 Yahoo 프록시 403은 네트워크 설정 적용으로 해결됐습니다.', '',
          'Δ BA는 성능 차이이며 통계적 유의성을 뜻하지 않습니다. '
          'preflight_ 파일은 별도 사전 점검 데이터이고 최종 실험 결과와 구분합니다.', '']
(OUT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
check = {'status': 'validated', 'validated_at_utc': datetime.now(timezone.utc).isoformat(),
         'learned_runs': 45, 'baseline_rows': 3, 'summary_rows': 9,
         'notebook_errors': 0, 'all_notebook_code_cells_executed': True}
(OUT / 'completion_check.json').write_text(json.dumps(check, indent=2))
members = ['SCI_v1_4_WALKFORWARD.completed.ipynb', 'final_results.csv', 'seed_results.csv',
           'persistence_comparison.csv', 'baselines.csv', 'formatted_summary.csv', 'results_report.md',
           'README.md', 'run_manifest.json', 'completion_check.json', 'execution_status.json',
           'run_notebook.py', 'finalize_artifacts.py', 'full_execution.log', 'training_live.log']
with zipfile.ZipFile(OUT / 'SCI_v1_4_WALKFORWARD_results.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in members:
        archive.write(OUT / name, name)
print(json.dumps(check), flush=True)
