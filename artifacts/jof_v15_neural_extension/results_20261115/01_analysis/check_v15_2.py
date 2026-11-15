import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, hashlib, importlib.util
import numpy as np
import pandas as pd

repo = Path("/repo")
data = Path("/data")
post = Path("/post")
frozen = repo / "artifacts/jof_v15_neural_extension"
sys.path.insert(0, str(frozen))

def sha(p):
    with p.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

import v15_locked_runner as runner
_, anchor = runner.check_lock(
    repo, frozen / "V15_CONFIG_LOCKED.json",
    "/authorization/record.json", require_analysis=True
)
assert anchor == "d866841eeb87c63f42bd10240c7acc06ee7dbe49"

change = json.loads((post / "change_record.json").read_text())
assert sha(post / "analysis_v15_2.py") == change["patched_analysis_sha256"]
assert sha(frozen / "v15_analysis_draft.py") == change["original_analysis_sha256"]

source = data / "results/v15_predictions.csv"
before = sha(source)
assert before == "71da5806ba5de6d42d62e7c47a553f015bd82426513ea02abd691d610d04c756"

analysis = load("v15_analysis_draft", post / "analysis_v15_2.py")
def no_auc(*args, **kwargs):
    raise RuntimeError("AUC is forbidden during validation")
analysis.roc_auc_score = no_auc

old_ops = data / "operations/v15_1/controller.py"
old_hashes = json.loads((data / "operations_sha256.json").read_text())
assert sha(old_ops) == old_hashes["v15_1/controller.py"]
ops = load("recorded_controller", old_ops)
ops.OUT = post

jobs = json.loads((frozen / "step4/job_manifest.json").read_text())["jobs"]
state = json.loads((data / "job_status.json").read_text())
assert len(jobs) == len(state["completed_artifacts"]) == 1080
assert all(state["states"][j["fit_id"]] == "COMPLETE" for j in jobs)

ops.final_validation(data / "results", jobs, state["completed_artifacts"])

p = pd.read_csv(source, float_precision="round_trip")
index = p.index[p.Model == "CfC_ENSEMBLE"][0]
value = np.float32(p.at[index, "Probability"])
direction = np.float32(0 if value > 0 else 1)
p.at[index, "Probability"] = float(np.nextafter(value, direction))
try:
    analysis.validate_predictions(repo, p)
except AssertionError:
    pass
else:
    raise RuntimeError("STOP: altered ensemble was not rejected")

assert sha(source) == before
report = {
    "status": "PASS",
    "completed_job_artifacts_checked": 1080,
    "float32_ensemble_exact": True,
    "one_float32_step_corruption_rejected": True,
    "predictions_sha256": before,
    "original_predictions_unchanged": True,
    "training_performed": False,
    "AUC_performed": False
}
(post / "validation_report.json").write_text(json.dumps(report, indent=2) + "\n")
print("V15_2_VALIDATION_PASS: 1080 jobs; exact ensemble; corruption rejected; NO_TRAINING_NO_AUC")
