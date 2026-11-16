# STEP3A 실행 범위·정합성·checkpoint 감사

확인일: 2026-11-16 (Asia/Seoul). 사용자 지시가 승인한 회고적 O1 A/B F1 CPU Pilot만 실행했다. 별도 pilot_execution_enabled와 config/runner/preflight SHA에 연결된 독립 승인 기록을 사용했다. production training_enabled=false/hmm_fit_enabled=false 및 이전 gate는 변경하지 않았다. 출처/PIT 미확정을 Pilot의 명시적 한계로 둔 것이며 production gate를 PASS로 바꾼 것이 아니다.

실행 전12개 gate와 O1 전용10개 사전검사를 통과했다. 전체 source/candidate/Notebook SHA를 보존된 감사와 대조했고 전체3939세션 일치는 이전 전수검증+파일 동일성으로 확인했다. Test 가격을 새로 파싱하지 않기 위해 정확히2714개 과거행만 읽었고 모델 프로세스에는 별도 사본/배열만 전달했다. 원래 전체 가격 파일·첨부 파일과 기존 data 디렉터리는 파일 barrier로 차단했다.

| 항목 | 실제 기간 | 행/표본 수 |
|---|---|---|
| 가격 입력 | 2010-01-04~2020-12-30 | 2714 |
| Train 경계 | 2010-01-04~2019-12-30 | 2466 |
| Train 적격 기준일 | 2010-03-30~2019-11-29 | 2387 |
| Validation 경계 | 2020-01-02~2020-12-30 | 248 |
| Validation 적격 기준일 | 2020-01-02~2020-12-01 | 228 |
| Scaler fit 시점 | 2010-03-03~2019-11-29 | 2406 |

Train purge 20개, Validation 미확정 제외 20개, Train label_end cutoff 위반 0개, Validation 미래 endpoint 위반 0개다. Train 최대label_end=2019-12-30, Validation 최대label_end=2020-12-30다.


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

## 사후 검사 결과

실행 전 gate12개 PASS, O1 전용 사전 unit 검사10개 PASS, 사후검사12개 PASS다. 최적 checkpoint의 Validation 재현10/10, 첫 epoch checkpoint/모든 RNG 복원10/10을 확인했다. 모델 학습 실패·손실 발산은0개다.

사후검사 하네스의 초기 경로 변수명이 unittest의 run 메서드와 겹치는 오류를 발견해 run_directory로 바꿨다. 검사 코드만 수정해 다시 실행했고 모델·데이터·하이퍼파라미터·checkpoint는 바꾸거나 재학습하지 않았다. 검증 요약은 manifests/step3a_verification_summary.json에 기록했다.
