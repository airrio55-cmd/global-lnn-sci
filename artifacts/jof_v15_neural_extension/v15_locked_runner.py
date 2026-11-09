"""V15 neural extension runner (DRAFT). Not runnable before an explicit immutable lock.
V14 frozen input, annual validation fits and two-year test fit are reused unchanged.
No model fitting occurs at import or preflight.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, platform, random, subprocess, sys, time
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

def check_lock(repo, cfgpath, lockpath):
    """Refuse training without a separately recorded, clean, inventory-verified Git lock."""
    cfg=json.loads(Path(cfgpath).read_text())
    lock=json.loads(Path(lockpath).read_text()) if Path(lockpath).exists() else {}
    if cfg.get("status")!="LOCKED" or cfg.get("permission_to_train") is not True:
        raise RuntimeError("V15 remains draft: model fitting forbidden")
    if cfg.get("epochs")!=60 or cfg.get("loss")!="CE" or cfg.get("seeds")!=list(SEEDS):
        raise RuntimeError("V15 fixed training settings not approved")
    if cfg.get("ensemble")!="CfC_RAW_0.5 + CfC_LOG_0.5; seed mean after matched-seed pair":
        raise RuntimeError("CfC ensemble configuration differs")
    if set(cfg.get("log_columns",{}))!=set(MARKETS) or any(cfg["log_columns"][m]!=list(LOGCOLS) for m in MARKETS):
        raise RuntimeError("Unapproved LOG inputs")
    head=subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()
    if lock.get("locked_commit")!=head or len(head)!=40:
        raise RuntimeError("Immutable lock commit missing or mismatched")
    if subprocess.check_output(["git","-C",str(repo),"status","--porcelain"],text=True).strip():
        raise RuntimeError("Git checkout not clean")
    inventory=lock.get("sha256",{})
    required=["artifacts/jof_v15_neural_extension/v15_locked_runner.py",
              "artifacts/jof_v15_neural_extension/V15_PROTOCOL_DRAFT.md",
              "artifacts/jof_v15_neural_extension/V15_CONFIG_DRAFT.json"]
    if not all(k in inventory for k in required):
        raise RuntimeError("Locked file inventory incomplete")
    for rel,digest in inventory.items():
        p=(Path(repo)/rel).resolve()
        if not p.is_relative_to(Path(repo).resolve()) or not p.exists() or sha256(p)!=digest:
            raise RuntimeError("Locked file hash invalid: "+rel)
    return cfg,head

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
    arr=frame[list(cols)].to_numpy(float);w=20
    used=np.unique(np.concatenate([np.arange(r["index"]-w,r["index"]) for r in train]))
    scaler=StandardScaler().fit(arr[used])
    def x(rows):
        raw=np.stack([arr[r["index"]-w:r["index"]] for r in rows])
        if not np.isfinite(raw).all():raise RuntimeError("Nonfinite LOG/RAW feature window")
        return scaler.transform(raw.reshape(-1,len(cols))).reshape(len(rows),w,len(cols)).astype("float32")
    return x(train),x(eval_rows)

def fit_predict(name,train,eval_rows,frame,cols,seed,epochs,device):
    import torch
    if not train or not eval_rows:raise RuntimeError("Empty V15 train/evaluation fold")
    y=np.asarray([r["y"] for r in train],dtype=np.int64)
    if np.unique(y).size!=2:raise RuntimeError("One-class training fold")
    xtr,xev=window_tensors(train,eval_rows,frame,cols)
    configure_seed(seed);torch.set_num_threads(2)
    model=build_model(name,xtr.shape[-1]).to(device)
    dataset=torch.utils.data.TensorDataset(torch.from_numpy(xtr),torch.from_numpy(y))
    loader=torch.utils.data.DataLoader(dataset,batch_size=64,shuffle=True,
                            generator=torch.Generator().manual_seed(seed),num_workers=0)
    opt=torch.optim.AdamW(model.parameters(),lr=.005,weight_decay=.0001)
    sch=torch.optim.lr_scheduler.OneCycleLR(opt,max_lr=.005,steps_per_epoch=len(loader),epochs=epochs)
    for _ in range(epochs):
        model.train()
        for bx,by in loader:
            bx,by=bx.to(device),by.to(device)
            opt.zero_grad(set_to_none=True)
            loss=torch.nn.functional.cross_entropy(model(bx),by)
            if not torch.isfinite(loss):raise RuntimeError("Nonfinite loss")
            loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
            opt.step();sch.step()
    model.eval()
    with torch.inference_mode():
        preds=torch.cat([torch.softmax(model(torch.from_numpy(part).to(device)),dim=1)[:,1].cpu()
                      for part in np.array_split(xev,max(1,(len(xev)+255)//256))]).numpy()
    if not np.isfinite(preds).all():raise RuntimeError("Nonfinite predictions")
    return preds

def preflight_dates(v14,repo):
    """Actual labels and AUC are not computed; only eligible feature dates are checked."""
    frozen=pd.read_csv(Path(repo)/"artifacts/jof_v14_preregistered_replication/first_run_20261109/v14_scoring_dates.csv")
    expected={}
    for item in frozen.itertuples(index=False):
        expected.setdefault((item.Market,item.Origin,item.Period),[]).append(str(item.Date))
    checked=0
    for market in MARKETS:
        raw,frame,cols,_=v14.load_market(Path(repo),market)
        if not set(LOGCOLS).issubset(frame.columns):
            raise RuntimeError(market+" LOG columns missing")
        for vy,ty in ORIGINS:
            label="O"+str(vy-2012)
            for period,years in [("Validation",(vy,vy+1)),("Test",(ty,ty+1))]:
                spans=[(vy,vy),(vy+1,vy+1)] if period=="Validation" else [(ty,ty+1)]
                rows=[]
                for start,end in spans:
                    rows+=v14.records(frame,raw,cols,f"{start}-01-01",f"{end}-12-31",preflight=True)
                dates=[p["Date"] for p in rows]
                if dates!=expected[(market,label,period)]:
                    raise RuntimeError(f"{market}/{label}/{period}: V14 scoring date mismatch")
                for row in rows:
                    i=row["index"]
                    if not np.isfinite(frame[list(LOGCOLS)].iloc[i-20:i].to_numpy(float)).all():
                        raise RuntimeError("LOG window not finite")
                checked+=1
    return checked

def run(repo,cfg,out):
    import torch
    v14=v14_module(repo)
    scorefile=Path(repo)/"artifacts/jof_v14_preregistered_replication/first_run_20261109/v14_scoring_dates.csv"
    reference=pd.read_csv(scorefile)
    records=[];fit_log=[]
    for market in MARKETS:
        raw,frame,cols,_=v14.load_market(repo,market)
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
                        p=fit_predict(name,train,ev,frame,colnames,seed,cfg["epochs"],cfg["device"])
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
                                "Y_true":row["y"],"s200":signals["200DMA"],"s60":signals["Momentum60"],
                                "s20":signals["Persistence"]})
                pd.DataFrame(records).to_csv(out/"v15_predictions.partial.csv",index=False)
                pd.DataFrame(fit_log).to_csv(out/"v15_fit_diagnostics.partial.csv",index=False)
    pd.DataFrame(records).to_csv(out/"v15_predictions.csv",index=False,float_format="%.17g")
    pd.DataFrame(fit_log).to_csv(out/"v15_fit_diagnostics.csv",index=False)
    # Deliberately leave V14-equivalent statistical test to reviewed analysis script
    (out/"FIT_COMPLETE_EVALUATION_PENDING.txt").write_text("Neural predictions complete. Do not interpret before reviewed V15 analysis.\\n")

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
    cfg,head=check_lock(args.repo,args.config,args.lock)
    if args.out.exists():raise RuntimeError("Refusing to overwrite a previous result directory")
    args.out.mkdir(parents=True)
    (args.out/"lock_sha.txt").write_text(head+"\\n")
    run(args.repo,cfg,args.out)

if __name__=="__main__":main()
