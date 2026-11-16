"""Local-only price/target derivatives; publish only redacted audits and summaries."""
from pathlib import Path
import sys,json,hashlib,datetime,shutil,argparse
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from kospi200.data import Calendar,BlockedError
from kospi200.reconciliation import reconcile_close,label_audit,full_excel_comparison,validate_prices,sha256
from kospi200.folds import rolling_origins
CHECKED='2026-11-16'

def save_json(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def find_one(name):
    options=list((ROOT/'data/user_supplied').glob(name)) if (ROOT/'data/user_supplied').exists() else []
    options+=list(Path('/workspace/attachments').glob('*/'+name))
    if not options:return None
    hashes={sha256(p) for p in options}
    if len(hashes)>1:raise BlockedError('Ambiguous input versions: '+name)
    return options[0]

def run():
    args=argparse.ArgumentParser();args.add_argument('--full-excel',type=Path);args.add_argument('--full-skiprows',type=int,default=0);args.add_argument('--full-sheet');args.add_argument('--full-date-column');args.add_argument('--full-close-column');a=args.parse_args()
    csv=find_one('KOSPI200_누락45일_종가_보완.csv');xlsx=find_one('KOSPI200_누락45일_종가_보완.xlsx');full=a.full_excel or find_one('KOSPI 200 종가.xlsx')
    if csv is None or xlsx is None:raise BlockedError('Required 45-row CSV/XLSX missing; do not create supplements')
    if full is not None and not full.is_file():raise BlockedError('Explicit full Excel path missing')
    inputs=[]
    for name,p in [('KOSPI 200 종가.xlsx',full),('KOSPI200_누락45일_종가_보완.csv',csv),('KOSPI200_누락45일_종가_보완.xlsx',xlsx)]:
        inputs.append({'file':name,'exists':p is not None,'sha256':sha256(p) if p else None,'bytes':p.stat().st_size if p else None,'status':'PASS_PRESENT' if p else 'BLOCKED_MISSING'})
    m=ROOT/'manifests';derived=ROOT/'data/derived';private=ROOT/'data/user_supplied';derived.mkdir(parents=True,exist_ok=True);private.mkdir(parents=True,exist_ok=True)
    for p in [csv,xlsx]+([full] if full is not None else []):
        destination=private/p.name
        if destination.exists() and sha256(destination)!=sha256(p):raise BlockedError('Would overwrite a different preserved input')
        if not destination.exists():shutil.copy2(p,destination)
    if full:
        if not all([a.full_sheet,a.full_date_column,a.full_close_column]):raise BlockedError('Full Excel requires explicit sheet/date/close column arguments; no guessed mappings')
        raw_full=pd.read_excel(full,sheet_name=a.full_sheet,skiprows=a.full_skiprows,header=None,names=['Date','Close','Unused'])
        if (a.full_date_column,a.full_close_column)!=('Date','Close'):raise BlockedError('Explicit no-header mapping requires Date,Close positional names')
        full_frame=raw_full[['Date','Close']]
        validated,full_details=validate_prices(full_frame)
        full_details.update({'sheet':a.full_sheet,'skipped_metadata_rows':a.full_skiprows,'mapping':'A=Date,B=Close; no header','supplier_verified':False})
    else:full_frame=None;full_details=None
    original_path=ROOT/'originals/KOSPI_200.csv';orig=pd.read_csv(original_path,float_precision='round_trip').rename(columns={'종가':'Close'})[['Date','Close']]
    supp=pd.read_csv(csv,float_precision='round_trip');sx=pd.read_excel(xlsx,sheet_name='누락 45일').rename(columns={'날짜 (Date)':'Date','KOSPI 200 종가':'Close'})[['Date','Close']]
    expected=pd.read_csv(m/'kospi_missing_dates_audit.csv',parse_dates=['date']).date
    sp=ROOT/'manifests/krx_sessions_2010_2025.csv';pro=json.loads((ROOT/'provenance/krx_calendar_provenance.json').read_text());assert sha256(sp)==pro['session_csv_sha256']
    sessions=pd.DatetimeIndex(pd.read_csv(sp,parse_dates=['Date']).Date,name='Date');cal=Calendar(sessions,pro['source_url'],sha256(sp),True)
    completed,integrity=reconcile_close(orig,supp,sx,calendar=cal,expected_missing=expected,
       original_file=original_path.name,supplement_file=csv.name,original_sha256=sha256(original_path),supplement_sha256=sha256(csv))
    compared=full_excel_comparison(orig,full_frame,calendar=cal)
    if full:
        compared.to_csv(derived/'kospi_price_reconciliation_private.csv',index=False,float_format='%.17g')
        public=compared.drop(columns=['Close_original','Close_excel','difference']).copy();public['difference']='WITHHELD_SOURCE_LICENSE_UNCONFIRMED'
        conflicts=int(compared['exact_match'].eq(False).sum());performed=len(compared)
        full_details['common_exact_matches']=int(compared.exact_match.sum())
        full_details['common_rounded_2dp_matches']=int(compared.rounded_2dp_match.sum())
        full_details['common_within_1e_minus9_matches']=int(compared.within_1e_minus9.sum())
        full_details['maximum_absolute_price_difference']=float(compared.difference.abs().max())
        sv=validate_prices(supp)[0].set_index('Date').Close;fv=validated.set_index('Date').Close
        full_details['supplement_45_exact_matches']=int(sv.eq(fv.reindex(sv.index)).sum())
        if full_details['supplement_45_exact_matches']!=45:raise BlockedError('Full Excel and supplement price conflict; no substitution')
    else:
        public=compared;conflicts=None;performed=0
    public.to_csv(m/'kospi_price_reconciliation.csv',index=False)
    completed.to_csv(derived/'kospi200_close_completed_2010_2025.csv',index=False,float_format='%.17g')
    label,features,window_ok,differences,summary=label_audit(orig,completed,cal)
    # No full source prices, target sequence or daily numeric feature series in public GitHub.
    target_output=label.drop(columns='Close').copy()
    target_output['label_status']=np.where(label.Target.notna(),'USER_SUPPLIED_LABEL_KNOWN','UNKNOWN_HORIZON_OUTSIDE_PERIOD')
    target_output['price_verification_status']='USER_SUPPLIED_NOT_KRX_OFFICIAL_VERIFIED'
    sources=completed.set_index('Date').source_sha256
    target_output['base_source_sha256']=sources
    target_output['endpoint_source_sha256']=sources.reindex(pd.DatetimeIndex(label.label_end)).to_numpy()
    target_output.to_csv(derived/'kospi200_targets_20sessions_2010_2025.csv',index_label='Date',na_rep='UNKNOWN')
    features.to_csv(derived/'kospi200_local_features_2010_2025.csv',index_label='Date',na_rep='UNKNOWN',float_format='%.17g')
    differences.to_csv(derived/'historical_baseline_label_comparison_private.csv',index=False,na_rep='UNKNOWN')
    public_diff=differences.drop(columns=['old_Target','new_Target','Target_changed']).copy();public_diff.to_csv(m/'step26_historical_horizon_audit.csv',index=False)
    sa=pd.DataFrame({'Date':pd.to_datetime(supp.Date),'csv_xlsx_price_match':True,'expected_missing_date':True,'verified_session':True,
      'overlaps_original':False,'included_once':True,'value_status':'USER_SUPPLIED_VERIFIED_MATCH','official_price_verified':False,
      'source_sha256':sha256(csv),'checked_date':CHECKED})
    sa.sort_values('Date').to_csv(m/'kospi_supplement_45_audit.csv',index=False)
    folds,selected=rolling_origins(label,cal,window_ok)
    for i,row in folds.iterrows():
        origin=row.origin;yr=2020+int(origin[1:]);dates=cal.sessions[cal.sessions.year<=yr-2] if row.partition=='train' else cal.sessions[cal.sessions.year==(yr-1 if row.partition=='validation' else yr)]
        l=label.loc[dates];known=l.Target.notna();before=known&window_ok.reindex(dates)
        retained=selected[origin][row.partition];t=label.loc[retained,'Target'].dropna().astype(int)
        folds.loc[i,'window_eligible_before_purge']=int(before.sum());folds.loc[i,'up_samples']=int(t.eq(1).sum());folds.loc[i,'down_or_equal_samples']=int(t.eq(0).sum());folds.loc[i,'up_ratio']=float(t.mean()) if len(t) else np.nan
        folds.loc[i,'min_label_end']=str(label.loc[retained,'label_end'].min().date()) if len(t) else ''
        folds.loc[i,'max_label_end']=str(label.loc[retained,'label_end'].max().date()) if len(t) else ''
        folds.loc[i,'label_end_cutoff_violations']=int(label.loc[retained,'label_end'].ge(pd.Timestamp(row.next_cutoff)).sum()) if row.next_cutoff else 0
    folds=folds.rename(columns={'eligible_samples':'domestic_supplied_value_structural_samples','status':'structural_status'})
    folds['structural_status']='PASS_USER_SUPPLIED_NUMERIC_SESSION_LABEL_INTEGRITY';folds['official_price_reconciled_samples']='';folds['domestic_PIT_verified_samples']='';folds['external_5feature_PIT_verified_samples']='';folds['execution_status']='BLOCKED_SOURCE_PIT_RUNTIME'
    folds.to_csv(m/'step26_rolling_origin_manifest.csv',index=False)
    # Exact formulas unchanged; measure data/calendar effects only, never model metrics.
    old=validate_prices(orig)[0].set_index('Date').Close
    old_features=pd.DataFrame({'Log_Ret':np.log(old/old.shift(1)),'Disparity':old/old.rolling(20).mean()-1,'Vol_Regime':np.log(old/old.shift(1)).rolling(40).std()})
    feature_changes={}
    for col in features:
        a0=old_features[col];b0=features[col].reindex(old.index);valid=a0.notna()&b0.notna()
        feature_changes[col]={'common_finite_rows':int(valid.sum()),'exact_value_differences':int(a0[valid].ne(b0[valid]).sum()),'differences_over_1e_minus12':int((a0[valid]-b0[valid]).abs().gt(1e-12).sum()),'max_absolute_difference':float((a0[valid]-b0[valid]).abs().max())}
    artifacts=[]
    for p in sorted(derived.glob('*.csv')):artifacts.append({'file':'data/derived/'+p.name,'sha256':sha256(p),'bytes':p.stat().st_size,'publication':'LOCAL_ONLY_LICENSE_SOURCE_UNCONFIRMED'})
    blocked=[{'id':'FULL_EXCEL_PRESENT','status':'BLOCKED' if not full else 'PASS','reason':'KOSPI 200 종가.xlsx not found' if not full else 'Present'},
       {'id':'COMMON_3894_PRICE_COMPARISON','status':'BLOCKED' if not full else 'PASS','reason':'Full Excel missing; zero comparisons; conflict count unknown' if not full else 'Differences recorded, neither source assumed true'},
       {'id':'OFFICIAL_PRICE_PROVENANCE','status':'BLOCKED','reason':'User-supplied agreement is not official provider/extraction/revision certification'},
       {'id':'DOMESTIC_CLOSE_18KST_AVAILABILITY','status':'BLOCKED','reason':'Original and supplement publication timing unknown'},
       {'id':'EXTERNAL_5FEATURE_PIT','status':'BLOCKED','reason':'Foreign_Net/Nasdaq/SOX availability unverified'},
       {'id':'ORIGINAL_RUNTIME_CHECKPOINT','status':'BLOCKED','reason':'Original ncps/hmmlearn versions, dt unit and checkpoint compatibility remain unresolved'},
       {'id':'PUBLIC_RAW_DATA_LICENSE','status':'BLOCKED','reason':'No raw/derived prices or full daily targets/features published'}]
    if full and conflicts:blocked.append({'id':'PRICE_CONFLICT_RESOLUTION','status':'BLOCKED','reason':'Observed price differences require review; no silent substitution'})
    out={'stage':'STEP2.6','checked_date_kst':CHECKED,'period':['2010-01-01','2025-12-31'],'input_files':inputs,
       'full_excel_validation':full_details,'full_excel_common_comparisons_performed':performed,'full_excel_price_conflicts':conflicts,
       'integrity':integrity,'label_audit':summary,'feature_data_effects':feature_changes,'derived_artifacts':artifacts,
       'source_url':None,'provider':'UNKNOWN','extraction_date':'UNKNOWN','revision_policy':'UNKNOWN','source_sheet_claims':pd.read_excel(xlsx,sheet_name='출처 및 검증').to_dict('records'),
       'gate_checks':blocked,'B02_restoration_status':'PASS_USER_SUPPLIED_VERIFIED_MATCH','B02_official_price_status':'BLOCKED',
       'all_2026_input_target_HMM_ablation_tau_observations_used':0,'training_enabled':False,'hmm_fit_enabled':False,'GPU_executed':False,
       'model_forward_executed':False,'checkpoint_loaded':False,'new_model_performance_or_pvalues_generated':False,'STEP3_smoke_ready':False,
       'future_target_invariance_contract':'Only labels with label_end<=perturbation cutoff must remain unchanged when prices strictly after that cutoff change. Prices inside a target horizon are expected to affect that target.'}
    save_json(m/'step26_cutoff_label_audit.json',out)
    save_json(ROOT/'provenance/step26_data_publication.json',{'checked_date_kst':CHECKED,'inputs':inputs,'derived_artifacts':artifacts,'raw_price_target_feature_series_publication_allowed':False,'public_audit_policy':'Dates, flags, input/artifact hashes and aggregate counts only; raw prices and daily labels/features remain local','comparison_policy':'Original prices preserved. Full Excel is a comparison-only source; numeric differences are recorded without substitution.'})
    print(json.dumps({'integrity':integrity,'full_excel_present':full is not None,'price_conflicts':conflicts,'label_audit':summary,'folds':folds[['origin','partition','raw_rows','window_eligible_before_purge','purged_labels','domestic_supplied_value_structural_samples','up_ratio']].to_dict('records')},ensure_ascii=False,indent=2))
if __name__=='__main__':run()
