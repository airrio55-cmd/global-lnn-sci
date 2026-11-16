from pathlib import Path
import json,hashlib,datetime,calendar,sys
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];S=Path(sys.argv[1]) if len(sys.argv)>1 else Path('work/step25_sources');M=R/'manifests';P=R/'provenance';P.mkdir(exist_ok=True)
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat();CHECKED='2026-11-16'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
inputs=json.loads((R/'evidence/input_manifest.json').read_text())
for it in inputs:assert digest(R/'originals'/it['filename'])==it['sha256']
logs=json.loads((S/'access_log.json').read_text())+json.loads((S/'krx_calendar_access.json').read_text())+json.loads((S/'krx_query_log.json').read_text())+json.loads((S/'krx_price_access.json').read_text())
for rec in logs:
 rec.setdefault('use','Official-source verification research, not price-vintage proof')
 rec.setdefault('limitation','Retrieval alone does not establish full historical coverage or supplied CSV origin')
 rec['checked_date_kst']=CHECKED
 if rec['id'].startswith('NASDAQ_CAL_') and int(rec['id'].split('_')[-1])<2021:
  rec['semantic_status']='FAILED_EXPECTED_PDF_RECEIVED_HTML_ERROR_PAGE'
 elif rec.get('http_status')==200 and rec['id'] in ['KRX_INDEX_PAGE','TORCH_SERIALIZATION']:
  rec['semantic_status']='FAILED_ERROR_OR_REDIRECT_PAGE_NOT_REQUESTED_CONTENT'
 elif rec.get('http_status')==400 or rec.get('error'):rec['semantic_status']='FAILED'
 else:rec['semantic_status']='RETRIEVED_REQUIRES_SCOPE_INTERPRETATION'
 # OTP bodies are ephemeral public form tokens, never published.
 if 'OTP' in rec['id']:rec['limitation']='Form token not published; not an account credential or evidence of price access'
write(P/'step25_source_catalog.json',{'checked_at':NOW,'raw_document_storage':'work/step25_sources only; raw pages/PDFs/wheel and source prices not published','sources':logs})
holidays={};all_sessions=[];annual=[]
for y in range(2010,2026):
 a=json.loads((S/f'KRX_HOLIDAY_{y}.json').read_text())['block1'];assert a and all(pd.Timestamp(d['calnd_dd']).year==y for d in a)
 for d in a:holidays.setdefault(pd.Timestamp(d['calnd_dd']),[]).append(d['holdy_nm'])
 week=pd.bdate_range(f'{y}-01-01',f'{y}-12-31');h=pd.DatetimeIndex([d['calnd_dd'] for d in a]);ss=week.difference(h);all_sessions.extend(ss)
 annual.append({'year':y,'sessions':len(ss),'source_holiday_rows':len(a),'source_id':f'KRX_HOLIDAY_{y}','response_sha256':digest(S/f'KRX_HOLIDAY_{y}.json'),'source_url':'https://open.krx.co.kr/contents/OPN/99/OPN99000001.jspx','query_year':y,'gridTp':'KRX','checked_at':NOW,'status':'PASS','basis':'Monday-Friday less official KRX cash-market holidays; no derivative-night calendar'})
sessions=pd.DatetimeIndex(all_sessions,name='Date');assert len(sessions)==3939
k=pd.read_csv(R/'originals/KOSPI_200.csv',parse_dates=['Date']);k=k[k.Date.between('2010-01-01','2025-12-31')].set_index('Date');missing=sessions.difference(k.index);non_session=k.index.difference(sessions);assert len(missing)==45 and len(non_session)==0 and k.index.is_unique
sid={d:i for i,d in enumerate(sessions)};verification=[]
for d in pd.date_range('2010-01-01','2025-12-31'):
 isopen=d in sid;reason='OPEN' if isopen else ('WEEKEND' if d.weekday()>=5 else '|'.join(holidays.get(d,['UNKNOWN'])))
 verification.append({'date':str(d.date()),'is_open':isopen,'session_id':sid.get(d,''),'kospi_rows':int(d in k.index),'reason':reason,'source_id':f'KRX_HOLIDAY_{d.year}','checked_date':CHECKED})
