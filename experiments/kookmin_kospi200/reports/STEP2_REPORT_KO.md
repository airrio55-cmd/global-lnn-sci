# STEP2 구현 결과

기준일2026-11-16. 브랜치 `audit/kookmin-kospi200-20261116`, 경로 `experiments/kookmin_kospi200/`.

**코드·설정·정적/합성 검증 준비는 완료했으나 실자료 실행은 BLOCKED다.** 모델 학습0, HMM fit0, GPU0, 실제 모델 forward0, checkpoint 로드0, 실자료 bootstrap0이다. `training_enabled=false`를 유지했다. 원본3노트북·CSV5파일, 기존 결과, main, JOF V14/V15 및 lock는 수정하지 않았다.

## 구현 파일

| 파일 | 변경 내용 |
|---|---|
| configs/experiment_config.json | 확정2010~2025·10학습모델·시드·피처순서·앙상블·6ablation·5origin·HMM·통계·실행차단 |
| configs/original_reproduction_config.json | 원본 t제외 window·AMP·offset·Hybrid 식 참조를 수정 사양과 분리 |
| src/kospi200/data.py | cutoff→검증 KRX 달력 label, nullable target, timezone-aware PIT·검증된 미국 schedule·max_age·lineage·미확정시각 차단 |
| src/kospi200/folds.py | 5개 origin, strict label_end purge, 과거 window 재사용, Train-only StandardScaler/transform |
| src/kospi200/specs.py | RAW/LOG 순서·6사양·seed 검증,3000 선언형 job, 같은origin/seed/date 앙상블 |
| src/kospi200/regimes.py | fit없는 HMM 순방향 계산·연속 history, Train-only 계획·임계값·명칭, collapse 차단 |
| src/kospi200/statistics.py | date별 seed평균 paired moving blocks·20/40/60·10000 고정 wrapper·Holm, seed pooling 차단 |
| src/kospi200/tau.py | 고정 ncps 소스 기준 raw/effective τ, affine/sparsity/softplus, regime/seed/origin 분위·탐색 연관 인터페이스 |
| tools/step2_preflight.py | 원본 무결성·필터 수·candidate label/window·origin 진단; 실제 KRX 인증을 우회하지 않음 |
| tools/static_audit.py | STEP1 전체기간 재현 재실행 차단; 기존 감사 증거는 그대로 보존 |
| tests/test_step2.py | 표준 unittest23개, 데이터·합성 숫자/소스 정적검사만 실행 |
| manifests/data_cutoff_manifest.json | 원천별 필터 수·해시·미확정20개·KRX 미검증·availability 차단 상태 |
| manifests/rolling_origin_manifest.csv | 15구간의 observed 경계·candidate purge/표본·BLOCKED·확정수 빈칸 |
| manifests/step2_test_results.json | 23PASS/0FAIL의 기계판독 결과 |
| manifests/data_lineage.csv, lineage_schema.json | 실제 공표시각 없음이 표시된 source ledger와 per-sample lineage schema |
| manifests/step2_preflight_gates.json | 실제데이터 BLOCKED7개와 검사 결과를 구분 |
| requirements-step2.txt | 이번 데이터·합성 검사 환경 버전 기록; 모델 패키지 설치 안함 |
| reports/PROTOCOL_KO.md, TEST_PLAN_KO.md | 확정 종료일·STEP2 구현·검증 상태 반영 |
| reports/STEP2_REPORT_KO.md, STEP2_PREFLIGHT_KO.md, STEP2_BLOCKERS_KO.md | 이번 변경·결과·미해결 증빙 |
| README.md, CHANGELOG.md, configs/proposed.json | 신규 진입점·승인/미승인 구분·원본 사양 차이·이전설정 superseded |

## 필터링과 표본 수

