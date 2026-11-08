#!/usr/bin/env python3
"""V14 locked historical rolling-origin replication. Do not alter after lock.
Usage: python run_v14_locked.py --repo /path/to/global-lnn-sci --out /path/to/results
Pre-lock price/feature-group-only check: add --preflight. No fit/outcome computation in preflight.
"""
import argparse, hashlib, itertools, json, platform, sys, traceback
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, rankdata
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
import sklearn, lightgbm

MARKETS={"SP500":"sp500_rerun","NASDAQ100":"nasdaq100","NIKKEI225":"nikkei225",
         "EUROSTOXX50":"eurostoxx50","KOSPI200":"kospi200"}
SIGNALS=["Persistence","200DMA","Momentum60"]
ORIGINS=[(2013+i,2015+i) for i in range(6)]
SEED=20261109; H=20; W=20; MIN_GROUP=20; REPS=10000

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def valid_year(date,year):
    return date.year==year
def spearman(x,y):
    x=np.asarray(x,float);y=np.asarray(y,float)
    if len(x)<3 or np.std(x)==0 or np.std(y)==0: return float("nan")
    return float(spearmanr(x,y).statistic)
def corr(x,y):
    if len(x)<3 or np.std(x)==0 or np.std(y)==0:return float("nan")
    return float(np.corrcoef(x,y)[0,1])
def auc(y,p):
    y=np.asarray(y,int)
    return float(roc_auc_score(y,p)) if len(np.unique(y))==2 else float("nan")
def coeff(y,s):
    a=np.asarray(y,int);b=np.asarray(s,int)
    if sum(b==0)<MIN_GROUP or sum(b==1)<MIN_GROUP:return float("nan")
    return float(np.mean(a[b==1])-np.mean(a[b==0]))
def model(name):
    if name=="LogisticRegression":
        return LogisticRegression(penalty="l2",solver="lbfgs",C=1.0,max_iter=5000,
               fit_intercept=True,tol=1e-4,class_weight=None,random_state=42)
    return LGBMClassifier(objective="binary",n_estimators=300,learning_rate=.03,
        num_leaves=31,max_depth=-1,min_child_samples=20,subsample=1.,
        colsample_bytree=1.,reg_alpha=0.,reg_lambda=0.,class_weight=None,
        verbosity=-1,random_state=42,data_random_seed=42,
        feature_fraction_seed=42,bagging_seed=42,drop_seed=42,extra_seed=42,
        deterministic=True,force_col_wise=True,n_jobs=2)
def records(df,raw,features,first,last,preflight=False):
    dates=raw.index;C=raw["Close"].to_numpy(float);F=df[features].to_numpy(float)
    if not dates.equals(df.index):raise RuntimeError("Feature/index mismatch")
    start=int(dates.searchsorted(pd.Timestamp(first)));end=int(dates.searchsorted(pd.Timestamp(last),side="right"))
    out=[]
    for i in range(max(start,201),min(end,len(dates)-H)):
        if dates[i+H]>pd.Timestamp(last):continue
        x=F[i-W:i]
        if x.shape!=(W,len(features)) or not np.isfinite(x).all():continue
        prev=i-1;signal={
            "Persistence":int(C[prev]>C[prev-20]),
            "200DMA":int(C[prev]>np.mean(C[prev-199:prev+1])),
            "Momentum60":int(C[prev]>C[prev-60])}
        rec={"Date":str(dates[i].date()),"index":i,"signals":signal}
        if not preflight:rec["y"]=int(C[i+H]>C[i])
        out.append(rec)
    return out
def load_market(root,market):
    folder=MARKETS[market]
    rawpath=root/"artifacts"/folder/"market_input.csv"
    featpath=root/"artifacts/jof_phase1_benchmark_expansion/frozen_features"/(market+".csv")
    manifest=root/"artifacts/jof_phase1_benchmark_expansion/data_manifest.json"
    raw=pd.read_csv(rawpath,index_col=0,parse_dates=True,float_precision="round_trip")
    feat=pd.read_csv(featpath,index_col=0,parse_dates=True,float_precision="round_trip")
    mm=json.loads(manifest.read_text())["markets"]
    names=next(x["Feature_names"] for x in mm if x["Market"]==market)
    if not raw.index.equals(feat.index) or raw.index.has_duplicates:raise RuntimeError("Raw/feature index differs")
    return raw,feat,names,{str(p.relative_to(root)):sha(p) for p in (rawpath,featpath,manifest)}
