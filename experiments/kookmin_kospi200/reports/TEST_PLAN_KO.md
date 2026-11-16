# STEP2 검증 계획과 현재 상태

확정 기간: **2010-01-01~2025-12-31**. 2026 관측은 모든 분석 입력·피처·학습·검증·테스트·HMM·Rolling-Origin·ablation·LTC 및 타깃 확인에 사용 금지. 원본은 보존하며 파생 데이터에서 먼저 날짜 필터를 적용한다. 모델/HMM 학습·GPU·실제 모델 forward·checkpoint 로드 금지. `training_enabled=false` 유지.

이번 실행은 표준 unittest와 pandas/numpy/scipy/sklearn 데이터·합성 수학 검사만 포함한다. StandardScaler의 합성 Train fit는 정규화 검증이며 모델/HMM 학습이 아니다. bootstrap은 합성100날짜에서 블록별30회로 계산 동작만 검증했다. 실제 연구 추론 설정은20/40/60·10000회·Holm으로 고정돼 있으며 실자료 검정은 실행하지 않았다. LTC는 손으로 구성한 숫자 snapshot만 계산했고 어떤 모델 forward도 하지 않았다.

| 검증 | 이번 결과 | 최종 학습 전 합격 기준 |
|---|---|---|
| 원본 보존 | PASS: 노트북3·CSV5 SHA-256 동일 | 원본·기존 결과·보호경로 변경0 |
| cutoff | PASS: 원천별2010이전/2026 제외수 기록 | 모든 downstream 관측·label_end가 기간 안 |
| 2026 sentinel | PASS: 2026 종가 변경/삭제해도 기간내 자료 동일 | 미국·외국인 포함 전 upstream PIT lineage에도 적용 |
| nullable tail | PASS: 달력 합성20세션 unknown, 파일 tail20개 후보 unknown | 실제 KRX 달력에서 label_end 확정; unknown→0 금지 |
| 실제 달력·가격 | BLOCKED: 외국인 대비 KOSPI 부재 날짜45개 | KRX 공식 세션·가격·누락 대조; 행shift 금지 |
| PIT 구현 | PASS: 미국 DST·주말·조기폐장 합성 schedule | 원천 schedule·실제 공표시각·latency 증빙 |
| 실제 변수 가용성 | BLOCKED: KOSPI·미국·외국인 증빙 없음 | 18:00 계약 충족·단위/시장/개정·max_age 승인 |
| 미래 perturbation | PASS: 미래 값 변경/삭제에 과거 선택 동일 | 실제 데이터 가용성 검증 후 같은 검사 |
| bfill/무제한 ffill | PASS: 코드에 사용 없음; stale/no-prior BLOCKED | 관측 age·출처·available_at·차단 이유 기록 |
| Rolling-Origin/purge | PASS: 합성15구간과 strict label_end 검사 | 실제15구간 경계·확정표본수는 현재 BLOCKED |
| window 계약 | PASS: t포함/t제외 구분, 과거 history 재사용 | 원본참조/수정 config 분리·동등비교 금지 |
| scaler | PASS: Train-only fit·미래값 불변·feature 순서 | 실제 Train feature dates·통계 lineage 저장 |
| 모델·seed·feature | PASS: 설정 및 선언형3000 job 검사 | 실제 모델 런타임 검증은 STEP3 승인 후 |
| 앙상블 | PASS: 같은 Origin/Seed/date만 결합, 누락 시 차단 | LTC RAW/LOG .5:.5, Hybrid .7LNN+.3RNN_RAW |
| HMM causal | PASS: 합성 supplied parameter forward prefix 불변·연속 filtering | 실제 fit 금지; 나중에 Train-only fit lineage 증명 |
| Train 레짐 | PASS: Train 임계값·명칭, test 요청/collapse 차단 | 실제 train state·수렴 기록; test median 대체 금지 |
| 시드 비독립성 | PASS: seed복제 시 시장날짜100개 유지 | 날짜단위 paired 비교; 시드 연결 McNemar 주분석 금지 |
| 통계 | PASS: 블록20/40/60·Holm 합성 계산 | 실자료10000회·고정 family·block감도 전부 보고 |
| LTC 인터페이스 | PASS: snapshot 식·입력/은닉 의존성·단위 미확정 차단 | 실자료는 버전·소스·단위·checkpoint lineage 확인 후 |
| provenance/가공파일 | BLOCKED | 가공파일 생성 코드·기간내 재생성 및 source lineage |
| no-training/no-tuning | PASS: AST 금지 호출·모델 import 없음, 실행 gate false | 실자료 outcome을 보고 config 변경 금지 |

검사 명령(네트워크/모델 불필요):

```bash
python experiments/kookmin_kospi200/tools/step2_preflight.py
python experiments/kookmin_kospi200/tests/test_step2.py
```

`originals/`에 manifest와 동일한 사용자 원본8개가 필요하다. 공개 브랜치에는 원본과 전체 notebook source/diff를 올리지 않는다. `tools/static_audit.py`의 이전 전체기간 재현 runner는 비활성화하고 기존 STEP1 결과는 그대로 보존한다.

KRX 달력 fixture는 **합성 테스트용**으로만 verified이고 실자료 캘린더 인증이 아니다. 실자료 observed dates를 verified=True로 우회하지 않는다. 실제 `rolling_origin_manifest.csv`의 상태는 BLOCKED, 확정 표본 수는 빈칸이다. 날짜필터 후 KOSPI3894행, feature-ready3854행, 유효 label 후보3834개, t포함window 후보3815개는 참고 수치이며 최종 실행 데이터로 사용하지 않는다.

향후 순서: 공식 달력·가격/가용시각 증빙 → 모든 BLOCKED 해소 → manifests 재생성·future perturbation 재검증 → 사양/실행 규모 검토 → 명시적 STEP3 학습 승인 → 모델 smoke/benchmark. 현재 학습을 시작할 수 없다.
