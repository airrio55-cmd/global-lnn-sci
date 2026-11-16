"""Aggregate Pilot diagnostics and plots only; never trains or reads Test prices."""
from pathlib import Path
import sys,json,hashlib,datetime
from zoneinfo import ZoneInfo
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(str(v) for v in row)+' |' for row in rows)+'\n'
def write(name,text):(ROOT/'reports'/name).write_text(text)
if __name__=='__main__':
 m=json.loads((ROOT/'manifests/step3a_execution_manifest.json').read_text());g=json.loads((ROOT/'manifests/step3a_preflight.json').read_text());config=json.loads((ROOT/'configs/step3a_pilot_config.json').read_text())
 runs=pd.read_csv(ROOT/'manifests/step3a_pilot_runs.csv');metrics=pd.read_csv(ROOT/'manifests/step3a_pilot_metrics.csv');history=pd.read_csv(ROOT/'manifests/step3a_epoch_history.csv')
 if m['fit_attempts']!=10 or m['completed_models']+m['failed_models']!=10:raise RuntimeError('Wait for all ten reserved fits to terminate before reporting')
 # Diagnostic curves consist solely of per-epoch aggregate losses / validation BA.
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 dest=ROOT/'reports/assets';dest.mkdir(exist_ok=True)
 for kind in ['loss','validation_ba']:
  fig,axes=plt.subplots(5,2,figsize=(12,14),constrained_layout=True)
  for i,model in enumerate(config['models']):
   for j,candidate in enumerate(['A','B']):
    key=f'{candidate}_{model}';ax=axes[i,j];h=history[history.run_id==key];row=m['fit_ledger'][key]
    if len(h):
     if kind=='loss':ax.plot(h.epoch,h.train_loss,label='Train focal loss');ax.plot(h.epoch,h.validation_loss,label='Validation focal loss')
     else:ax.plot(h.epoch,h.validation_BA,label='Validation BA');ax.set_ylim(0,1)
     best=row.get('best_validation_epoch')
     if best:ax.axvline(best,color='gray',linestyle='--',linewidth=.8,label='Selected epoch')
    ax.set_title(f'{candidate} / {model} / {row["status"]}');ax.set_xlabel('Epoch');ax.grid(alpha=.2);ax.legend(fontsize=7)
  fig.suptitle('STEP3A retrospective CPU Pilot — validation diagnostics only',fontsize=12)
  fig.savefig(dest/f'step3a_{kind}_curves.svg',metadata={'Date':None});plt.close(fig)
 rows=[]
 for candidate in ['A','B']:
  for model in config['models']:
   item=m['fit_ledger'][f'{candidate}_{model}'];s=item.get('metrics',{})
   rows.append([candidate,model,item['epochs_completed'],item.get('best_validation_epoch'),*[f'{s[k]:.6f}' if k in s else 'N/A' for k in ['validation_BA','macro_f1','recall0','recall1','accuracy','brier','prediction_positive_rate']],item.get('prediction_status',item['status'])])
 failures=[(i['run_id'],i['status'],i.get('error')) for i in m['fit_ledger'].values() if i['status'].startswith('FAILED')]
 degenerates=[i['run_id'] for i in m['fit_ledger'].values() if i.get('prediction_status')=='DEGENERATE_PREDICTION']
 write('STEP3A_PILOT_RESULTS_KO.md','''# STEP3A 제한적 실자료 CPU Pilot 결과

확인일: 2026-11-16 (Asia/Seoul). 이번 단계는 과거 자료의 Train/Validation 학습이 정상적으로 동작하는지 확인하는 **회고적·탐색적 구현 Pilot**이다. 아래 숫자는 EarlyStopping에 사용한 Validation 진단이며, 독립 Test 평가·논문 일반화 성능·실시간 예측·투자 수익성·미래정보 누출 완전 배제를 입증하지 않는다.

'''+f"실제 시작한 fit {m['fit_attempts']}/최대10, 완료 {m['completed_models']}, 실패/발산 {m['failed_models']}다. A/B 각각 다섯 아키텍처를 독립적으로 학습했고 추가 모델이나 seed를 시도하지 않았다. Train2387개·Validation228개, 원본 구조·F1입력순서·고정 offset·max100epoch·patience10·CPU/FP32/AMP-off를 유지했다.\n\n"+table(['후보','모델','실행epoch','최적epoch','Val BA','MacroF1','Recall0','Recall1','Accuracy','Brier','양성예측률','예측상태'],rows)+'''

최적 epoch는 Validation BA가 엄격히 개선된 최초 epoch다. 동점은 개선으로 보지 않고 patience를 증가시켰다. Accuracy/F1/Recall/Brier 또는 후보간 성능으로 checkpoint를 선택하지 않았다. 최적 checkpoint를 다시 로드한 Validation 결과가 해당 epoch 기록과 정확히 같음을 검사했다.

'''+f"최적 checkpoint의 단일 클래스 예측 모델: {', '.join(degenerates) if degenerates else '없음'}. 실패/발산: {failures if failures else '없음'}. 단일 클래스 예측은 DEGENERATE_PREDICTION으로 표시했고, 학습 완료 여부와 구분했다. 모든 epoch의 단일 클래스 여부도 history에 남겼다. NaN/발산/예외를 숨기거나 모델을 다시 초기화해 좋은 결과로 교체하지 않았다.\n\n"+'''
![Loss curves](assets/step3a_loss_curves.svg)

![Validation BA curves](assets/step3a_validation_ba_curves.svg)

곡선의 점선은 BA 기준 최적 epoch이며 실증 성능 우열을 주장하기 위한 그림이 아니다. 전체 epoch의 Train/Validation focal loss, BA 및 진단지표, learning rate, optimizer step, patience 상태는 manifests/step3a_epoch_history.csv에 보존했다. 모델별 checkpoint·학습 history·Validation 일별 확률은 새 ignored 디렉터리에만 저장했다. 공개 manifest에는 집계와 해시만 있다.

원본 Notebook의 모델·FocalLoss 정의는 실제 셀6/8의 소스 해시를 검증해 그대로 재사용했다. alpha0.25는 원본처럼 focal loss 전체 배율이며 클래스별 alpha_t 보정이 아니다. OneCycleLR은 steps_per_epoch38·최대100epoch로 구성하고 실제 EarlyStopping까지의 step만 수행했다. threshold는 확률>0.5다.
''')
 compare=[]
 for model in config['models']:
  a=m['fit_ledger']['A_'+model];b=m['fit_ledger']['B_'+model]
  if a.get('metrics') and b.get('metrics'):
   compare.append([model,*[f"{b['metrics'][k]-a['metrics'][k]:+.6f}" for k in ['validation_BA','macro_f1','brier','prediction_positive_rate']],b['epochs_completed']-a['epochs_completed'],b['best_validation_epoch']-a['best_validation_epoch']])
 write('STEP3A_A_B_COMPARISON_KO.md','''# STEP3A A/B 구현·수치 민감도 비교

확인일: 2026-11-16 (Asia/Seoul). A/B 모두 **BOTH_UNVERIFIED**, 공식 가격 인증 및 production-PIT는 미확정이다. A/B 주 자료를 선택하지 않았고 Validation 결과로 프로토콜을 바꾸지 않았다. 본 비교는 같은 O1 날짜·원본 모델·유효 seed·학습 설정에서 두 가격 표현의 수치 민감도를 보여주는 진단이다.

A는 기존 종가+보완 자료, B는 전체 Excel의 보존된 후보다. 전체 후보의 기존3939세션 전수검증과 SHA 동일성을 확인한 뒤, 실제 가격 값은 앞2714행(2010~2020)만 준비했다. Test 구간의 가격·타깃·예측·성능은 이 비교에 사용하지 않았다. 파일 전체 SHA 계산은 무결성 검사일 뿐 후속 구간의 가격 관측을 모델에 사용한 것이 아니다.

A/B는 독립적으로 Log_Ret·Disparity·보조 Vol_Regime과 Train-only scaler를 계산했다. Train/Validation 날짜·레이블·표본 수는 같으며, scaler를 섞지 않았다. 각 아키텍처의 A/B 유효 seed도 같다. 자료의 작은 수치 표현 차이가 정규화·신경망 최적화·Validation BA 및 EarlyStopping 경로를 바꿀 수 있지만, 이를 공급처의 정답 여부나 일반화 우열로 해석하지 않는다.

다음은 B-A 차이이며 통계적 유의성 검정이 아니다. 각 후보에서 같은 BA 규칙으로 checkpoint를 선택했지만 최적 epoch는 다를 수 있다. 따라서 차이에는 입력 표현·최적화 궤적·checkpoint 선택 효과가 함께 들어가며, 고정 epoch에서의 순수 가격 인과효과로 해석하지 않는다.

'''+table(['모델','Δ Val BA','Δ MacroF1','Δ Brier','Δ 양성예측률','Δ 실행epoch','Δ 최적epoch'],compare)+'''

단일 클래스 예측 여부와 epoch별 궤적도 두 후보를 모두 보고했다. 결과가 낮거나 단일 클래스라는 이유로 날짜·seed·구조·learning rate·피처·A/B 선택을 바꾸지 않았다. 모델별 Validation은 EarlyStopping에 사용됐으므로 독립 평가가 아니다. 한 seed의 수치 차이에서 확증적 결론을 내리지 않는다.

주 분석 자료를 확정하려면 실제 공급처, 지수 정의·단위, 추출 방식, 수정정책, 최초 공표·개정 vintage 및18:00 가용성 증거가 필요하다. 이번 Pilot의 Validation 점수는 이 증거를 대체하지 않는다.
''')
 metas=[g['datasets'][n]['metadata'] for n in ['A','B']];m0=metas[0]
 data_rows=[['가격 입력',m0['price_start']+'~'+m0['price_end'],m0['price_rows']],['Train 경계',m0['train_boundary_start']+'~'+m0['train_boundary_end'],2466],['Train 적격 기준일',m0['train_first_sample']+'~'+m0['train_last_sample'],m0['train_samples']],['Validation 경계',m0['validation_boundary_start']+'~'+m0['validation_boundary_end'],248],['Validation 적격 기준일',m0['validation_first_sample']+'~'+m0['validation_last_sample'],m0['validation_samples']],['Scaler fit 시점',m0['scaler']['fit_start']+'~'+m0['scaler']['fit_end'],m0['scaler']['fit_rows']]]
 write('STEP3A_EXECUTION_AUDIT_KO.md','''# STEP3A 실행 범위·정합성·checkpoint 감사

확인일: 2026-11-16 (Asia/Seoul). 사용자 지시가 승인한 회고적 O1 A/B F1 CPU Pilot만 실행했다. 별도 pilot_execution_enabled와 config/runner/preflight SHA에 연결된 독립 승인 기록을 사용했다. production training_enabled=false/hmm_fit_enabled=false 및 이전 gate는 변경하지 않았다. 출처/PIT 미확정을 Pilot의 명시적 한계로 둔 것이며 production gate를 PASS로 바꾼 것이 아니다.

실행 전12개 gate와 O1 전용10개 사전검사를 통과했다. 전체 source/candidate/Notebook SHA를 보존된 감사와 대조했고 전체3939세션 일치는 이전 전수검증+파일 동일성으로 확인했다. Test 가격을 새로 파싱하지 않기 위해 정확히2714개 과거행만 읽었고 모델 프로세스에는 별도 사본/배열만 전달했다. 원래 전체 가격 파일·첨부 파일과 기존 data 디렉터리는 파일 barrier로 차단했다.

'''+table(['항목','실제 기간','행/표본 수'],data_rows)+f"\nTrain purge {m0['train_purged']}개, Validation 미확정 제외 {m0['validation_unknown_excluded']}개, Train label_end cutoff 위반 {m0['train_label_cutoff_violations']}개, Validation 미래 endpoint 위반 {m0['validation_future_endpoint_violations']}개다. Train 최대label_end={m0['train_max_label_end']}, Validation 최대label_end={m0['validation_max_label_end']}다.\n\n"+'''
window=t-19~t·20실제세션, 피처순서 Log_Ret/Disparity를 고정했다. Vol_Regime은40일 trailing std(ddof1) 기반 공통 적격 마스크 보조변수로만 사용하고 신경망 입력에 넣지 않았다. NaN 자동0 치환·bfill·미래 보간은 없다. KRX session_id 차이20으로 레이블을 확인했다. Validation 말단20개에 필요한 후속 가격을 읽지 않고 UNKNOWN으로 제외했다. 2026년 관측 사용0, Test 예측0, HMM fit/GPU/전체RO/Ablation0이다.

Scaler는 유지된 Train 입력 window 날짜 합집합2406행에만 fit했고 Validation은 transform만 했다. A/B별 scaler와 피처를 독립 계산했다. Train 클래스0/1은1071/1316, Validation은70/158이다. 검증 기준일과 endpoint를 연결한 private lineage 해시를 남겼다.

## 예산과 모델 선택

A/B×다섯 모델=최대10개 fit identity만 등록했다. 완료 모델은 재개 시 건너뛰고 실패 모델도 자동 재시도하지 않는다. max100epoch·patience10·Validation BA strict improvement만 적용했다. batch64·FP32·CPU·AMP-off·고정seed/offset과원본 아키텍처를 유지했다. 실제 history와 best epoch의 선택 근거를 공개 집계에 보존했다.

## Checkpoint 복원과 재개 범위

각 모델의 첫 epoch 경계에서 model/optimizer/scheduler·EarlyStopping·Python/NumPy/Torch/DataLoader RNG를 저장·새 객체로 복원했다. state 및 RNG 동일성과 같은 Validation logits 동일성을 확인하고, 복원된 객체로 다음 epoch를 계속했다. 이는 추가 fit이나 중복 optimizer update가 아니다. 완료 후 BA 최적 checkpoint를 다시 로드한 확률·집계지표가 해당 history와 정확히 같음을 확인했다.

새 ignored 경로에 best.pt/latest.pt, feature order, scaler 메타데이터, candidate/Origin/Model/Seed, 데이터·코드·config·승인 SHA, 환경버전, RNG와 history를 함께 저장한다. resume는 같은 identity/config/data/code의 **완료 epoch 경계**에서만 허용한다. 중간 epoch가 강제 중단되면 마지막 committed epoch 이후 작업을 버리고 그 경계에서 재현한다. 완료된 실험을 새 fit으로 다시 학습하지 않는다. 실제 fit 전체를 별도로 재학습하는 반복은10fit 예산 밖이므로 하지 않았다. 전체 독립 반복 재현을 완료했다고 주장하지 않는다.

실행환경은 STEP2.9 고정 venv, Torch2.10.0+cpu/ncps1.0.1, CPU thread1·deterministic algorithms, 프로세스 시작 전PYTHONHASHSEED2다. 패키지를 업데이트하지 않았다. LTC wrapper의 제약True와 참조 parameter 수도 유지했다.

## 금지 범위와 보존

Test의 종가·정답·확률·성능을 배열화하거나 모델 선택/보고에 사용하지 않았다. 전체 파일 hash/공식 달력의 무결성 메타데이터와 Test 값 분석을 구분했다. 이 단계에서는 Test 내용을 포함하는 기존 전체 회귀검사를 재실행하지 않고 해시를 보존했으며 O1 전용 검사를 사용했다.

원본 Notebook 전체는 실행하지 않았고 검증된 셀6/8의 모델/loss 정의만 재사용했다. 원본 CSV·기존 성능표·JOF V14/V15·main은 보존한다. 공개 파일은 코드·집계·loss curve·해시만이며 가격 시계열·일별Target·확률·checkpoint는 공개하지 않는다. 새 모델의 검증 결과를 과거 박사논문 표에 덮어쓰지 않는다.
''')
 write('STEP3A_NEXT_GATES_KO.md','''# STEP3A 이후 남은 gate와 승인 범위

확인일: 2026-11-16 (Asia/Seoul). 이번 Pilot은 과거 O1 Train/Validation 학습과 저장/복원·구현 진단을 위한 별도 승인이다. 실시간 예측·production-PIT·투자 수익·미래정보 누출 완전 배제·확증적 일반화 성능은 인증하지 않는다.

| 항목 | 현재 판정 | 다음에 필요한 것 |
|---|---|---|
| O1 A/B F1 CPU Pilot | 실제 실행 결과 참조 | 허용된10fit 이외 추가 실행은 별도 승인 |
| 가격 소스/PIT | BOTH_UNVERIFIED / BLOCKED | 공급처·정의·단위·추출/수정·과거vintage·18시 가용성 증빙 |
| A/B 주 자료 선택 | 미선택 | Validation/Test 점수가 아닌 출처 신뢰성·정의·일관성 근거로 사전 결정 |
| Test 평가 | 미승인 | 학습·자료·지표·분석 protocol 확정 후 별도 승인 |
| 전체5Origin/10Seed | 미승인 | 전체 예산·복원 정책·최종 데이터/코드 해시·사전 검정계획 승인 |
| 외부5피처/Ablation | BLOCKED | Foreign_Net 시장/단위/공표, Nasdaq/SOX 공급처 PIT 및 공통 날짜 확보 |
| 수동 레짐 | 기존 Train-only 계획 유지 | 최종 자료로 Train30/70참조 동결; Validation/Test 재계산 금지 |
| HMM fit/레짐 | 미승인 | Train-only fit/선택·명칭, forward filtering·실패보고를 고정한 별도 승인 |
| GPU·LTC τ 분석 | 미승인 | 장치/수치환경 및 실제 시간단위·추출 정의와 추가 실행 승인 |

Validation은 EarlyStopping에 사용한 구현 진단이므로 최종 논문 일반화 성능으로 쓰지 않는다. 단일 클래스 예측·수치 민감도·실패도 있는 그대로 보고하며 이를 보고 seed·날짜·모델 구조·하이퍼파라미터를 바꾸지 않는다. A/B 비교에서 높은 점수를 보이는 후보를 자동 선택하지 않는다.

기존 production training_enabled=false, hmm_fit_enabled=false는 유지했다. 이번 승인은500/3000fit, 전체RO, Test, HMM fit, GPU 또는main 병합 승인으로 확장되지 않는다. 새 연구단계를 원하면 해당 목적·데이터·gate·예산·출력 범위를 별도로 승인해야 한다.
''')
 # Preserve all earlier artifacts, except intentionally updated project README/CHANGELOG.
 before=json.loads(Path('/workspace/work/step3a/before.json').read_text());pres=[]
 for name,old in before.items():
  if name in ['README.md','CHANGELOG.md']:continue
  actual=sha(ROOT/name);pres.append({'file':name,'before_sha256':old,'after_sha256':actual,'status':'PASS' if old==actual else 'FAIL'})
 assert all(x['status']=='PASS' for x in pres),'A prior protected artifact changed'
 (ROOT/'provenance/step3a_preservation.json').write_text(json.dumps({'checked_at_kst':datetime.datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),'all_prior_artifacts_unchanged':True,'artifacts':pres,'production_files_unchanged':True},ensure_ascii=False,indent=2)+'\n')
 for name in ['README.md','CHANGELOG.md']:
  path=ROOT/name;marker='\n## STEP3A / 2026-11-16\n'
  if marker not in path.read_text():
   note=f"\n사용자가 별도로 승인한 회고적 CPU Pilot으로 O1/A-B/F1/Seed2의10 fit을 시작했고 {m['completed_models']}개 완료, {m['failed_models']}개 실패했다. Train2387/Validation228, Train20purge·Validation20UNKNOWN 제외, Test/GPU/HMM/전체RO/Ablation0. 모든 설정과A/B source 미확정·production false gate를 유지했다. loss/Validation 진단·EarlyStopping·checkpoint/RNG 복원 기록을 새 로컬 경로에 보존했다. 원자료·일별Target·확률·모델 가중치는 공개하지 않는다. 집계CSV/곡선·STEP3A 보고서4개와 독립승인·코드/해시만 감사 브랜치에 게시한다.\n"
   path.write_text(path.read_text()+marker+note)
 print('STEP3A reports, curves, preservation written; prior protected artifacts unchanged:',len(pres))