def fit_predict(train,eval_,df,features,name):
    if not train or not eval_:raise ValueError("empty train/evaluation fold")
    Y=np.array([x["y"] for x in train],int)
    if len(np.unique(Y))!=2:raise ValueError("one-class training fold")
    features_array=df[features].to_numpy(float)
    train_indices=np.array([x["index"] for x in train],int)
    # Original market-specific feature scaler: same feature mean/scale shared across lags.
    # Only feature rows present in eligible training windows are included.
    used=np.unique(np.concatenate([np.arange(i-W,i) for i in train_indices]))
    scaler=StandardScaler().fit(features_array[used])
    def X(rows):
        data=np.stack([features_array[r["index"]-W:r["index"]] for r in rows])
        return scaler.transform(data.reshape(-1,len(features))).reshape(len(rows),W*len(features))
    estimator=model(name);estimator.fit(X(train),Y)
    return estimator.predict_proba(X(eval_))[:,1]
def period_scoring(raw,feat,features,origin):
    vy,ty=origin;startyear=raw.index.min().year
    val_preds={name:[] for name in ("LogisticRegression","LightGBM")}
    val=[]
    for year in (vy,vy+1):
        tr=records(feat,raw,features,f"{startyear}-01-01",f"{year-1}-12-31")
        ev=records(feat,raw,features,f"{year}-01-01",f"{year}-12-31")
        for name in val_preds:val_preds[name].extend(fit_predict(tr,ev,feat,features,name))
        val.extend(ev)
    training=records(feat,raw,features,f"{startyear}-01-01",f"{ty-1}-12-31")
    test=records(feat,raw,features,f"{ty}-01-01",f"{ty+1}-12-31")
    test_preds={name:fit_predict(training,test,feat,features,name) for name in val_preds}
    return val,test,{k:np.asarray(v) for k,v in val_preds.items()},test_preds
def single_unit(market,origin,raw,feat,features):
    val,test,vprob,tprob=period_scoring(raw,feat,features,origin)
    if not val or not test:raise RuntimeError("Empty scoring window")
    v_y=np.array([x["y"] for x in val]);t_y=np.array([x["y"] for x in test])
    record={"Market":market,"Origin":"O"+str(origin[0]-2012),
            "ValStart":val[0]["Date"],"ValEnd":val[-1]["Date"],
            "TestStart":test[0]["Date"],"TestEnd":test[-1]["Date"],
            "NVal":len(val),"NTest":len(test)}
    deltas=[]
    for m in ("LogisticRegression","LightGBM"):
        av=auc(v_y,vprob[m]);at=auc(t_y,tprob[m])
        record[m+"_ValAUC"]=av;record[m+"_TestAUC"]=at
        record[m+"_DeltaAUC"]=at-av
        deltas.append(at-av)
    record["MeanDeltaAUC"]=float(np.mean(deltas)) if all(np.isfinite(deltas)) else float("nan")
    for sig in SIGNALS:
        vs=np.array([x["signals"][sig] for x in val]);ts=np.array([x["signals"][sig] for x in test])
        record[sig+"_ValN0"]=int(sum(vs==0));record[sig+"_ValN1"]=int(sum(vs==1))
        record[sig+"_TestN0"]=int(sum(ts==0));record[sig+"_TestN1"]=int(sum(ts==1))
        a=coeff(v_y,vs);b=coeff(t_y,ts)
        record[sig+"_Eval"]=a;record[sig+"_Etest"]=b
        record[sig+"_Shift"]=b-a
        for m in ("LogisticRegression","LightGBM"):
            record[m+"_"+sig+"_rVal"]=corr(vprob[m],vs)
            record[m+"_"+sig+"_rTest"]=corr(tprob[m],ts)
    a=[record[m+"_200DMA_rTest"] for m in ("LogisticRegression","LightGBM")]
    record["rTest200_Mean"]=float(np.mean(a)) if all(np.isfinite(a)) else float("nan")
    record["H1b_T"]=record["200DMA_Shift"]*record["rTest200_Mean"]
    return record,val,test
def finite_rows(df,pred):
    return df[np.isfinite(df[pred].to_numpy(float)) & np.isfinite(df.MeanDeltaAUC.to_numpy(float))].copy()
