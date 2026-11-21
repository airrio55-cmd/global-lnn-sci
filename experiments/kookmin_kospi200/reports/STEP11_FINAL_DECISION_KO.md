# STEP11 최종 판단 및 여덟 질문

확인일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. 

이번 STEP11은 기존 문서·정적 코드·저장된 감사 결과를 읽는 보완 감사다. 금융 fit/forward/새 평가·HMM 실행·τ 계측·bootstrap draw·신규 p값/CI는 모두 **0**이다. 기존 보고서·결과·설정은 수정하지 않으며 master 실행 flags=false를 유지한다. 연구기간 2010-01-01~2025-12-31과 2026 시장 관측 사용 금지를 유지한다. JOF 다국가 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, 주 분석 가격 **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, STEP9B1R **METHOD_NOT_VALIDATED**를 유지한다. 파일 무결성·코드 계약 확인을 공급처 인증·PIT·통계적 타당성 인증으로 해석하지 않는다. 아래 판정은 해당 증거 범위에 한정된다.

## 결론

현재 근거는 **조건부 회고적·기술적·탐색적 논문 집필**을 뒷받침한다. 데이터 공식 인증·historical PIT·확증적 우월성·투자성과 인증은 차단 상태다. 이것은 학위 심사 통과나 원자료 이용권한을 보증하는 판정이 아니다. 제목·RQ·기여의 범위는 지도교수와 최종 결정해야 한다.

| 질문 | 확인된 사실·판단 | 미확인/필요 조치 |
| --- | --- | --- |
| 1. 현재 데이터는 학위논문에 사용 가능한가? | 사용자 제공 최종 시계열에 조건부인 회고적 탐색 연구로는 활용 가능 | 이용권한·출처 한계 고지 및 교수 검토 필요; 공식/PIT 인증 연구로는 불가 |
| 2. A/B에 부족한 증거는? | 파일 내부 연결과 교차대조는 존재 | 공급처→최초 파일 연결, 다운로드/제품 정의/개정 정책, 충돌2일 원인, 학술 이용권한 |
| 3. historical PIT 검증 방법은? | 역사적 배포·수신·적재·vintage archive가 있으면 세션별 cutoff와 연결 가능 | 현재 파일/현행 일정만으로 불가; 로그 소실 시 UNKNOWN 유지 |
| 4. 기존 검정은 어디까지 주장 가능한가? | 동결 근사절차에서 Primary/Origin BA 미기각, 일부 Secondary 신호라는 기존 사실 | 유효 명목 오류율·동등성·전반 우월성 인증 불가; baseline 통계 우월성 NOT_TESTED |
| 5. 추가 통계검정이 꼭 필요한가? | 기술·탐색적 RQ 집필에는 자동 필수 아님 | 확증적 비교를 핵심 주장하려면 별도 추정대상·검증된 방법·사전 계획/승인이 필요; p값 추가가 출처 문제를 해결하지 않음 |
| 6. LTC 퇴화·τ가 주요 기여가 가능한가? | 24/100 단일클래스 진단과 τ의 구성효과를 고려한 탐색적 연관은 기여 후보 | 인과 메커니즘·일반적 고장률·경제적 기억·수익성으로 확대 불가 |
| 7. 신규 실험 없이 가장 중요한 해결은? | 문서–코드 모델 정체성/선택 기준 정합, RQ·주장 수준 정정, 원 증빙/수정 실행 아카이브 연결 | 자료가 실제 달라질 때만 영향 감사 후 필요한 범위의 별도 실험 검토 |
| 8. 교수에게 먼저 보고할 위험/조치는? | CfC/LTC 충돌, 가격/PIT 미인증, Primary 비유의/방법 미검증을 먼저 고지 | 최신 F1 진단 중심 방향A와 원형 Ensemble 방향B의 주장 차이를 정하고 제목·핵심기여를 정합화 |

## 실행 준비도

문서 보완과 증거 요청은 진행 가능하다. 금융학습/추론/추가 검정 실행 준비도는 이번 감사로 PASS가 되지 않는다. STEP9B1R METHOD_NOT_VALIDATED, 가격 BOTH_UNVERIFIED/primary PENDING, production-PIT BLOCKED를 유지한다. 최초 독립 Test라는 주장은 이미 노출된 자료에서 복구할 수 없다.

기존 결과와 반대 증거·실패·복구 이력을 보존한다. HMM 선택10은100후보의 일부이며 τ100은99+독립복구1의 versioned 결과다. 새로운 학습·평가·draw·p값·CI는0이다. 새 미래기간·2026 자료 수집도 승인하지 않는다. 후속 연구는 증거 확보와 사양·예산·별도 승인 이후에만 검토한다.

## 공통 근거와 확인 한계

우선 근거: [STEP10_MASTER_AUDIT_KO.md](STEP10_MASTER_AUDIT_KO.md), [STEP10_DATA_PIT_GAP_AUDIT_KO.md](STEP10_DATA_PIT_GAP_AUDIT_KO.md), [STEP10_STATISTICAL_EVIDENCE_KO.md](STEP10_STATISTICAL_EVIDENCE_KO.md), [STEP10A_PRICE_PROVENANCE_AUDIT_KO.md](STEP10A_PRICE_PROVENANCE_AUDIT_KO.md), [STEP10A_HISTORICAL_PIT_AUDIT_KO.md](STEP10A_HISTORICAL_PIT_AUDIT_KO.md), [STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md](STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md), [STEP10B_MASTER_COMPARISON_KO.md](STEP10B_MASTER_COMPARISON_KO.md), [STEP10C_FINAL_RECOMMENDATION_KO.md](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP10C_STATISTICAL_RECONCILIATION_KO.md](STEP10C_STATISTICAL_RECONCILIATION_KO.md).

STEP11 확인일은 위와 같다. 기존 외부 조회의 확인일·접근 제한은 STEP10A 및 provenance 원기록을 따른다. 이번에는 외부 가격·새 공급처 인증 자료를 수집하지 않았다. 기존 문서의 주장과 외부 원자료로 입증된 사실을 분리하며, 새 금융 결과를 산출하지 않았다.
