"""Data-only STEP2 diagnostics. Observed dates are NOT a certified KRX calendar."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from kospi200.data import cutoff,local_features,BlockedError,Calendar,labels_on_calendar
from kospi200.specs import validate_config


def run():
    if (ROOT/"manifests/step25_gate_results.json").exists():
        raise SystemExit("STEP2 snapshot runner superseded by STEP2.5; use tools/step25_verify.py with original source evidence, do not overwrite verified manifests.")
    c=json.loads((ROOT/'configs/experiment_config.json').read_text());validate_config(c)
    originals=ROOT/'originals';manifest=json.loads((ROOT/'evidence/input_manifest.json').read_text())
    for item in manifest:
        p=originals/item['filename']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('Missing/modified original: '+item['filename'])
    tables={};counts=[]
    for p in sorted(originals.glob('*.csv')):
        raw=pd.read_csv(p);date_col='Date' if 'Date' in raw else '날짜';raw=raw.rename(columns={date_col:'Date'})
        dt=pd.to_datetime(raw.Date);filtered=cutoff(raw);tables[p.name]=filtered.set_index('Date')
        counts.append({'file':p.name,'before_rows':len(raw),'excluded_before_2010':int((dt<'2010-01-01').sum()),
          'excluded_2026_or_later':int((dt>'2025-12-31').sum()),'after_rows':len(filtered),
          'first_date':str(filtered.Date.min().date()),'last_date':str(filtered.Date.max().date()),
          'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    k=tables['KOSPI_200.csv'];close=k['종가'];idx=k.index
    # Diagnostic only. Never pass an observed-only calendar as verified production KRX.
    endpoint=pd.Series(idx,index=idx).shift(-20);future=close.shift(-20)
    target=pd.Series(pd.NA,index=idx,dtype='Int64');known=future.notna()&endpoint.notna()
    target.loc[known]=(future[known]>close[known]).astype(int)
    feats=local_features(close);feature_ready=feats.notna().all(axis=1)
    window_ready=feature_ready.rolling(20,min_periods=20).sum().eq(20)
    foreign_dates=tables['Foreigner_Net.csv'].index
    missing=foreign_dates[(foreign_dates>=idx.min())&(foreign_dates<=idx.max())].difference(idx)
    unknown=idx[~known]
    processed=tables['processed_regression_data.csv'];expected=(future/close-1).reindex(processed.index)
    processed_matches=bool(expected.notna().all() and np.allclose(processed.Target_Ret20,expected,rtol=0,atol=1e-12))
    rows=[]
    for i in range(1,6):
        oy=2020+i;vstart=idx[idx.year==oy-1][0];tstart=idx[idx.year==oy][0]
        for part,mask,bound in [('train',idx.year<=oy-2,vstart),('validation',idx.year==oy-1,tstart),('test',idx.year==oy,None)]:
            dates=idx[mask];kn=known.reindex(dates);purge=kn&(endpoint.reindex(dates)>=bound) if bound is not None else pd.Series(False,index=dates)
            kept=kn&~purge&window_ready.reindex(dates)
            rows.append({'origin':f'O{i}','partition':part,'observed_boundary_start':str(dates[0].date()),
               'observed_boundary_end':str(dates[-1].date()),'rows_before_label_filter':len(dates),
               'unknown_labels':int((~kn).sum()),'candidate_purged':int(purge.sum()),
               'candidate_input_ineligible':int((kn&~purge&~window_ready.reindex(dates)).sum()),
               'candidate_samples':int(kept.sum()),'candidate_first_sample':str(dates[kept][0].date()) if kept.any() else '',
               'candidate_last_sample':str(dates[kept][-1].date()) if kept.any() else '',
               'next_cutoff':str(bound.date()) if bound is not None else '',
               'confirmed_samples':'','status':'BLOCKED','reason':'KRX_calendar_and_PIT_availability_unverified'})
    report={'period':c['period'],'source_filter_counts':counts,'raw_integrity':'PASS',
      'model_fit_calls':0,'hmm_fit_calls':0,'model_forward_calls':0,'checkpoint_load_calls':0,
      'calendar_status':'BLOCKED','calendar_evidence':'Source KOSPI dates only; full official KRX calendar/price reconciliation missing',
      'foreign_dates_absent_in_kospi_count':len(missing),'foreign_dates_absent_in_kospi':[str(d.date()) for d in missing],
      'candidate_counts':{'raw_KOSPI_after_cutoff':len(k),'known_endpoint_by_observed_rows':int(known.sum()),
        'feature_warmup_exclusions':int((~feature_ready).sum()),'feature_ready_rows':int(feature_ready.sum()),
        'feature_ready_with_known_label':int((feature_ready&known).sum()),
        'include_t_window20_candidate_samples':int((window_ready&known).sum()),
        'original_exclude_t_window20_candidate_samples':int((feature_ready.shift(1,fill_value=False).rolling(20,min_periods=20).sum().eq(20)&known).sum()),
        'unknown_tail':int((~known).sum()),'unknown_start':str(unknown[0].date()),'unknown_end':str(unknown[-1].date()),
        'last_valid_prediction_base_candidate':str(idx[known][-1].date()),'last_label_end_candidate':str(endpoint[known].iloc[-1].date())},
      'confirmed_production_sample_count':None,'candidate_status':'BLOCKED_NOT_KRX_CERTIFIED_NOT_PIT_READY',
      'processed_target_recomputed_inside_cutoff_matches':processed_matches,
      'feature_values_generated_for_model':False,
      'availability_status':{v:'BLOCKED' for v in c['availability']},
      'lineage_status':'Schema implemented; actual release records unavailable; no fabricated lineage rows',
      'source_notes':['2026 rows inspected only for exclusion counts/hash integrity; never used in features/targets.',
        '2025-12-31 US source dates remain inside date filter but cannot match earlier KRX decisions if released later.',
        'Original audit evidence remains historical and is not an analysis input.']}
    dest=ROOT/'manifests';dest.mkdir(exist_ok=True)
    (dest/'data_cutoff_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    pd.DataFrame(rows).to_csv(dest/'rolling_origin_manifest.csv',index=False)
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':run()