| 파일 | 필터 전 | 2010이전 제외 | 2026이후 제외 | 기간내 |
|---|---:|---:|---:|---:|
| KOSPI_200.csv | 3935 | 0 | 41 | 3894 |
| Foreigner_Net.csv | 5000 | 1020 | 41 | 3939 |
| Nasdaq.csv | 4067 | 0 | 43 | 4024 |
| SOX.csv | 4067 | 0 | 43 | 4024 |
| processed_regression_data.csv | 3854 | 0 | 0 | 3854 |

원본 파일을 수정하거나 저장해 덮어쓰지 않았다. 해시·제외수 확인을 위해 원본을 읽는 것은 허용된 무결성 감사이며, 실제 feature/target 후보는 필터 후 자료에서만 계산한다. 가공파일은 기본 입력에서 제외하며 기간내 Target_Ret20 재계산 일치는 확인했으나 실제20KRX세션·PIT 증명은 아니다.

파일상 마지막 KOSPI 종가는2025-12-30. 관측행 기준 마지막 유효 예측 기준일 후보는 **2025-12-01**, label_end 후보는 **2025-12-30**이다. **2025-12-02~12-30의 마지막20개는 unknown이며 평가 제외**한다. 2026 종가로 이를 확정하지 않는다.

필터 후3894행에서 feature warmup40행을 제외하면3854행, 확정 endpoint가 있는 feature-ready 후보는3834개, t포함20window까지 요구하면3815개다. 원본 t제외 입력은3814개 후보이며 같은 조건이라고 주장하지 않는다. 이들은 관측행 진단 수치다. **KRX 공식 달력과 PIT 가용성 미확정 때문에 최종 실험 표본 수는 null이다.**

외국인 파일에 있고 KOSPI에 없는 날짜45개는 manifest에 기록했다. 이들을 모두 실제KRX누락이라고 임의 확정하거나 외국인 날짜를 공식달력으로 대체하지 않았다. 실제 KRX 달력/확정 종가 대조 후 endpoint·rolling·origin·표본 수를 다시 확정해야 한다. 관측행 기반 진단상 각 origin의 train/validation20개씩 purge되지만 실제 달력 기준 최종 purge 수는 아직 BLOCKED다.

## 검증 결과와 제한

독립 테스트23개 PASS, FAIL0. 원본해시, cutoff·2026 sentinel, nullable tail·실제 달력축 synthetic endpoint, timezone/DST/조기폐장, 미래 perturbation, stale/no-prior 차단, 미확정 외국인 metadata 차단,15개 fold·purge, window, Train-only scaler, config/feature/seed, keyed ensemble, HMM forward causality, Train reference·collapse, seed 표본 증가 방지, bootstrap/Holm, τ synthetic algebra, 금지 import/호출·gate를 확인했다.

이 PASS는 **구현의 합성·정적 검증**이다. 실제 입력 provenance·전체 KRX 달력·미국/외국인 공표시각·runtime단위에는 BLOCKED7개가 남는다. 실자료 per-sample 입력 lineage를 꾸며내지 않았고 source ledger만 생성했다. HMM 파라미터는 synthetic 숫자만 사용했으며 fit은 하지 않았다. LTC도 실제 모델·checkpoint를 사용하지 않았다. bootstrap 검사는 합성자료30replicate로 동작만 확인했고 연구용10000회는 미실행이다.

## STEP3 진입 판단

**학습을 포함하는 STEP3 시작 불가.** 필수 BLOCKED 해소, 실제달력·공표시각 manifest 재생성, 동일 future-perturbation 검사 통과와 별도 실행 승인 후 가능하다. 구현 검토·증빙 수집은 계속할 수 있다. 예상 전체 규모는 기본500 neural fit,6사양 총3000 fit이며 이번에 실행한 선언형 job 생성은 모델 실행이 아니다. 결과 기반 튜닝·실자료 성능/p값 재생성·main 병합은 하지 않았다.

이번 보고서는 commit 자체에 포함되므로 자기 commit SHA를 파일 안에 넣지 않는다. 최종 대화 보고와 GitHub commit 기록에서 새 SHA를 제공한다.
