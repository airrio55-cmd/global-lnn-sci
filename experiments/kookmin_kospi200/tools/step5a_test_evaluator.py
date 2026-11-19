"""Fail-closed STEP5A financial Test entrypoint; performs no artifact reads."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from kospi200.step5a_evaluation import financial_test_entrypoint
if __name__=='__main__':financial_test_entrypoint()