pd.DataFrame(verification).to_csv(M/'krx_calendar_verification.csv',index=False)
pd.DataFrame({'Date':sessions.strftime('%Y-%m-%d'),'session_id':np.arange(len(sessions))}).to_csv(M/'krx_sessions_2010_2025.csv',index=False)
write(P/'krx_calendar_provenance.json',{'status':'PASS','checked_at':NOW,'source_url':'https://open.krx.co.kr/contents/MKD/01/0110/01100305/MKD01100305.jsp','rules_url':'https://regulation.krx.co.kr/contents/RGL/03/03010100/RGL03010100T1.jsp','parameters':{'bld':'MKD/01/0110/01100305/mkd01100305_01','gridTp':'KRX','search_bas_yy':'2010..2025'},'session_count':len(sessions),'calendar_rows':len(verification),'session_csv_sha256':digest(M/'krx_sessions_2010_2025.csv'),'verification_csv_sha256':digest(M/'krx_calendar_verification.csv'),'annual':annual,'confidence':'HIGH_OFFICIAL_HISTORICAL_HOLIDAY_RESPONSES_PLUS_OFFICIAL_WEEKDAY_RULE','limitations':['Cash-market calendar only, not Eurex/night derivatives.','Session confirmation is not proof of index close or supplied CSV availability.','Source responses are checked as of retrieval; no historical release-vintage archive.']})
rows=[]
for d in missing:
 rows.append({'date':str(d.date()),'krx_open':'YES','kospi200_calculation':'UNKNOWN_NO_DAILY_OFFICIAL_PRICE_RESPONSE','official_close_exists':'UNKNOWN','official_close':'','kospi_file_missing':'YES','source_id':f'KRX_HOLIDAY_{d.year}','source_url':'https://open.krx.co.kr/contents/MKD/01/0110/01100305/MKD01100305.jsp','checked_date':CHECKED,'verdict':'MISSING_KRX_SESSION_CONFIRMED_CLOSE_UNKNOWN'})
pd.DataFrame(rows).to_csv(M/'kospi_missing_dates_audit.csv',index=False)
pd.DataFrame(columns=['Date','official_close','index_identifier','source_url','source_response_sha256','verified_at','status']).to_csv(M/'kospi_official_close_supplement.csv',index=False)
# Official calendar axis diagnostic, prices still original/unverified; no filling or price supplement.
sys.path.insert(0,str(R/'src'));from kospi200.data import Calendar,labels_on_calendar,local_features
from kospi200.folds import rolling_origins
cal=Calendar(sessions,'KRX official annual cash holidays + weekday rules',digest(M/'krx_sessions_2010_2025.csv'),True)
labs=labels_on_calendar(k['종가'],cal);feats=local_features(labs.Close);feature_ok=feats.notna().all(axis=1);window_ok=feature_ok.rolling(20,min_periods=20).sum().eq(20)
folds,_=rolling_origins(labs,cal,window_ok);folds=folds.rename(columns={'boundary_start':'official_boundary_start','boundary_end':'official_boundary_end','eligible_samples':'diagnostic_available_price_samples','first_sample':'diagnostic_first_sample','last_sample':'diagnostic_last_sample'})
folds['confirmed_samples']='';folds['calendar_status']='PASS';folds['status']='BLOCKED';folds['reason']='Official_price_provenance_and_PIT_unverified; no price imputation'
for i,row in folds.iterrows():
 origin=row.origin;yr=2020+int(origin[1]);partition=row.partition
 dates=sessions[sessions.year<=yr-2] if partition=='train' else sessions[sessions.year==(yr-1 if partition=='validation' else yr)]
 good=labs.loc[dates];purge=good.Target.notna() & (good.label_end>=pd.Timestamp(row.next_cutoff)) if row.next_cutoff else pd.Series(False,index=dates)
 kept=good.Target.notna()&~purge&window_ok.reindex(dates)
 folds.loc[i,'diagnostic_max_label_end']=str(good.loc[kept,'label_end'].max().date()) if kept.any() else ''
