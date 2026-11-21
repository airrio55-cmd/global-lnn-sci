# STEP11 읽기 전용 실행·보존 감사

확인일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. 

이번 STEP11은 기존 문서·정적 코드·저장된 감사 결과를 읽는 보완 감사다. 금융 fit/forward/새 평가·HMM 실행·τ 계측·bootstrap draw·신규 p값/CI는 모두 **0**이다. 기존 보고서·결과·설정은 수정하지 않으며 master 실행 flags=false를 유지한다. 연구기간 2010-01-01~2025-12-31과 2026 시장 관측 사용 금지를 유지한다. JOF 다국가 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, 주 분석 가격 **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, STEP9B1R **METHOD_NOT_VALIDATED**를 유지한다. 파일 무결성·코드 계약 확인을 공급처 인증·PIT·통계적 타당성 인증으로 해석하지 않는다. 아래 판정은 해당 증거 범위에 한정된다.

## 수행 범위

우선9개 문서와 STEP25~29·STEP10A/B/C·STEP5C·STEP9B1R 등 관련 보고서, 기존 manifest 및 정적 계약 소스를 읽었다. 저장 STEP5C600행의 행 수·고유 가설 identity와 기존 family 요약, STEP9B1R 추천 방법 없음/9설정 핵심 기준 미충족을 확인했다. 저장 수치의 재인용과 새 p값/CI 계산을 구분했다. 원 가격 시계열을 수치 배열로 읽거나 금융 실행 모듈을 import하지 않았다.

고정 master config SHA-256은 `f4ea7a18d7812b00b8c581191a110f63a6799a22e066484ec251ee32f7912c5c`다. 기존 STEP10C 공개 commit은 `93636e508d7e07e3117d81b2bb119b439b207593`다. SHA 검사는 정적 파일 무결성 확인에 한정한다.

## 보존 및 공개 검사

시작 snapshot은 기존 project **10106개 파일**이다. 전체 byte SHA를 다시 비교해 **기존 파일 변경/삭제0**을 확인했다. 검증 결과는 외부 로컬 로그에 보존한다. 새 project 경로는 요청한 STEP11 보고서9개로 제한한다. 비공개 inventory·검사 로그·staging metadata는 project 외부 로컬에 보존하고 게시하지 않는다.

| 검사 | 요구·판정 범위 |
| --- | --- |
| 우선9보고서 존재·읽기 | PASS |
| 기존600행·고유 identity600 | PASS; 새 p/CI 계산 아님 |
| METHOD_NOT_VALIDATED 유지 | PASS; 과학적 방법 승인 상태는 BLOCKED |
| master SHA·false flags 보존 | PASS; 기존 byte snapshot 비교 포함 |
| 기존 NN500/Test500/Baseline40/HMM100선택10/τ100 보존 | PASS: 전체 기존파일 SHA 일치; 재실행0 |
| 새 금융 fit/forward/평가·HMM·τ | 0 |
| 새 bootstrap draw·p값·CI | 0 |
| 새로운 시장자료·2026 관측 사용 | 0 |
| 공개 범위 | PASS: 신규9개 보고서만; 원자료·개별결과·private 설정 제외 |

공급처 인증·historical PIT·확증 방법의 미해결은 문서 작성 검사 PASS와 별개다. 신규 금융 실행 예산은0이며 후속 실험을 자동 시작하지 않는다.

정적·보존·공개 범위 검사 **29개 PASS / FAIL0**을 확인했다. 이는 새 금융 테스트나 기존 방법론의 타당성 PASS가 아니다. 데이터 공급처 UNKNOWN, historical PIT BLOCKED, 통계 방법 METHOD_NOT_VALIDATED는 그대로다.

## Git 반영 계약

원격 audit head를 재확인하고 expected_sha로 보호해 신규 보고서9개만 commit/push한다. main의 시작 SHA와 종료 SHA, commit 변경경로9개를 확인한다. 원본 Notebook/CSV·논문 원문·기존 보고서·JOF는 변경하지 않는다. commit SHA와 원격 반영 결과는 최종 응답과 외부 로컬 영수증에 기록해 자기참조 SHA 문제를 피한다.

공개본은 증거 수준·방법 제안·다중 fit 집계 사실만 포함한다. 개별 가격·Target·확률·weights·checkpoint·실제 Train threshold·class support·비공개 경로·운영 설정을 게시하지 않는다. 복구된 단일 τ를 역산할 새로운 정량 집계도 없다.

## 공통 근거와 확인 한계

우선 근거: [STEP10_MASTER_AUDIT_KO.md](STEP10_MASTER_AUDIT_KO.md), [STEP10_DATA_PIT_GAP_AUDIT_KO.md](STEP10_DATA_PIT_GAP_AUDIT_KO.md), [STEP10_STATISTICAL_EVIDENCE_KO.md](STEP10_STATISTICAL_EVIDENCE_KO.md), [STEP10A_PRICE_PROVENANCE_AUDIT_KO.md](STEP10A_PRICE_PROVENANCE_AUDIT_KO.md), [STEP10A_HISTORICAL_PIT_AUDIT_KO.md](STEP10A_HISTORICAL_PIT_AUDIT_KO.md), [STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md](STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md), [STEP10B_MASTER_COMPARISON_KO.md](STEP10B_MASTER_COMPARISON_KO.md), [STEP10C_FINAL_RECOMMENDATION_KO.md](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP10C_STATISTICAL_RECONCILIATION_KO.md](STEP10C_STATISTICAL_RECONCILIATION_KO.md).

STEP11 확인일은 위와 같다. 기존 외부 조회의 확인일·접근 제한은 STEP10A 및 provenance 원기록을 따른다. 이번에는 외부 가격·새 공급처 인증 자료를 수집하지 않았다. 기존 문서의 주장과 외부 원자료로 입증된 사실을 분리하며, 새 금융 결과를 산출하지 않았다.
