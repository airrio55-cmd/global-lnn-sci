# STEP2.9 준비도와 본실험 시작 전 체크리스트

확인일: 2026-11-16 (Asia/Seoul).

- 독립 합성 CPU Smoke: **PASS**, 5모델·70개 판정·optimizer update10회.
- 기존90개 회귀검사: **90 PASS /0 FAIL**.
- 새 제어·증거 검사: **13 PASS /0 FAIL**. 합성 모델을 다시 학습하지 않고 기록·gate·승인 재사용 차단을 검사했다.
- 국내 F1 **실자료 실행은 BLOCKED**. 가격 선택과18시 가용성은 미해결이며 이번 승인은 실자료용이 아니다.
- 전체5피처·전체Ablation·GPU·HMM fit·실제 Test 접근은 계속 미승인/BLOCKED다.

원본 Notebook/CSV·가격 후보·이전 보고서/코드/manifest·기존 성능표 등 **158개 기존 산출물 해시가 동일**하다. 이전 production config와 STEP2.8 실자료 runner/gate는 변경하지 않았다. 이번 결과는 해당2피처·CPU·한batch lifecycle의 실제 호환성 증거로 활용할 수 있으나, 기존 gate를 자동으로 PASS로 올리지는 않았다.

## 본실험 사양 유지

Origins O1~O5와 Seeds[2,12,22,32,42,52,62,72,82,92], 원본 아키텍처별 RAW/LOG offset과 공통 hyperparameter를 유지한다. 합성 검사에서는5개의 공통2피처 사례만 실행했으며 RAW/LOG 별도 실험이나500fit Rolling-Origin을 실행하지 않았다.

본실험 시작 전 체크리스트는 다음과 같다. PASS는 해당 코드/기존 데이터 감사/합성 구조 검사 범위를 뜻하며 최종 가격/PIT 인증으로 확대하지 않는다.

| 항목 | 상태 | 필요 증거 또는 범위 |
|---|---|---|
| 가격 소스 선택·출처 | BLOCKED | Select A/B before real training based on verified supplier/definition/revision evidence; both currently unverified |
| 예측 의사결정시각 | BLOCKED | Existing t18:00 KST include_t proposal unchanged; explicit approval/evidence or new separately approved contract needed |
| 국내 입력 가용성 | BLOCKED | Supplier-specific historical available_at, initial/corrected vintage and collection latency for domestic Close |
| 공식 KRX 달력 | PASS | 3939 official sessions; existing calendar source/hash and regression unchanged |
| 20세션 레이블 | PASS | Candidate diagnostics3919 known/20UNKNOWN; no2026 targets; selected-source finalization pending |
| Label purging | PASS | Train label_end<Validation start; Validation label_end<Test start; existing regressions |
| Train-only scaler | PASS | Existing diagnostic Train-only fit/lineage and perturbation; final-source lineage must be frozen |
| Train-only 수동 임계값 | PASS | Train30/70 quantiles and one-class null rules implemented; freeze selected-source references before real execution |
| HMM 실제 fit/filtering | BLOCKED | Plan fixed; actual HMM fit not authorized/executed. Future fit Train-only, forward posterior continuity, fixed Train names, no fallback |
| 5Origin/10Seed 고정 | PASS | O1-O5; ten fixed seeds and unchanged architecture/channel offsets; no origin/seed selection from Test |
| 2피처 CPU 합성 호환성 | PASS | Five models synthetic constructor/forward/backward/checkpoint/repro passed in pinned candidate environment only |
| RAW5피처 실행 검증 | BLOCKED | Static parameter counts only; runtime verification not authorized |
| 실자료 저장·재개 | BLOCKED | Synthetic state/optimizer/scheduler restoration PASS; full real-data early-stop/epoch/batch/scaler/lineage/RNG/DataLoader resumption not executed |
| 통계검정 사양 | PASS | Protocol: date-paired moving-block20/40/60,10000replicates,Holm; no seed-concatenated McNemar; real-data inference not executed |
| 데이터·코드 해시 | PASS | Prior hashes preserved; synthetic config/source/runner/checkpoint hashes recorded; freeze final source/code before real experiment |
| 전체5피처 외부 PIT | BLOCKED | Foreign_Net scope/unit/release and Nasdaq/SOX supplier-PIT remain unresolved |
| 실자료 별도 실행 승인 | BLOCKED | Synthetic-only authorization does not permit STEP3 financial-data training, Test access, HMM fit, GPU, Rolling-Origin or Ablation |


## 결과 저장과 재개

이번 합성 checkpoint의 model/optimizer/scheduler와 Torch RNG 저장·복원 및 logits 동일성은 PASS다. 실자료의 전체epoch 재개는 별도 검증이 필요하다. 향후 checkpoint에는 early stopping 상태, epoch/batch 위치, scaler와 feature순서, Origin/Seed, 가격 후보·데이터·코드 SHA-256, label_end cutoff, Train 레짐 임계값, Python/NumPy/Torch/DataLoader RNG 및 환경 버전을 함께 저장해야 한다. 합성 한-step 복원을 전체 학습 resume 완료라고 표시하지 않는다.

통계 사양은 날짜 기준 paired moving-block bootstrap20/40/60·10000반복·Holm이다. seed 연결 McNemar를 주 분석으로 사용하지 않고 실자료 p값을 생성하지 않았다. HMM은 향후 Train-only fit·Train-only 후보 선택·상태 명칭·Validation/Test forward filtering을 유지하며 별도 승인 없이는 fit하지 않는다.

## 추가 사용자 결정·증빙

1. 공급처·정의·개정 증거를 확보한 가격 A/B 선택과 고정 처리 원칙. 둘 다 미확인이므로 이번에는 선택하지 않았다.
2. t18:00·t포함 입력에 대한 실제 공급처의 과거 available_at/vintage/수집지연 증빙. 계약 변경을 원하면 별도 config와 명시적 승인이 필요하다.
3. 실자료용 최종 데이터·프로토콜·환경 해시를 확정한 뒤 **별도의 실자료 실행 범위 승인**. 이번 합성 승인 기록은 사용할 수 없다.
4. 전체5피처를 진행하려면 Foreign_Net의시장/단위/공표와 Nasdaq/SOX 공급처 PIT 및5피처 실행 검증이 추가로 필요하다.

공개 산출물은 코드·검증 요약·해시만 포함한다. 모든 checkpoint와 합성 배열은 새로운 ignored 디렉터리에 남겼다. main 병합이나JOF V14/V15·잠금 파일 변경은 하지 않는다.