folds.to_csv(M/'rolling_origin_manifest.csv',index=False)
obs_end=pd.Series(k.index,index=k.index).shift(-20);real_end=labs.label_end.reindex(k.index);comparable=obs_end.notna()&real_end.notna()
labeldiag={'status':'DIAGNOSTIC_ONLY_ORIGINAL_PRICES_NOT_OFFICIALLY_RECONCILED','calendar_verified':True,'actual_sessions':len(sessions),'original_price_rows':len(k),'missing_current_close':int(labs.Close.isna().sum()),'label_status_counts':{str(a):int(b) for a,b in labs.label_status.value_counts().items()},'known_original_price_labels_on_calendar':int(labs.Target.notna().sum()),'feature_ready_rows':int(feature_ok.sum()),'feature_ready_known_labels':int((feature_ok&labs.Target.notna()).sum()),'window20_include_t_candidates':int((window_ok&labs.Target.notna()).sum()),'row20_vs_KRX20_different_label_end':int((obs_end[comparable]!=real_end[comparable]).sum()),'last_valid_base_date_on_calendar':str(labs.index[labs.Target.notna()][-1].date()),'last_label_end':str(labs.loc[labs.Target.notna(),'label_end'].iloc[-1].date()),'unknown_tail':20,'confirmed_production_samples':None,'limitation':'Calendar endpoint dates verified; original price values and feature availability remain uncertified.'}
write(M/'step25_label_diagnostics.json',labeldiag)
# US 2021-25 official annual calendars + separate unscheduled closure alert.
events=json.loads((S/'us_pdf_events.json').read_text());flat=[e for arr in events.values() for e in arr];event_by={e['date']:e for e in flat};usrows=[]
for y in range(2021,2026):
 for d in pd.bdate_range(f'{y}-01-01',f'{y}-12-31'):
  event=event_by.get(str(d.date()));closed=event is not None and event['kind']=='CLOSED';hour='13:00' if event is not None and event['kind']=='EARLY_CLOSE' else '16:00'
  close=pd.NaT if closed else pd.Timestamp(str(d.date())+' '+hour,tz='America/New_York')
  usrows.append({'source_date':str(d.date()),'is_open':not closed,'close_et':'' if closed else close.isoformat(),'close_utc':'' if closed else close.tz_convert('UTC').isoformat(),'close_kst':'' if closed else close.tz_convert('Asia/Seoul').isoformat(),'kind':'CLOSED' if closed else ('EARLY_CLOSE' if hour=='13:00' else 'REGULAR'),'source_id':event['source_id'] if event else f'NASDAQ_CAL_{y}','checked_date':CHECKED,'limitation':'Market session close only; CSV publisher availability unknown'})
