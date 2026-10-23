"""Run the protocol-locked EUROSTOXX50 notebook; validate, optionally commit/push.

From repository root, with the existing Python 3.12 environment activated:
    python -u artifacts/eurostoxx50/run_experiment.py --publish
Publishing is opt-in and uses normal, non-force Git push to origin/main.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback
import zipfile

import nbformat
from nbclient import NotebookClient
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SOURCE = OUT / 'SCI_v1_4_WALKFORWARD_EUROSTOXX50.ipynb'
NAME = 'SCI_v1_4_WALKFORWARD_EUROSTOXX50'
os.chdir(ROOT)
for key, value in {
    'OMP_NUM_THREADS': '2', 'MKL_NUM_THREADS': '2', 'XDG_CACHE_HOME': '/workspace/.cache',
    'IPYTHONDIR': '/workspace/.ipython', 'JUPYTER_CONFIG_DIR': '/workspace/.jupyter',
    'JUPYTER_DATA_DIR': '/workspace/.local/share/jupyter',
    'JUPYTER_RUNTIME_DIR': '/workspace/.local/share/jupyter/runtime',
}.items():
    os.environ.setdefault(key, value)


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def save_json(name, value):
    temporary = OUT / (name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False))
    temporary.replace(OUT / name)


def git(*args):
    result = subprocess.run(['git', *args], cwd=ROOT, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def validate_outputs(nb, source_hashes):
    nbformat.validate(nb)
    code = [c for c in nb.cells if c.cell_type == 'code']
    assert all(c.execution_count is not None for c in code)
    assert not any(o.output_type == 'error' for c in code for o in c.outputs)
    for name, digest in source_hashes.items():
        assert hashlib.sha256((OUT / name).read_bytes()).hexdigest() == digest, f'Source changed during run: {name}'
    yahoo_hashes = json.loads((OUT / 'unchanged_yahoo_sources.json').read_text())
    for name, digest in yahoo_hashes.items():
        assert hashlib.sha256((OUT / 'sources' / (name + '.csv')).read_bytes()).hexdigest() == digest
    lock = json.loads((OUT / 'protocol_lock.json').read_text())
    assert hashlib.sha256((ROOT / lock['german_rate_path']).read_bytes()).hexdigest() == lock['german_rate_sha256']
    data_manifest = json.loads((OUT / 'data_manifest.json').read_text())
    assert hashlib.sha256((OUT / 'market_input.csv').read_bytes()).hexdigest() == data_manifest['sha256']
    results = pd.read_csv(OUT / 'seed_results.csv')
    summary = pd.read_csv(OUT / 'summary.csv')
    comparison = pd.read_csv(OUT / 'persistence_comparison.csv')
    baseline = pd.read_csv(OUT / 'baselines.csv')
    learned = results[results.Seed.astype(str) != 'BASELINE']
    assert len(results) == 48 and len(learned) == 45 and len(baseline) == 3
    assert len(summary) == 9 and len(comparison) == 45
    assert not learned.duplicated(['Market', 'Feature_Set', 'Model', 'Loss', 'Seed']).any()
    assert set(learned.Market) == {'EUROSTOXX50'} and set(learned.Feature_Set) == {'COMMON_LOCAL'}
    assert np.isfinite(learned[['Balanced_Accuracy', 'Macro_F1', 'WF_Val_BA', 'Threshold']]).all().all()
    predictions = sorted((OUT / 'predictions').glob('*.csv'))
    assert len(predictions) == 90
    for file in predictions:
        frame = pd.read_csv(file)
        assert len(frame) > 0 and frame.Probability.between(0, 1).all()
        assert set(frame.Y_true.unique()) <= {0, 1}
    assert json.loads((OUT / 'leakage_audit.json').read_text())['status'] == 'passed'
    check = {'status': 'validated', 'validated_at_utc': timestamp(), 'learned_runs': 45,
             'baseline_rows': 3, 'summary_rows': 9, 'prediction_files': 90,
             'all_code_cells_executed': True, 'notebook_errors': 0,
             'source_hashes_unchanged': True, 'thresholds_checked_against_validation_only': True}
    save_json('completion_check.json', check)


def publication_files():
    names = ['README.md', 'results_report.md', 'seed_results.csv', 'summary.csv',
             'formatted_summary.csv', 'persistence_comparison.csv', 'baselines.csv',
             NAME + '.ipynb', NAME + '.completed.ipynb', 'execution.log',
             'execution_status.json', 'completion_check.json', 'protocol_lock.json',
             'data_manifest.json', 'leakage_audit.json', 'market_input.csv', 'run_manifest.json',
             'preflight.py', 'export_results.py', 'run_experiment.py', 'acquire_inputs.py',
             'sources_manifest.json', 'availability.csv', 'unchanged_yahoo_sources.json', 'local_preflight.log', 'local_preflight_check.py']
    return ([OUT / name for name in names] + sorted((OUT / 'predictions').glob('*.csv'))
            + sorted((OUT / 'sources').glob('*.csv')))


def package_results(files):
    destination = OUT / (NAME + '_results.zip')
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            assert file.is_file(), str(file)
            archive.write(file, str(file.relative_to(OUT)))
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
    return destination


def publish(files):
    assert git('branch', '--show-current') == 'main', 'Publication requires current branch main'
    assert not git('diff', '--cached', '--name-only'), 'Preserve unrelated staged work; publication stopped'
    # Preserve any pre-existing local edits rather than committing them accidentally.
    assert not git('diff', '--name-only'), 'Tracked edits need review before automatic publication'
    secret = re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|[?&]token=[A-Za-z0-9]{20,})')
    for file in files:
        if file.suffix != '.zip':
            assert not secret.search(file.read_text()), f'Credential-like content needs review: {file.name}'
    git('fetch', 'origin', 'main')
    git('merge', '--ff-only', 'origin/main')
    git('add', '--', *[str(p.relative_to(ROOT)) for p in files])
    staged = git('diff', '--cached', '--name-only').splitlines()
    assert staged and all(name.startswith('artifacts/eurostoxx50/') for name in staged)
    git('diff', '--cached', '--check')
    git('commit', '-m', 'Add protocol-preserving EUROSTOXX50 walk-forward experiment results')
    commit = git('rev-parse', 'HEAD')
    git('push', 'origin', 'main')
    remote_commit = git('ls-remote', 'origin', 'refs/heads/main').split()[0]
    assert remote_commit == commit, 'Remote main verification failed'
    save_json('publication.json', {'status': 'published', 'commit': commit,
                                 'branch': 'main', 'verified_at_utc': timestamp(),
                                 'file_count': len(staged)})
    print('PUBLISHED', commit, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    if (OUT / 'execution_status.json').exists():
        previous = json.loads((OUT / 'execution_status.json').read_text())
        if previous.get('status') == 'running' and Path('/proc/' + str(previous.get('pid'))).exists():
            raise RuntimeError('An experiment is already active; do not launch a duplicate.')
    if (OUT / 'completion_check.json').exists():
        raise RuntimeError('A completed run exists. Preserve it rather than overwriting/retraining automatically.')
    nb = nbformat.read(SOURCE, as_version=4)
    lock = json.loads((OUT / 'protocol_lock.json').read_text())
    packages = {name: importlib.metadata.version(name) for name in lock['packages']}
    assert packages == lock['packages'], 'Package versions differ from the fixed protocol environment'
    for index, digest in lock['unchanged_cell_hashes'].items():
        assert hashlib.sha256(nb.cells[int(index)].source.encode()).hexdigest() == digest
    for cell in nb.cells:
        if cell.cell_type == 'code':
            cell.outputs = []
            cell.execution_count = None
    sources = [SOURCE.name, 'preflight.py', 'export_results.py', 'protocol_lock.json', 'run_experiment.py', 'acquire_inputs.py']
    source_hashes = {name: hashlib.sha256((OUT / name).read_bytes()).hexdigest() for name in sources}
    save_json('run_manifest.json', {'started_at_utc': timestamp(), 'python': sys.version,
                                  'device': 'CPU', 'threads': 2, 'base_commit': lock['base_commit'],
                                  'source_hashes': source_hashes, 'packages': packages,
                                  'publish_requested': args.publish})
    status = {'status': 'running', 'started_at_utc': timestamp(), 'pid': os.getpid(),
              'configuration': 'EUROSTOXX50 COMMON_LOCAL; unchanged original training protocol; all 45 runs'}
    save_json('execution_status.json', status)
    save_json('publication.json', {'status': 'pending_completion' if args.publish else 'not_requested'})
    save_json('progress.json', {'status': 'starting', 'completed_runs': 0, 'expected_runs': 45})

    with (OUT / 'execution.log').open('w', encoding='utf-8') as log:
        class LoggedClient(NotebookClient):
            def process_message(self, msg, cell, cell_index):
                content = msg.get('content', {})
                kind = msg.get('msg_type', msg.get('header', {}).get('msg_type'))
                if kind == 'stream':
                    log.write(content.get('text', ''))
                    log.flush()
                elif kind == 'error':
                    log.write('\n'.join(content.get('traceback', [])) + '\n')
                    log.flush()
                return super().process_message(msg, cell, cell_index)

        client = LoggedClient(nb, timeout=None, kernel_name='global-lnn-sci', record_timing=True,
                              resources={'metadata': {'path': str(ROOT)}})

        def checkpoint(cell, cell_index, **kwargs):
            nbformat.write(nb, OUT / (NAME + '.in_progress.ipynb'))
            log.write(f'\nCompleted cell {cell_index}\n')
            log.flush()

        client.on_cell_executed = checkpoint
        try:
            client.execute()
            status.update(status='completed', completed_at_utc=timestamp())
        except BaseException as exc:
            status.update(status='failed', error_type=type(exc).__name__, error=str(exc), failed_at_utc=timestamp())
            (OUT / 'execution_error.txt').write_text(traceback.format_exc())
            raise
        finally:
            suffix = '.completed.ipynb' if status['status'] == 'completed' else '.execution_attempt.ipynb'
            nbformat.write(nb, OUT / (NAME + suffix))
            status['executed_code_cells'] = sum(c.cell_type == 'code' and c.execution_count is not None for c in nb.cells)
            status['error_cells'] = [i for i, c in enumerate(nb.cells)
                                   if c.cell_type == 'code' and any(o.output_type == 'error' for o in c.outputs)]
            save_json('execution_status.json', status)
    # The committed execution log is now closed and cannot become dirty after publication.
    validate_outputs(nb, source_hashes)
    save_json('progress.json', {'status': 'completed', 'completed_runs': 45, 'expected_runs': 45,
                               'completed_at_utc': timestamp()})
    files = publication_files()
    archive = package_results(files)
    if args.publish:
        try:
            publish(files + [archive])
        except BaseException as exc:
            save_json('publication.json', {'status': 'failed', 'error_type': type(exc).__name__,
                                         'error': str(exc), 'at_utc': timestamp()})
            raise
    print('COMPLETE: 45 runs validated; results saved in', OUT, flush=True)


if __name__ == '__main__':
    main()
