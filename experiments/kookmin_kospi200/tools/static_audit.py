from pathlib import Path
import json,glob,hashlib,csv,ast,difflib,shutil
import pandas as pd,numpy as np
R=Path(__file__).resolve().parents[1]; E=R/'evidence';E.mkdir(parents=True,exist_ok=True)
manifest=json.loads((E/'input_manifest.json').read_text())
for item in manifest:
 p=R/'originals'/item['filename']
 if not p.is_file(): raise FileNotFoundError('Required original missing: '+str(p))
 if p.stat().st_size!=item['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
  raise ValueError('Original SHA-256/size mismatch: '+str(p))
ns={}
for f in glob.glob(str(R/'originals'/'*.ipynb')):
 tag='single' if '단일' in f else ('10seed' if '10개' in f else '5seed');ns[tag]=json.load(open(f))
for tag,n in ns.items():
 lines=[]
 for i,c in enumerate(n['cells'],1):
  lines.append(f'\n## Cell {i}; id={c.get("id","")}; {c["cell_type"]}\n')
  lines.extend(f'{j:04}: {s}\n' for j,s in enumerate(''.join(c['source']).splitlines(),1))
 (E/(tag+'_cells.txt')).write_text(''.join(lines))
rows=[]
for i in range(18):
 src={t:''.join(ns[t]['cells'][i]['source']) for t in ns}
 row={'cell_1based':i+1,'id':ns['single']['cells'][i].get('id',''),'type':ns['single']['cells'][i]['cell_type']}
 for t,s in src.items():row[t+'_sha256']=hashlib.sha256(s.encode()).hexdigest()
 row['single_equals_5']=src['single']==src['5seed'];row['5_equals_10']=src['5seed']==src['10seed'];rows.append(row)
with (E/'cell_comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
for a,b in [('single','5seed'),('5seed','10seed'),('single','10seed')]:
 def txt(t):return ''.join(f'\n### Cell {i}\n'+''.join(c['source'])+'\n' for i,c in enumerate(ns[t]['cells'],1)).splitlines(True)
 (E/f'{a}_vs_{b}.diff').write_text(''.join(difflib.unified_diff(txt(a),txt(b),fromfile=a,tofile=b)))
files={Path(p).name:p for p in glob.glob(str(R/'originals'/'*.csv'))}; data={};summary=[]
for name,p in files.items():
 d=pd.read_csv(p);col='Date' if 'Date' in d else '날짜'; dates=pd.to_datetime(d[col],errors='coerce');data[name]=d.assign(**{col:dates}).set_index(col).sort_index()
 summary.append({'file':name,'rows':len(d),'columns':list(d),'date_min':str(dates.min().date()),'date_max':str(dates.max().date()),'date_duplicates':int(dates.duplicated().sum()),'unparseable_dates':int(dates.isna().sum()),'sorted_ascending':bool(dates.is_monotonic_increasing),'missing':{k:int(v) for k,v in d.isna().sum().items()},'zeros':{k:int(v) for k,v in d.select_dtypes(include='number').eq(0).sum().items()},'nonfinite_numeric':{k:int(v) for k,v in (~np.isfinite(d.select_dtypes(include='number'))).sum().items()},'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest(),'upstream_provider':'not documented in attachments','available_at':'not provided'})
(E/'data_inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
k,f,n,s=[data[x] for x in ['KOSPI_200.csv','Foreigner_Net.csv','Nasdaq.csv','SOX.csv']]
j=k[['종가']].rename(columns={'종가':'Close'}).join([f[['외국인']].rename(columns={'외국인':'Foreign_Net'}),n[['Close']].rename(columns={'Close':'Nasdaq'}),s[['Close']].rename(columns={'Close':'SOX'})]);a=j.ffill();b=a.bfill();fw=b.Close.shift(-20)
b['Log_Ret']=np.log(b.Close/b.Close.shift());b['Vol_Regime']=b.Log_Ret.rolling(40).std();b['Disparity']=b.Close/b.Close.rolling(20).mean()-1;b['Target']=(fw>b.Close).astype(int);b=b.dropna();tr,va=int(len(b)*.6),int(len(b)*.2)
res={'method':'independent pandas data-only reproduction; no notebook cells executed','join_missing':j.isna().sum().to_dict(),'ffill_filled':(j.isna()&a.notna()).sum().to_dict(),'bfill_filled':(a.isna()&a.bfill().notna()).sum().to_dict(),'US_dates_lost_before_ffill':len(n.index.difference(k.index)),'retained_rows':len(b),'unresolved_tail_labels':20,'unresolved_tail_start':str(b.index[-20].date()),'tail_zero_labels':int(b.Target.tail(20).eq(0).sum()),'splits':[]}
for name,d in [('train',b.iloc[:tr]),('validation',b.iloc[tr:tr+va]),('test',b.iloc[tr+va:])]:res['splits'].append({'name':name,'rows':len(d),'start':str(d.index.min().date()),'end':str(d.index.max().date()),'scored_rows':len(d)-20,'scored_start':str(d.index[20].date())})
res['boundary_checks']=[{'next_partition_start':str(b.index[c].date()),'previous_last_label_end':str(b.index[c-1+20].date()),'next_first_scored_label_start':str(b.index[c+20].date()),'purge_rows_under_strict_partition_cutoff':20} for c in [tr,tr+va]]
p=data['processed_regression_data.csv'];res['processed_checks']={'used_by_notebooks':False,'close_max_abs_error':float((p.KOSPI200-k['종가'].reindex(p.index)).abs().max()),'target_ret20_max_abs_error':float((p.Target_Ret20-(k['종가'].shift(-20)/k['종가']-1).reindex(p.index)).abs().max()),'sox_lag1_max_abs_error':float((p.SOX_Lag1-p.SOX.shift()).abs().max())}
(E/'data_only_checks.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
# Small data-only regressions. No imports from any notebook and no fit calls.
checks=[]
def check(name,condition):
 assert condition,name
 checks.append({'test':name,'status':'PASS'})
check('original_target_tail_is_twenty_false_zeros',b.Target.tail(20).eq(0).all())
future=k['종가'].shift(-20); fixed=pd.Series(pd.NA,index=k.index,dtype='Int64'); known=future.notna()&k['종가'].notna();fixed.loc[known]=(future.loc[known]>k['종가'].loc[known]).astype(int)
check('proposed_nullable_target_keeps_twenty_unknown',fixed.tail(20).isna().all() and fixed.notna().sum()==len(k)-20)
check('known_target_values_preserved',np.array_equal(fixed[known].astype(int).to_numpy(),(future[known]>k['종가'][known]).astype(int).to_numpy()))
end=pd.Series(k.index,index=k.index).shift(-20);cut=k.index[200];eligible=end.notna()&(end<cut)
check('proposed_purge_keeps_all_label_ends_before_cutoff',bool((end[eligible]<cut).all()) and int(eligible.sum())==180)
# Future sentinel probes for backward vs forward fill.
x=pd.Series([np.nan,2.,3.]);z=pd.Series([np.nan,200.,3.]);check('bfill_future_sentinel_changes_past',x.bfill().iloc[0]!=z.bfill().iloc[0]);check('ffill_does_not_pull_future_into_leading_gap',pd.isna(x.ffill().iloc[0]) and pd.isna(z.ffill().iloc[0]))
# Replication is not new information.
y=np.array([1,0,1]);pa=np.array([1,0,0]);pb=np.array([0,0,1]);discord=lambda a,b:int(np.sum(a!=b))
check('seed_pooling_repeats_discordances_without_new_dates',discord(np.tile(pa,5),np.tile(pb,5))==5*discord(pa,pb))
(E/'static_tests.json').write_text(json.dumps({'scope':'data-only synthetic/reproduction tests, no learning or HMM fitting','checks':checks},ensure_ascii=False,indent=2))
print(json.dumps({'files':len(summary),'checks':checks,'splits':res['splits']},ensure_ascii=False,indent=2))