def stat(df,pred):
    return spearman(df[pred],df["MeanDeltaAUC"])
def perm_p(df,pred,direction,seed):
    d=finite_rows(df,pred);obs=stat(d,pred)
    if not np.isfinite(obs):return {"N":len(d),"rho":None,"nominal_p":None}
    rng=np.random.default_rng(seed);base=d[pred].to_numpy(float)
    partitions=[np.flatnonzero((d.Market==market).to_numpy()) for market in MARKETS]
    hit=0
    for _ in range(REPS):
        x=base.copy()
        for idx in partitions:
            if len(idx)>1:x[idx]=rng.permutation(base[idx])
        z=spearman(x,d.MeanDeltaAUC)
        hit+=int(z<=obs if direction=="negative" else z>=obs)
    return {"N":len(d),"rho":obs,"nominal_p":(1+hit)/(1+REPS)}
def rotate_p(df,pred,direction):
    d=finite_rows(df,pred);obs=stat(d,pred)
    if not np.isfinite(obs):return {"total":0,"tail_fraction":None}
    base=d[pred].to_numpy(float)
    partitions=[np.flatnonzero((d.Market==m).to_numpy()) for m in MARKETS]
    counts=[max(1,len(ix)) for ix in partitions];hits=0;total=0
    for shifts in itertools.product(*[range(n) for n in counts]):
        arr=base.copy()
        for ix,k in zip(partitions,shifts):
            if len(ix):arr[ix]=np.roll(base[ix],k)
        rho=spearman(arr,d.MeanDeltaAUC)
        hits+=int(rho<=obs if direction=="negative" else rho>=obs);total+=1
    synced=[]
    for k in range(6):
        arr=base.copy()
        for ix in partitions:
            if len(ix):arr[ix]=np.roll(base[ix],k%len(ix))
        synced.append(spearman(arr,d.MeanDeltaAUC))
    return {"total":total,"tail_fraction":hits/total,"synchronized_n":6,
            "synchronized_tail_fraction":sum((v<=obs if direction=="negative" else v>=obs) for v in synced)/6}
def diagnostics(df,pred):
    d=finite_rows(df,pred)
    x=d[pred].to_numpy(float);y=d.MeanDeltaAUC.to_numpy(float)
    codes=pd.get_dummies(d.Market).reindex(columns=list(MARKETS)[1:],fill_value=0).to_numpy(float)
    X=np.column_stack([np.ones(len(x)),x,codes])
    coef=float(np.linalg.lstsq(X,y,rcond=None)[0][1]) if len(x)>X.shape[1] else None
    loo={m:stat(d[d.Market!=m],pred) for m in MARKETS}
    within={m:stat(d[d.Market==m],pred) for m in MARKETS}
    # Center ranks within market, then pool within-market rank residuals.
    rx=np.zeros(len(d));ry=np.zeros(len(d))
    for m in MARKETS:
        ix=np.flatnonzero((d.Market==m).to_numpy())
        if len(ix)>1:
            rx[ix]=rankdata(x[ix])-np.mean(rankdata(x[ix]))
            ry[ix]=rankdata(y[ix])-np.mean(rankdata(y[ix]))
    centered=corr(rx,ry)
    return {"market_fixed_effect_slope":coef,"leave_one_market_out":loo,
            "within_market_rho":within,"centered_rank_corr":centered}
