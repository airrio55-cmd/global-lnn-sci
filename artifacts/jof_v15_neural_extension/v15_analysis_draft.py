"""V15 fixed hypothesis analysis, separate from training. Never used to select models.
Run only after a completed, immutable V15 prediction file is available.
"""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from v15_common import reference_dates, sha
from v15_locked_runner import check_lock

ARCH=("LSTM","LTC_RAW","CfC_RAW")
MODELS=ARCH+("CfC_LOG","CfC_ENSEMBLE")
SEEDS=(42,52,62)
MARKETS=("SP500","NASDAQ100","NIKKEI225","EUROSTOXX50","KOSPI200")

def v14_reference(repo):
    spec=importlib.util.spec_from_file_location("v14_ref",Path(repo)/"artifacts/jof_v14_preregistered_replication/run_v14_locked.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def corr(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float)
    if len(a)<3 or np.std(a)==0 or np.std(b)==0:return np.nan
    return float(np.corrcoef(a,b)[0,1])

def effect(y,s):
    y=np.asarray(y,int);s=np.asarray(s,int)
    if (s==0).sum()<20 or (s==1).sum()<20:return np.nan
    return float(y[s==1].mean()-y[s==0].mean())

def validate_predictions(repo,inp):
    """Structural validation only: deliberately no AUC calculation."""
    key=["Market","Origin","Period","Date","Model","Seed"]
    if not set(key+["Probability","Y_true","s200","s60","s20"]).issubset(inp):raise ValueError("Missing prediction columns")
    if inp[key].isna().any().any() or inp.duplicated(key).any():raise ValueError("Duplicate/null prediction keys")
    if set(inp.Market)!=set(MARKETS) or set(inp.Model)!=set(MODELS) or set(inp.Seed)!=set(SEEDS):raise ValueError("Incomplete fixed markets/models/seeds")
    if not np.isfinite(inp.Probability).all() or not inp.Probability.between(0,1).all():raise ValueError("Invalid probabilities")
    for col in ["Y_true","s200","s60","s20"]:
        if not inp[col].isin([0,1]).all():raise ValueError("Invalid binary field: "+col)
        if inp.groupby(["Market","Origin","Period","Date"])[col].nunique().ne(1).any():raise ValueError("Inconsistent label/signal: "+col)
    ref=reference_dates(repo)
    refkeys=list(ref[["Market","Origin","Period","Date"]].itertuples(index=False,name=None))
    required=set(refkeys)
    for (model,seed),g in inp.groupby(["Model","Seed"]):
        actual=set(g[["Market","Origin","Period","Date"]].itertuples(index=False,name=None))
        if actual!=required or len(g)!=len(ref):raise ValueError("Missing/extra V14 dates in model-seed series")
    pivot=inp.pivot(index=["Market","Origin","Period","Date","Seed"],columns="Model",values="Probability")
    np.testing.assert_allclose(pivot.CfC_ENSEMBLE,.5*pivot.CfC_RAW+.5*pivot.CfC_LOG,atol=1e-14,rtol=0)
    return True

def analysis(repo,source,out,*,config=None,lock=None):
    if config is None or lock is None:raise RuntimeError("DRAFT: analysis/AUC disabled without separate authorization and immutable lock")
    cfg,_=check_lock(repo,config,lock)
    if cfg.get("permission_to_analyze") is not True:raise RuntimeError("AUC/analysis permission not enabled")
    completion=json.loads((Path(source).parent/"completion_manifest.json").read_text())
    if completion.get("fit_count")!=1080 or completion.get("prediction_sha256")!=sha(source):raise ValueError("Predictions not a complete frozen1080fit run")
    if Path(out).resolve().is_relative_to(Path(repo).resolve()):raise ValueError("Write future analysis outside the protected checkout")
    if Path(out).exists():raise ValueError("Refusing to overwrite previous analysis")
    inp=pd.read_csv(source);validate_predictions(repo,inp)
    group=["Market","Origin","Period","Date","Model"]
    if inp.groupby(group).Seed.nunique().ne(3).any():
        raise ValueError("Missing seed probabilities")
    for k in ["Y_true","s200","s60","s20"]:
        if inp.groupby(["Market","Origin","Period","Date"])[k].nunique().gt(1).any():
            raise ValueError("Inconsistent signal/label: "+k)
    avg=inp.groupby(group,sort=False,as_index=False).agg(
        Probability=("Probability","mean"),Y_true=("Y_true","first"),
        s200=("s200","first"),s60=("s60","first"),s20=("s20","first"))
    universe=avg.groupby(["Market","Origin","Period","Date"]).Model.nunique()
    if universe.ne(len(MODELS)).any():raise ValueError("Missing model/dates")
    rows=[]
    for (m,o),u in avg.groupby(["Market","Origin"]):
        val=u[u.Period=="Validation"];test=u[u.Period=="Test"]
        r={"Market":m,"Origin":o,"NVal":len(val)//len(MODELS),"NTest":len(test)//len(MODELS)}
        for model in MODELS:
            av=val[val.Model==model];te=test[test.Model==model]
            if av.Y_true.nunique()!=2 or te.Y_true.nunique()!=2:
                raise ValueError("Undefined AUC")
            a=roc_auc_score(av.Y_true,av.Probability);b=roc_auc_score(te.Y_true,te.Probability)
            r[f"{model}_ValAUC"]=float(a)
            r[f"{model}_TestAUC"]=float(b)
            r[f"{model}_DeltaAUC"]=float(b-a)
            for sig,col in [("200DMA","s200"),("Momentum60","s60"),("Persistence","s20")]:
                r[f"{model}_{sig}_rVal"]=corr(av.Probability,av[col])
                r[f"{model}_{sig}_rTest"]=corr(te.Probability,te[col])
        reference=val[val.Model==ARCH[0]]
        forecast=test[test.Model==ARCH[0]]
        for sig,col in [("200DMA","s200"),("Momentum60","s60"),("Persistence","s20")]:
            r[f"{sig}_Shift"]=effect(forecast.Y_true,forecast[col])-effect(reference.Y_true,reference[col])
        r["MeanValAUC"]=float(np.mean([r[f"{m}_ValAUC"] for m in ARCH]))
        r["MeanTestAUC"]=float(np.mean([r[f"{m}_TestAUC"] for m in ARCH]))
        r["MeanDeltaAUC"]=float(np.mean([r[f"{m}_DeltaAUC"] for m in ARCH]))
        align=[r[f"{m}_200DMA_rTest"] for m in ARCH]
        r["rTest200_Mean"]=float(np.mean(align)) if np.isfinite(align).all() else np.nan
        r["H1b_T"]=r["200DMA_Shift"]*r["rTest200_Mean"]
        rows.append(r)
    df=pd.DataFrame(rows).sort_values(["Market","Origin"]).reset_index(drop=True)
    if len(df)!=30:raise ValueError("Expected 30 market-origin units")
    v14=v14_reference(repo)
    result={"analysis":"V15 neural extension; exploratory historical pre-specification, not prospective",
            "H1_mean_models":list(ARCH),"H3_models":list(ARCH),
            "model_delta_summary":{m:{"mean":float(df[f"{m}_DeltaAUC"].mean()),
                                     "median":float(df[f"{m}_DeltaAUC"].median())} for m in MODELS}}
    hyp=[("H1","200DMA_Shift","negative"),("H1b","H1b_T","positive"),
         ("H2_Momentum60","Momentum60_Shift","negative"),
         ("H2_Persistence","Persistence_Shift","negative")]
    for name,pred,direction in hyp:
        result[name]={**v14.perm_p(df,pred,direction,20261109),
                      "circular":v14.rotate_p(df,pred,direction),
                      "diagnostics":v14.diagnostics(df,pred)}
    ordered=sorted((result[k]["nominal_p"],k) for k in ["H1b","H2_Momentum60","H2_Persistence"]
                   if result[k]["nominal_p"] is not None)
    for k in ["H1b","H2_Momentum60","H2_Persistence"]:result[k]["Holm3"]=None
    running=0
    for i,(p,k) in enumerate(ordered):
        running=max(running,(3-i)*p);result[k]["Holm3"]=min(1.,running)
    hv=[df[f"{m}_Persistence_rVal"].to_numpy(float) for m in ARCH]
    a=np.concatenate(hv);valid=a[np.isfinite(a)]
    result["H3"]={"negative":int(np.sum(valid<0)),"evaluable":len(valid),"planned":90,
                  "no_independent_unit_p":True}
    negative=int(np.sum(df["rTest200_Mean"].to_numpy(float)<0))
    result["H1_alignment_prerequisite"]={"negative":negative,"planned":30,"evaluable":int(df["rTest200_Mean"].notna().sum()),"met":negative>=16}
    r=result["H1"];rho=r["rho"];p=r["nominal_p"]
    if rho is None: label="not evaluable"
    elif rho>=0:label="Not supported in direction"
    elif p is not None and p<.05:label="Nominally supported under a non-exact permutation diagnostic"
    else:label="Directionally consistent, nominally non-significant"
    if not result["H1_alignment_prerequisite"]["met"]:label="Not interpretable as H1 support: alignment prerequisite not met"
    if r["N"]!=30:label="not fully evaluable under locked 30-unit design; "+label
    result["H1_label"]=label
    result["H3_CfC_ENSEMBLE"]={"negative":int((df["CfC_ENSEMBLE_Persistence_rVal"]<0).sum()),"evaluable":int(df["CfC_ENSEMBLE_Persistence_rVal"].notna().sum()),"planned":30,"descriptive_only":True}
    # Secondary: evaluate individual seed H1 directions; descriptive, no seed pseudo-replication.
    seed_rows=[]
    for seed,sg in inp.groupby("Seed"):
        for (m,o),z in sg.groupby(["Market","Origin"]):
            vs=z[z.Period=="Validation"];ts=z[z.Period=="Test"];d=[];details={}
            for model in MODELS:
                va=vs[vs.Model==model];te=ts[ts.Model==model]
                av=roc_auc_score(va.Y_true,va.Probability);at=roc_auc_score(te.Y_true,te.Probability)
                details.update({f"{model}_ValAUC":float(av),f"{model}_TestAUC":float(at),f"{model}_DeltaAUC":float(at-av)})
                if model in ARCH:d.append(at-av)
            reference=df[(df.Market==m)&(df.Origin==o)].iloc[0]
            seed_rows.append({"Seed":int(seed),"Market":m,"Origin":o,
                              "MeanDeltaAUC":float(np.mean(d)),"200DMA_Shift":reference["200DMA_Shift"],**details})
    sdf=pd.DataFrame(seed_rows)
    result["seed_H1_direction"]={}
    for seed,z in sdf.groupby("Seed"):
        good=z.dropna(subset=["200DMA_Shift","MeanDeltaAUC"])
        result["seed_H1_direction"][str(seed)]={"rho":v14.spearman(good["200DMA_Shift"],good["MeanDeltaAUC"]),
                                                 "n":len(good)}
    # Compare V14 only as descriptive period-matched non-neural benchmark, not new confirmatory claim.
    baseline=pd.read_csv(Path(repo)/"artifacts/jof_v14_preregistered_replication/first_run_20261109/v14_unit_level.csv")
    baseline_cols=["Market","Origin","MeanDeltaAUC"]+[f"{m}_{metric}" for m in ["LogisticRegression","LightGBM"] for metric in ["ValAUC","TestAUC","DeltaAUC"]]
    if len(baseline)!=30 or baseline.duplicated(["Market","Origin"]).any():raise ValueError("Incomplete V14 comparison units")
    comparison=df.merge(baseline[baseline_cols],on=["Market","Origin"],how="left",validate="one_to_one",
                         suffixes=("_Neural","_NonNeural"))
    if comparison.MeanDeltaAUC_NonNeural.isna().any():raise ValueError("Missing V14 baseline")
    for metric in ["ValAUC","TestAUC","DeltaAUC"]:
        comparison[f"CfC_Ensemble_minus_RAW_{metric}"]=comparison[f"CfC_ENSEMBLE_{metric}"]-comparison[f"CfC_RAW_{metric}"]
    for metric in ["ValAUC","TestAUC"]:
        comparison[f"Mean{metric}_NonNeural"]=(comparison[f"LogisticRegression_{metric}"]+comparison[f"LightGBM_{metric}"])/2
        comparison[f"{metric}_Neural_minus_NonNeural"]=comparison[f"Mean{metric}"]-comparison[f"Mean{metric}_NonNeural"]
    comparison["DeltaDifference"]=comparison.MeanDeltaAUC_Neural-comparison.MeanDeltaAUC_NonNeural
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    df.to_csv(out/"v15_unit_level.csv",index=False,float_format="%.17g")
    sdf.to_csv(out/"v15_seed_sensitivity.csv",index=False,float_format="%.17g")
    comparison.to_csv(out/"v15_model_comparison.csv",index=False,float_format="%.17g")
    (out/"v15_results.json").write_text(json.dumps(v14.clean(result),indent=2,allow_nan=False)+"\n")
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True,type=Path);ap.add_argument("--predictions",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--config",required=True,type=Path);ap.add_argument("--lock",required=True,type=Path)
    ap.add_argument("--acknowledge-analysis",action="store_true")
    args=ap.parse_args()
    if not args.acknowledge_analysis:raise RuntimeError("DRAFT: explicit analysis authorization required")
    if not (args.predictions.exists() and args.predictions.stat().st_size>0):
        raise RuntimeError("No complete frozen predictions")
    analysis(args.repo,args.predictions,args.out,config=args.config,lock=args.lock)

if __name__=="__main__":main()
