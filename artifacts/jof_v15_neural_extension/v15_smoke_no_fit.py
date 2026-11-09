"""V15 model topology + determinism smoke check. No training, no real datasets, no AUC."""
import argparse, importlib.util, json, platform, sys
from pathlib import Path
import numpy as np

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path)
    a=p.parse_args()
    here=Path(__file__).resolve().parent
    spec=importlib.util.spec_from_file_location("v15_locked_runner",here/"v15_locked_runner.py")
    runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
    import torch, sklearn
    try:
        import ncps
    except ImportError as e:
        raise SystemExit("SMOKE BLOCKED: install audited ncps version before topology test") from e
    torch.set_num_threads(2)
    x=torch.arange(4*20*8,dtype=torch.float32).reshape(4,20,8)/1000.
    reports=[]
    with torch.inference_mode():
        for arch in ("LSTM","LTC","CfC"):
            runner.configure_seed(42)
            m1=runner.build_model(arch,8).eval()
            z1=m1(x)
            runner.configure_seed(42)
            m2=runner.build_model(arch,8).eval()
            z2=m2(x)
            if z1.shape!=(4,2) or not torch.isfinite(z1).all():
                raise RuntimeError(f"{arch}: invalid shape or non-finite logits")
            if not torch.equal(z1,z2):
                raise RuntimeError(f"{arch}: same-seed CPU output not bitwise reproducible")
            reports.append({"model":arch,"input":[4,20,8],"logits":[4,2],
                            "bitwise_same_seed_cpu":True,
                            "parameters":sum(t.numel() for t in m1.parameters())})
    out={"status":"SMOKE_PASS","no_fitting":True,"no_historical_labels":True,
         "torch":torch.__version__,"ncps":getattr(ncps,"__version__","unknown"),
         "python":platform.python_version(),"models":reports}
    if a.out:
        if a.out.exists():raise FileExistsError(a.out)
        a.out.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))

if __name__=="__main__":main()
