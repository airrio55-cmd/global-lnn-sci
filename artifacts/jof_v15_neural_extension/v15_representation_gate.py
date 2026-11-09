"""V15 representation provenance gate. This module never trains a model."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

MARKETS = ("SP500", "NASDAQ100", "NIKKEI225", "EUROSTOXX50", "KOSPI200")
ALLOWED = {"verified_historical", "new_prespecified"}

def validate_representation(config_path, repo_root):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    rep = config.get("log_representation_provenance")
    if not isinstance(rep, dict):
        raise ValueError("Missing LOG provenance. V15 LOCK IS BLOCKED.")
    if rep.get("classification") not in ALLOWED:
        raise ValueError("LOG provenance must identify verified historical or new prespecified variant")
    if not rep.get("formula") or not rep.get("time_alignment_rule"):
        raise ValueError("Missing exact LOG formula or prediction-time alignment")
    if not rep.get("source_description"):
        raise ValueError("Missing LOG source details")
    columns = config.get("log_columns")
    if not isinstance(columns, dict) or set(columns) != set(MARKETS):
        raise ValueError("Must map each of five markets")
    for market in MARKETS:
        cols = columns[market]
        if not isinstance(cols, list) or not cols or len(set(cols)) != len(cols):
            raise ValueError(f"{market}: invalid LOG columns")
    paths = rep.get("source_file_sha256")
    if not isinstance(paths, dict) or not paths:
        raise ValueError("Missing LOG source file SHA256 inventory")
    root = Path(repo_root).resolve()
    for rel, expected in paths.items():
        p = (root / rel).resolve()
        if not p.is_relative_to(root) or not p.is_file():
            raise ValueError(f"LOG source missing or outside repository: {rel}")
        observed = hashlib.sha256(p.read_bytes()).hexdigest()
        if observed != expected:
            raise ValueError(f"LOG source changed: {rel}")
    if config.get("status") != "LOCKED":
        raise ValueError("Draft config: full fit forbidden")
    return True

if __name__ == "__main__":
    raise SystemExit("Import validate_representation; this is not a training script.")
