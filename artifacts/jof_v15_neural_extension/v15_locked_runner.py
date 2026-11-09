"""V15 neural extension runner (DRAFT). Not runnable before an explicit immutable lock.
V14 frozen input, annual validation fits and two-year test fit are reused unchanged.
No model fitting occurs at import or preflight.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, platform, random, subprocess, sys, time
from datetime import datetime, timezone
from v15_common import require_training, required_inventory, integrity, reference_dates
from v15_representation_gate import validate_representation
from pathlib import Path
import numpy as np
import pandas as pd

MODELS=("LSTM","LTC","CfC")
SEEDS=(42,52,62)
LOGCOLS=("Log_Ret","Disparity20")
ORIGINS=((2013,2015),(2014,2016),(2015,2017),(2016,2018),(2017,2019),(2018,2020))
MARKETS=("SP500","NASDAQ100","NIKKEI225","EUROSTOXX50","KOSPI200")

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check_lock(repo,cfgpath,lockpath,*,require_execution=False,require_analysis=False):
    from v15_locking import check
    return check(repo,cfgpath,lockpath,require_execution=require_execution,require_analysis=require_analysis)

def v14_module(repo):
    path=Path(repo)/"artifacts/jof_v14_preregistered_replication/run_v14_locked.py"
    spec=importlib.util.spec_from_file_location("v14_frozen",path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def configure_seed(seed):
    import torch
    random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
    if torch.cuda.is_available():torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True
    torch.use_deterministic_algorithms(True)

def build_model(name,input_size):
    import torch
    from torch import nn
    if name not in MODELS:raise ValueError("Invalid V15 neural architecture")
    if name=="LSTM":
        seq=nn.LSTM(input_size,128,num_layers=1,batch_first=True)
    else:
        from ncps.torch import LTC,CfC
        seq=(LTC if name=="LTC" else CfC)(input_size,128,batch_first=True)
    class Net(nn.Module):
        def __init__(self):
            super().__init__();self.seq=seq;self.dropout=nn.Dropout(.2);self.fc=nn.Linear(128,2)
            for layer in self.modules():
                if isinstance(layer,nn.Linear):
                    nn.init.xavier_uniform_(layer.weight)
                    if layer.bias is not None:nn.init.zeros_(layer.bias)
        def forward(self,x):
            z,_=self.seq(x)
            return self.fc(self.dropout(z[:,-1,:]))
    return Net()

def window_tensors(train,eval_rows,frame,cols):
    from sklearn.preprocessing import StandardScaler
    if not train or not eval_rows:raise ValueError("Empty train/evaluation window")
    if any(r["index"]<20 or r["index"]>=len(frame) for r in train+eval_rows):raise ValueError("Window index outside frame")
    if max(r["index"]+20 for r in train)>=min(r["index"] for r in eval_rows):raise ValueError("Training label endpoint overlaps evaluation period")
    arr=frame[list(cols)].to_numpy(float);w=20
    used=np.unique(np.concatenate([np.arange(r["index"]-w,r["index"]) for r in train]))
    scaler=StandardScaler().fit(arr[used])
    def x(rows):
        raw=np.stack([arr[r["index"]-w:r["index"]] for r in rows])
        if not np.isfinite(raw).all():raise RuntimeError("Nonfinite LOG/RAW feature window")
        return scaler.transform(raw.reshape(-1,len(cols))).reshape(len(rows),w,len(cols)).astype("float32")
    if not np.isfinite(arr[used]).all():raise ValueError("Nonfinite training scaler input")
    return x(train),x(eval_rows),scaler,used

def fit_predict(name,train,eval_rows,frame,cols,seed,epochs,device,*,cfg=None,artifact_dir=None,execution_authorized=False):
    require_training(cfg or {},execution_authorized=execution_authorized)
    if epochs!=60 or device!="cpu" or seed not in SEEDS or artifact_dir is None:raise RuntimeError("Unapproved fit settings or missing artifact directory")
    import torch
    if not train or not eval_rows:raise RuntimeError("Empty V15 train/evaluation fold")
    y=np.asarray([r["y"] for r in train],dtype=np.int64)
    if np.unique(y).size!=2:raise RuntimeError("One-class training fold")
    xtr,xev,scaler,used=window_tensors(train,eval_rows,frame,cols)
    artifact_dir=Path(artifact_dir);artifact_dir.mkdir(parents=True,exist_ok=False)
    started=datetime.now(timezone.utc).isoformat();epoch_losses=[]
    configure_seed(seed);torch.set_num_threads(2)
    model=build_model(name,xtr.shape[-1]).to(device)
    dataset=torch.utils.data.TensorDataset(torch.from_numpy(xtr),torch.from_numpy(y))
    loader=torch.utils.data.DataLoader(dataset,batch_size=64,shuffle=True,
                            generator=torch.Generator().manual_seed(seed),num_workers=0)
    opt=torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=.0001)
    sch=torch.optim.lr_scheduler.OneCycleLR(opt,max_lr=.005,steps_per_epoch=len(loader),epochs=epochs)
    for epoch in range(epochs):
        model.train();loss_sum=0.;seen=0
        for bx,by in loader:
            bx,by=bx.to(device),by.to(device)
            opt.zero_grad(set_to_none=True)
            loss=torch.nn.functional.cross_entropy(model(bx),by)
            if not torch.isfinite(loss):raise RuntimeError("Nonfinite loss")
            loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
            opt.step();sch.step()
            loss_sum+=float(loss.detach().cpu())*len(by);seen+=len(by)
        epoch_losses.append({"epoch":epoch+1,"train_loss":loss_sum/seen})
        pd.DataFrame(epoch_losses).to_csv(artifact_dir/"training_loss.csv",index=False)
    model.eval()
    with torch.inference_mode():
        preds=torch.cat([torch.softmax(model(torch.from_numpy(part).to(device)),dim=1)[:,1].cpu()
                      for part in np.array_split(xev,max(1,(len(xev)+255)//256))]).numpy()
    if not np.isfinite(preds).all():raise RuntimeError("Nonfinite predictions")
    torch.save({"state_dict":model.cpu().state_dict(),"architecture":name,"input_size":len(cols),"seed":seed,"epochs":epochs,"loss":"CE","probabilities":torch.from_numpy(preds.copy())},artifact_dir/"checkpoint.pt")
    replay_checkpoint(artifact_dir/"checkpoint.pt",xev)
    metadata={"columns":list(cols),"scaler_mean":scaler.mean_.tolist(),"scaler_scale":scaler.scale_.tolist(),"scaler_var":scaler.var_.tolist(),"scaler_used_rows":used.tolist(),"train_dates":[r["Date"] for r in train],"evaluation_dates":[r["Date"] for r in eval_rows],"input_tensor_sha256":hashlib.sha256(xtr.tobytes()).hexdigest(),"eval_tensor_sha256":hashlib.sha256(xev.tobytes()).hexdigest(),"started_at_utc":started,"ended_at_utc":datetime.now(timezone.utc).isoformat()}
    (artifact_dir/"fit_metadata.json").write_text(json.dumps(metadata,indent=2)+"\n")
    pd.DataFrame({"Date":[r["Date"] for r in eval_rows],"Y_true":[r["y"] for r in eval_rows],"Probability":preds,"Y_pred":(preds>.5).astype(int)}).to_csv(artifact_dir/"predictions.csv",index=False,float_format="%.17g")
    return preds

def replay_checkpoint(path,xev):
    """Inference-only reconstruction of trusted local tensor-only checkpoints."""
    import torch
    ck=torch.load(path,map_location="cpu",weights_only=True)
    if ck["architecture"] not in MODELS or xev.ndim!=3 or xev.shape[1:]!=(20,ck["input_size"]):raise ValueError("Checkpoint/input schema mismatch")
    configure_seed(ck["seed"]);torch.set_num_threads(2)
    model=build_model(ck["architecture"],ck["input_size"]);model.load_state_dict(ck["state_dict"],strict=True);model.eval()
    with torch.inference_mode():
        p=torch.cat([torch.softmax(model(torch.from_numpy(part)),1)[:,1] for part in np.array_split(xev,max(1,(len(xev)+255)//256))]).numpy()
    expected=ck["probabilities"].numpy()
    np.testing.assert_allclose(p,expected,atol=1e-7,rtol=0)
    return p

def preflight_dates(v14,repo):
    from v15_preflight_readonly import audit
    return audit(repo)['groups']

def run(repo,cfg,out,*,cfgpath=None,lockpath=None):
    if cfgpath is None or lockpath is None:raise RuntimeError("Separate immutable lock verification required")
    verified,_=check_lock(repo,cfgpath,lockpath,require_execution=True)
    if cfg!=verified:raise RuntimeError("Config changed after lock check")
    from v15_job_manifest import build
    plan=build(repo)
    if plan!=json.loads((Path(repo)/"artifacts/jof_v15_neural_extension/step4/job_manifest.json").read_text()):raise RuntimeError("Execution plan changed after protocol freeze")
    import torch
    v14=v14_module(repo)
    scorefile=Path(repo)/"artifacts/jof_v14_preregistered_replication/first_run_20261109/v14_scoring_dates.csv"
    reference=reference_dates(repo)
    (out/"execution_config.json").write_text(json.dumps(cfg,indent=2)+"\n")
    import importlib.metadata
    (out/"environment.json").write_text(json.dumps({"python":platform.python_version(),"platform":platform.platform(),"device":cfg["device"],"CUBLAS_WORKSPACE_CONFIG":os.environ.get("CUBLAS_WORKSPACE_CONFIG"),"packages":{n:importlib.metadata.version(n) for n in ["torch","ncps","numpy","pandas","scikit-learn"]}},indent=2)+"\n")
    records=[];fit_log=[]
    for market in MARKETS:
        raw,frame,cols,_=v14.load_market(repo,market)
        integrity(raw,frame,cols)
        for vy,ty in ORIGINS:
            origin="O"+str(vy-2012)
            folds=[(vy,vy),(vy+1,vy+1),(ty,ty+1)]
            for start,end in folds:
                period="Validation" if start in (vy,vy+1) and end==start else "Test"
                train=v14.records(frame,raw,cols,f"{raw.index.min().year}-01-01",f"{start-1}-12-31")
                ev=v14.records(frame,raw,cols,f"{start}-01-01",f"{end}-12-31")
                ref=reference[(reference.Market==market)&(reference.Origin==origin)&(reference.Period==period)]
                if period=="Validation":ref=ref[ref.Date.astype(str).str.slice(0,4)==str(start)]
                if [r["Date"] for r in ev]!=ref.Date.astype(str).tolist():
                    raise RuntimeError("V14 scoring dates mismatch")
                for seed in SEEDS:
                    probs={}
                    for name,representation,tag in [
                        ("LSTM","RAW","LSTM"),("LTC","RAW","LTC_RAW"),
                        ("CfC","RAW","CfC_RAW"),("CfC","LOG","CfC_LOG")]:
                        colnames=cols if representation=="RAW" else LOGCOLS
                        t0=time.monotonic()
                        stem=f"{market}_{origin}_{start}_{tag}_{seed}"
                        try:
                            p=fit_predict(name,train,ev,frame,colnames,seed,cfg["epochs"],cfg["device"],cfg=cfg,artifact_dir=out/"fits"/stem,execution_authorized=True)
                        except Exception as error:
                            (out/"failure.json").write_text(json.dumps({"fit":stem,"error_type":type(error).__name__,"message":str(error),"status":"failed_not_complete"},indent=2)+"\n")
                            raise
                        probs[tag]=p
                        fit_log.append({"Market":market,"Origin":origin,"Stage":start,"Model":tag,
                                        "Seed":seed,"TrainN":len(train),"EvalN":len(ev),
                                        "Seconds":time.monotonic()-t0})
                    probs["CfC_ENSEMBLE"]=.5*(probs["CfC_RAW"]+probs["CfC_LOG"])
                    for tag,pr in probs.items():
                        for row,p in zip(ev,pr):
                            signals=row["signals"]
                            records.append({"Market":market,"Origin":origin,"Period":period,
                                "Date":row["Date"],"Model":tag,"Seed":seed,"Probability":float(p),
                                "Y_true":row["y"],"Y_pred":int(p>.5),"s200":signals["200DMA"],"s60":signals["Momentum60"],
                                "s20":signals["Persistence"]})
                pd.DataFrame(records).to_csv(out/"v15_predictions.partial.csv",index=False)
                pd.DataFrame(fit_log).to_csv(out/"v15_fit_diagnostics.partial.csv",index=False)
    pd.DataFrame(records).to_csv(out/"v15_predictions.csv",index=False,float_format="%.17g")
    pd.DataFrame(fit_log).to_csv(out/"v15_fit_diagnostics.csv",index=False)
    if len(fit_log)!=1080:raise RuntimeError("Incomplete planned1080fits")
    (out/"completion_manifest.json").write_text(json.dumps({"status":"fits_complete","fit_count":1080,"prediction_sha256":sha256(out/"v15_predictions.csv"),"protocol_config_sha256":sha256(cfgpath)},indent=2)+"\n")
    # Deliberately leave V14-equivalent statistical test to reviewed analysis script
    (out/"FIT_COMPLETE_EVALUATION_PENDING.txt").write_text("Neural predictions complete. Do not interpret before reviewed V15 analysis.\n")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True,type=Path)
    ap.add_argument("--config",required=True,type=Path)
    ap.add_argument("--lock",required=True,type=Path)
    ap.add_argument("--out",type=Path)
    ap.add_argument("--preflight",action="store_true")
    ap.add_argument("--acknowledge-compute",action="store_true")
    args=ap.parse_args()
    if args.preflight:
        n=preflight_dates(v14_module(args.repo),args.repo)
        print("READ-ONLY PREFLIGHT PASS: "+str(n)+" V14 groups; no model fits")
        return
    if not args.acknowledge_compute:raise SystemExit("Training requires explicit --acknowledge-compute")
    cfg,head=check_lock(args.repo,args.config,args.lock,require_execution=True)
    if args.out is None:raise RuntimeError("--out is required for training")
    if args.out.resolve().is_relative_to(args.repo.resolve()):raise RuntimeError("Write future training outputs outside protected checkout")
    if args.out.exists():raise RuntimeError("Refusing to overwrite a previous result directory")
    args.out.mkdir(parents=True)
    (args.out/"lock_sha.txt").write_text(head+"\n")
    run(args.repo,cfg,args.out,cfgpath=args.config,lockpath=args.lock)

if __name__=="__main__":main()