us=pd.DataFrame(usrows);us.to_csv(M/'us_official_schedule_2021_2025.csv',index=False)
# Preserve explicit older official events, without claiming full older calendars.
older=[{'date':'2010-11-26','kind':'EARLY_CLOSE','close_local':'13:00','source_id':'NASDAQ_EARLY_2010'},{'date':'2020-11-27','kind':'EARLY_CLOSE','close_local':'13:00','source_id':'NASDAQ_EARLY_2020'},{'date':'2012-10-29','kind':'CLOSED','close_local':'','source_id':'NASDAQ_CLOSURE_SANDY1'},{'date':'2012-10-30','kind':'CLOSED','close_local':'','source_id':'NASDAQ_CLOSURE_SANDY2'},{'date':'2018-12-05','kind':'CLOSED','close_local':'','source_id':'NASDAQ_CLOSURE_BUSH'}]
pd.DataFrame(flat+older).sort_values('date').to_csv(M/'us_verified_special_dates.csv',index=False)
# Clock transformations for all 16 years: not standalone proof of an actual trading session.
dst=[]
for y in range(2010,2026):
 def nth_sunday(month,n):return [d for d in calendar.Calendar().itermonthdates(y,month) if d.month==month and d.weekday()==6][n-1]
 for kind,day in [('START',nth_sunday(3,2)),('END',nth_sunday(11,1))]:
  for offset in [-2,1]:
   date=pd.Timestamp(day)+pd.Timedelta(days=offset);close=pd.Timestamp(str(date.date())+' 16:00',tz='America/New_York')
   dst.append({'year':y,'transition':kind,'transition_date':str(day),'clock_probe_date':str(date.date()),'close_et':close.isoformat(),'close_utc':close.tz_convert('UTC').isoformat(),'close_kst':close.tz_convert('Asia/Seoul').isoformat(),'scope':'timezone_clock_rule_only','source_id':'NIST_DST','checked_date':CHECKED})
pd.DataFrame(dst).to_csv(M/'us_dst_transition_checks.csv',index=False)
# Date-only mapping audit, values not exported. available_at deliberately blank.
nas=pd.read_csv(R/'originals/Nasdaq.csv',parse_dates=['Date']);nas=nas[nas.Date.between('2010-01-01','2025-12-31')].set_index('Date')
sox=pd.read_csv(R/'originals/SOX.csv',parse_dates=['Date']);sox=sox[sox.Date.between('2010-01-01','2025-12-31')].set_index('Date');assert nas.index.equals(sox.index)
usdates=pd.Series(nas.index,index=nas.index);same=usdates.reindex(sessions);joined=same.ffill();joined_shift=joined.shift(1);source_shift=usdates.shift(1).reindex(sessions).ffill()
openus=us[us.is_open].copy();openus['close_utc']=pd.to_datetime(openus.close_utc,utc=True);openus['source_date']=pd.to_datetime(openus.source_date)
checkdec=pd.DataFrame({'kr_date':sessions,'decision_at':sessions.tz_localize('Asia/Seoul')+pd.Timedelta(hours=18)});checkdec['decision_at']=checkdec.decision_at.dt.tz_convert('UTC')
cand=pd.merge_asof(checkdec.sort_values('decision_at'),openus.sort_values('close_utc')[['source_date','close_utc','source_id']],left_on='decision_at',right_on='close_utc',direction='backward')
cand.loc[cand.kr_date.dt.year<2021,['source_date','close_utc','source_id']]=pd.NA
mapping=[]
fmt=lambda x:'' if pd.isna(x) else str(pd.Timestamp(x).date())
for i,row in cand.iterrows():
 d=row.kr_date;verified=pd.notna(row.source_date)
 mapping.append({'kr_date':fmt(d),'variables':'Nasdaq|SOX','kospi_price_present':d in k.index,'decision_at_utc':row.decision_at.isoformat(),'same_date_join':fmt(same.loc[d]),'same_date_ffill':fmt(joined.loc[d]),'joined_KR_shift1':fmt(joined_shift.loc[d]),'source_US_shift1':fmt(source_shift.loc[d]),'latest_completed_session':fmt(row.source_date),'market_close_utc':'' if not verified else row.close_utc.isoformat(),'market_schedule_verified':verified,'provider_available_at':'','production_PIT_date':'','input_status':'BLOCKED','source_id':'' if not verified else row.source_id})
