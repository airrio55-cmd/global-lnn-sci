# STEP10 한계와 독창성 후보

확인일: 2026-11-20 KST

이번 STEP10은 기존 저장 결과의 읽기 전용 감사와 논문 집필용 동결이다. 새 금융 fit / checkpoint load·forward / bootstrap draw / p값 / CI / Test 예측·성능 재계산 / HMM refit·refilter / LTC τ 계측 / Ensemble / GPU / 외부 금융 수집 / 2026 시장 관측 사용은 모두 0이다. master training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지했다.

가격 A/B는 BOTH_UNVERIFIED, 주 분석 가격은 PENDING, historical 18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 재현성 snapshot의 PASS와 원천·PIT·통계적 타당성의 PASS는 서로 다르다. 기존 파일을 수정하지 않고 신규 STEP10 자료만 작성한다. 단일 복구 τ를 역산할 수 있는 새100개 정량집계·차이·분할값은 공개하지 않는다.

| 기여 후보 | 동결 근거 | 지원되는 범위 | 함께 제시할 한계 |
| --- | --- | --- | --- |
| 동일 날짜 기반 NN–baseline 비교 | STEP8BR Test40 및 NN 저장500 | 평가일·Target 정렬과 반대 지표 보고 | 정보이력 차이 및 통계검정 미실시 |
| Seed/Origin 안정성 평가 | STEP4D/5B | 초기화·시기별 변동과 실패를 전수 보존 | Seed는 독립 시장 반복 아님 |
| LTC 퇴화 진단 | STEP5B model_instability | LTC24/100, LSTM2/100 등 다른 모델도 병기 | 한클래스 예측과 수치발산 구분 |
| 레짐과 성능 연결 | STEP6B | Train-only 경계와 forward filtering, support/null 공개 원칙 | 시장 상태의 인과효과 아님 |
| 전도도 기반 τ 분석 | STEP7A/7B/7BR | 원시·유효τ/observation/substep 구분, 99+1 이력 | model step·구성독립효과 미식별 |
| 실패·복구·추론 한계의 재현성 | STEP8B→8BR, STEP7B→7BR, STEP9B1R | 실패를 덮어쓰지 않는 버전·SHA·차단 정책 | SHA로 데이터 출처/PIT를 인증할 수 없음 |

독창성은 관련 문헌 및 지도교수 검토를 전제로 한 후보다. “500회 학습 자체가 최초·독창적”, “LNN이 최고”, “τ가 퇴화 원인”, “실시간 수익성 검증”으로 쓰지 않는다. 결과가 지지하는 것은 통합 진단 설계와 반대 증거·실패까지 보존하는 재현성이다.

교수 검토용 강점3개: (1) NN·단순 기준모형의 동일 평가일 비교와 지표별 반대 증거를 함께 제시, (2) Seed/Origin·단일클래스·레짐·LTC conductance를 연결한 진단, (3) 실패·복구·추론 미검증을 삭제하지 않는 동결 lineage.

핵심 한계3개: (1) 가격 출처와 historical18시 가용성 미확정, (2) 역사적 Test 노출·중첩 label·반복 Seed의 의존성 및 입력이력 차이, (3) 근사검정 타당성 미검증·baseline 검정 미실시·τ 구성독립/인과효과 미식별.

추가 제출자료: 공급처·다운로드/추출 로그·지수코드/단위·조정/개정정책·최초 배포와 수신시각 로그, 외국인 자료 정의와 공표 증빙, 미국지수 과거 세션/latency 증빙. 논문 집필은 서술·탐색적 범위를 명시하면 착수 가능하나, 실시간/확증/인과 연구로 인증된 것은 아니다.