def clean(obj):
    if isinstance(obj,dict):return {str(k):clean(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [clean(v) for v in obj]
    if isinstance(obj,(np.integer,)):return int(obj)
    if isinstance(obj,(np.floating,float)):
        return float(obj) if np.isfinite(obj) else None
    return obj
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--preflight",action="store_true")
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    expected=[];data={};hashes={}
    for market in MARKETS:
        raw,feat,features,h=load_market(a.repo,market)
        hashes.update(h);data[market]=(raw,feat,features)
        for vi,ti in ORIGINS:
            for kind,start,end in (("Validation",vi,vi+1),("Test",ti,ti+1)):
                rows=records(feat,raw,features,f"{start}-01-01",f"{end}-12-31",preflight=True)
                sig=np.array([x["signals"]["200DMA"] for x in rows])
                expected.append({"Market":market,"Origin":"O"+str(vi-2012),"Period":kind,
                  "EligiblePriceAndFeatureN":len(rows),"DMA0":int(sum(sig==0)),"DMA1":int(sum(sig==1))})
    pd.DataFrame(expected).to_csv(a.out/"v14_preflight_signal_counts.csv",index=False)
    meta={"input_sha256":hashes,"python":platform.python_version(),
      "numpy":np.__version__,"pandas":pd.__version__,"sklearn":sklearn.__version__,
      "lightgbm":lightgbm.__version__,"min_group":MIN_GROUP}
    (a.out/"v14_input_inventory.json").write_text(json.dumps(meta,indent=2))
    if a.preflight:
        print("PREFLIGHT ONLY: price/feature eligibility and 200DMA group counts; no target labels or model fitting.")
        return
    rows=[];errors=[];pred_date_rows=[]
    for m,(raw,feat,features) in data.items():
        for origin in ORIGINS:
            try:
                unit,val,test=single_unit(m,origin,raw,feat,features)
                rows.append(unit)
                for period,points in (("Validation",val),("Test",test)):
                    for item in points:pred_date_rows.append({"Market":m,"Origin":unit["Origin"],
                            "Period":period,"Date":item["Date"]})
            except Exception as e:
                errors.append({"Market":m,"Origin":origin,"type":type(e).__name__,"reason":str(e)})
                rows.append({"Market":m,"Origin":"O"+str(origin[0]-2012),"MeanDeltaAUC":float("nan")})
    df=pd.DataFrame(rows);df.to_csv(a.out/"v14_unit_level.csv",index=False)
    pd.DataFrame(pred_date_rows).to_csv(a.out/"v14_scoring_dates.csv",index=False)
    result={"errors":errors,"expected_units":30,"successful_units":30-len(errors)}
    for name,pred,direction in (("H1","200DMA_Shift","negative"),
         ("H1b","H1b_T","positive"),("H2_Momentum60","Momentum60_Shift","negative"),
         ("H2_Persistence","Persistence_Shift","negative")):
        test=perm_p(df,pred,direction,SEED)
        result[name]={**test,"circular":rotate_p(df,pred,direction),
                     "diagnostics":diagnostics(df,pred)}
    # Holm multiplicity family includes only H1b and two H2 hypotheses.
    labels=["H1b","H2_Momentum60","H2_Persistence"]
    vals=sorted([(result[k]["nominal_p"],k) for k in labels
                 if result[k]["nominal_p"] is not None])
    adjust=0
    for i,(pv,k) in enumerate(vals):
        adjust=max(adjust,(len(labels)-i)*pv)
        result[k]["Holm3"]=min(1.,adjust)
    h3=[(m,r[m+"_Persistence_rVal"]) for r in rows for m in ("LogisticRegression","LightGBM")
        if m+"_Persistence_rVal" in r and np.isfinite(r[m+"_Persistence_rVal"])]
    result["H3"]={"negative":sum(r<0 for _,r in h3),"evaluated":len(h3),"planned":60}
    good=finite_rows(df,"200DMA_Shift")
    neg=sum(float(r["rTest200_Mean"])<0 for _,r in good.iterrows()
            if "rTest200_Mean" in r and np.isfinite(r["rTest200_Mean"]))
    result["H1_alignment_prerequisite"]={"negative":neg,"evaluable":len(good),
        "planned":30,"met":neg>=16,"threshold":16}
    h1=result["H1"];rho=h1["rho"];pv=h1["nominal_p"]
    if rho is None:label="not evaluable"
    elif rho>=0:label="Not supported in direction"
    elif pv is not None and pv<.05:label="Nominally supported under a non-exact permutation diagnostic"
    else:label="Directionally consistent, nominally non-significant"
    result["H1_label"]=label;result["H1_complete_case_note"]=f'evaluated on {h1["N"]} of 30 units'
    result["software_and_hashes"]=meta
    (a.out/"v14_results.json").write_text(json.dumps(clean(result),indent=2)+"\n")
    (a.out/"v14_execution.log").write_text(json.dumps(clean({"errors":errors,
                  "units":30,"no_test_2022_2025":True,"group_threshold":20}),indent=2)+"\n")
    print(json.dumps(clean({"H1":result["H1"],"label":label,"H3":result["H3"]}),indent=2))
if __name__=="__main__":
    main()