mapdf=pd.DataFrame(mapping);mapdf.to_csv(M/'us_market_availability_audit.csv',index=False)
covered=mapdf.market_schedule_verified;realmap=mapdf.loc[covered]
summary={'checked_at':NOW,'scope':'2021-2025 verified market-close calendar candidate; NOT provider PIT input mapping','KRX_decision_dates':len(mapdf),'verified_calendar_candidate_dates':int(covered.sum()),'older_or_no_prior_verified_schedule':int((~covered).sum()),'same_date_ffill_differs_from_completed_session':int((realmap.same_date_ffill!=realmap.latest_completed_session).sum()),'joined_KR_shift1_differs':int((realmap.joined_KR_shift1!=realmap.latest_completed_session).sum()),'source_US_shift1_differs':int((realmap.source_US_shift1!=realmap.latest_completed_session).sum()),'provider_PIT_verified_dates':0,'official_US_sessions_by_year':{str(y):int(((pd.to_datetime(us.source_date).dt.year==y)&us.is_open).sum()) for y in range(2021,2026)},'early_closes_verified_2021_2025':int(us.kind.eq('EARLY_CLOSE').sum()),'full_2010_2020_calendar_status':'BLOCKED; PDF URL probes returned HTML error bodies','DST_clock_probes':len(dst),'limitations':['No 0-second publisher delay assumed.','latest_completed_session is a diagnostic calendar candidate, never populated as production_PIT_date.','Regular-session close is not index-finalization or CSV-publication time.','Nasdaq/SOX share source-date arrays, so one mapping row covers both; price values not published.']}
write(M/'us_mapping_summary.json',summary)
# Processed formula audit, strictly cutoff-first and numeric only; no source claim.
f=pd.read_csv(R/'originals/Foreigner_Net.csv',parse_dates=['날짜']);f=f[f['날짜'].between('2010-01-01','2025-12-31')].set_index('날짜')
p=pd.read_csv(R/'originals/processed_regression_data.csv',parse_dates=['Date']).set_index('Date');j=k[['종가','거래량']].join([nas.Close.rename('Nasdaq'),sox.Close.rename('SOX'),f['외국인'].rename('Foreigner')]).ffill()
formula=[]
for col,v,expr in [('KOSPI200',j['종가'],'KOSPI_200.Close'),('Vol',j['거래량'],'KOSPI_200.Volume'),('Foreigner',j.Foreigner,'Foreign_Net same date'),('Nasdaq',j.Nasdaq,'same-date Nasdaq Close joined on observed KOSPI rows then ffill'),('SOX',j.SOX,'same-date SOX Close joined on observed KOSPI rows then ffill'),('Nasdaq_Ret20',j.Nasdaq.pct_change(20,fill_method=None),'Nasdaq / Nasdaq.shift(20 observed KOSPI rows) - 1'),('Foreigner_NetBuy20',j.Foreigner.rolling(20).sum(),'Foreigner.rolling(20 observed KOSPI rows).sum()'),('SOX_Lag1',j.SOX.shift(1),'SOX.shift(1 observed KOSPI row)'),('Target_Ret20',j['종가'].shift(-20)/j['종가']-1,'Close.shift(-20 observed KOSPI rows)/Close-1')]:
  v=v.reindex(p.index);formula.append({'column':col,'candidate_formula':expr,'matched_rows':int(np.isclose(p[col],v,rtol=0,atol=1e-9).sum()),'total_rows':len(p),'max_absolute_error':float((p[col]-v).abs().max()),'status':'NUMERIC_MATCH_NOT_GENERATOR_PROVENANCE'})
write(P/'processed_formula_verification.json',{'status':'PARTIAL','checked_at':NOW,'input_sources':[{'file':it['filename'],'sha256':it['sha256'],'url':None,'origin':'user_attachment_not_upstream_attestation'} for it in inputs if it['filename'].endswith('.csv')],'generation_code_found':False,'revision_history_found':False,'used_in_default_experiment':False,'formulas':formula,'limitation':'A numerically matching candidate recipe is not proof of author, extraction process, revisions or PIT safety.'})
foreign={'status':'BLOCKED','checked_at':NOW,'file':'Foreigner_Net.csv','sha256':digest(R/'originals/Foreigner_Net.csv'),'source_url':None,'official_reference_url':'https://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd','market_scope':'UNKNOWN','instrument_scope':'UNKNOWN','amount_or_quantity':'UNKNOWN','unit':'UNKNOWN','sign_definition':'UNKNOWN','provisional_or_final':'UNKNOWN','first_publication_at':None,'revision_policy':'UNKNOWN','same_day_input_allowed':False,'source_collection_code_found':False,'alternative_A':{'definition':'F1/F2/F3 variants as predeclared where Foreign_Net is excluded; no outcome-based choice','feasible_without_foreign_provenance':True,'still_requires_other_gates':True},'alternative_B':{'definition':'previous-session flow only after verified actual release and approved max_age','status':'BLOCKED','reason':'One-session lag does not prove availability when release policy is unknown'},'selection_policy':'No model performance examined; no new A/B selection made','limitation':'Investor category column names and matching KRX dates do not establish market scope, cash/futures, units, or timing.'}
write(M/'foreign_net_provenance.json',foreign)
# Source-version evidence without importing or installing packages.
wheel=json.loads((S/'ncps_static_dist.json').read_text());notebooks=[]
for file in (R/'originals').glob('*.ipynb'):
 n=json.loads(file.read_text());out=''.join(''.join(o.get('text',[])) for o in n['cells'][1].get('outputs',[]));notebooks.append({'file':file.name,'sha256':digest(file),'python_metadata':n['metadata']['language_info']['version'],'stored_torch_output':'2.10.0+cpu' if '2.10.0+cpu' in out else None,'stored_cuda_available':False if 'CUDA available: False' in out else None,'ncps_version':None,'hmmlearn_version':None,'limitation':'Stored notebook output only, not a current run or proof of every historical training environment'})
write(P/'ltc_version_verification.json',{'status':'PARTIAL','checked_at':NOW,'notebooks':notebooks,'root_requirements_url':'https://github.com/airrio55-cmd/global-lnn-sci/blob/81010974d4f56c5c02bc028af20e6bab356ae0e4/requirements.txt','root_requirements_version_pins':False,'ncps_reference_distribution':wheel,'reference_commit':'695ec22d7d1831f2ced67346ef7d2f08c525bd47','reference_cell_matches_ncps_1_0_1_bytewise':digest(S/'NCPS_LTC_CELL.html')==wheel['files']['ncps/torch/ltc_cell.py']['sha256'],'reference_wrapper_matches_ncps_1_0_1_bytewise':digest(S/'NCPS_LTC_WRAPPER.html')==wheel['files']['ncps/torch/ltc.py']['sha256'],'wrapper_default_implicit_constraints':True,'cell_direct_default_implicit_constraints':False,'ode_unfolds_default':6,'timespans_omitted_elapsed_time':1.0,'tau_raw':'positive(cm)/positive(gleak)','tau_effective':'positive(cm)/(positive(gleak)+sum(g_recurrent(hidden))+sum(g_sensory(mapped_inputs)))','tau_interpretation':'Frozen-state/input conductance time constant; not full nonlinear Jacobian timescale','dt_unit':'UNKNOWN_PHYSICAL_UNIT; one numerical step when timespans omitted, not proved one day','checkpoint_compatibility':'BLOCKED_NOT_LOADED_OR_TESTED','installed_packages':False,'model_forward':False,'limitation':'Reference source equivalence is not proof the original notebooks used ncps 1.0.1. Original ncps/hmmlearn lock and compatible checkpoints still required.'})
write(M/'step25_analysis_summary.json',{'checked_at':NOW,'labels':labeldiag,'us_mapping':summary,'original_integrity':'PASS','model_training':0,'hmm_fit':0,'GPU':0,'model_forward':0,'checkpoint_load':0,'package_install':0})
print(json.dumps({'sessions':len(sessions),'missing':len(missing),'label_diagnostics':labeldiag,'us_mapping':summary,'folds':folds[['origin','partition','official_boundary_start','official_boundary_end','purged_labels','diagnostic_available_price_samples','diagnostic_max_label_end']].to_dict('records')},ensure_ascii=False,indent=2))
