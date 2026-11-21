# STEP11 논문 보완 우선순위

확인일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. 

이번 STEP11은 기존 문서·정적 코드·저장된 감사 결과를 읽는 보완 감사다. 금융 fit/forward/새 평가·HMM 실행·τ 계측·bootstrap draw·신규 p값/CI는 모두 **0**이다. 기존 보고서·결과·설정은 수정하지 않으며 master 실행 flags=false를 유지한다. 연구기간 2010-01-01~2025-12-31과 2026 시장 관측 사용 금지를 유지한다. JOF 다국가 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, 주 분석 가격 **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, STEP9B1R **METHOD_NOT_VALIDATED**를 유지한다. 파일 무결성·코드 계약 확인을 공급처 인증·PIT·통계적 타당성 인증으로 해석하지 않는다. 아래 판정은 해당 증거 범위에 한정된다.

## 해결 수단별 우선순위

| 우선순위·범주 | 남은 문제 | 해결조건·담당 증거 | 논문 영향 |
| --- | --- | --- | --- |
| P0 A: 기존 아카이브 | CfC 서술/LTC 코드, loss/BA early stopping, HMM 서술 불일치 | STEP10C의 문단·활성 코드 근거로 원고 정정안과 버전 대응 작성; 원고 승인 별도 | 실제 모델을 잘못 명명하는 핵심 오류 방지 |
| P0 A: 기존 아카이브 | RQ·표·통계 주장 과장 | STEP11 등급과 Primary 비유의/Secondary 반대 증거를 함께 고지 | 신규 계산 없이 논증 범위를 정합화 |
| P0 B: 사용자 원본 | Word 수정 대표Seed/비중첩 McNemar의 실행 버전 부족 | 수정 script·출력·원예측·실행환경·hash 연결을 비공개 확보 | 보고됐다는 사실과 독립 확인을 구별 |
| P0 B/C: 사용자/공급처 | A/B 최초 입수·코드·단위·개정·이용권한 | STEP10A R01~R10 다운로드/계약/로그 원본 확보 | 가격 정체성·학술 이용조건 판단; Test로 선택 금지 |
| P0 C: 공급처 | historical18KST 공개·수신/vintage | 제품별 역사적 배포·receipt·revision 증거와 행별 연결 | 실시간 가능성 주장은 계속 차단 |
| P1 D: 방법론 | METHOD_NOT_VALIDATED | 추정대상·의존성·가족·calibration 기준을 사전 검토 | 확증적 p/CI 주장 유보; 추가 검정 자동 필수 아님 |
| 조건부 E: 신규 실험 | 실제 가격/endpoint/입력 vintage 변경 | 먼저 변화 영향·의존 산출물 범위 감사, 별도 사양·예산·승인 | 달라진 데이터를 쓴 결과는 새 version; 자동500재학습 아님 |
| 조건부 E: 신규 실험 | 원형 Ensemble 추가효과를 핵심 주장 | 외부 RAW5 PIT·공통 계약 동결 후 bridge 별도 승인 | 현재 F1 기술적 방향에는 자동 필수 아님 |
| 조건부 E: 신규 실험 | 확증적 미래 일반화 | 독립 사전등록 평가·검증된 추론 방법·새 기간 별도 승인 | 현재 Test를 재명명해 해결할 수 없음 |
| F: 현재 설계에서 불가 | 과거 로그 소실 시 당시 receipt/vintage 완전 인증 | 복구 가능한 독립 원기록이 없으면 UNKNOWN 유지 | 역사적 인증 불가를 한계로 명시 |
| F: 현재 설계에서 불가 | τ 인과효과/이미 노출된 Test의 최초 독립성 | 현재 관측 설계로 식별 불가 | 인과·최초 확증 표현 삭제; 후속 설계는 별도 연구 |

## 신규 실험 없이 먼저 할 일

우선 모델 정체성·원고와 코드의 선택 기준·HMM/시간 정렬 서술을 바로잡는 정정안을 제시하고, 핵심 RQ를 동결 결과가 지지하는 범위로 좁힌다. 원고·초기 Notebook·최신 F1을 별도 버전으로 인용한다. STEP10B 당시 DOCX 부재 기록은 수정하지 않고 STEP10C 확보 사실을 연결한다. 표6 SD 차이는 저장4자리 SD를3자리 표시 반올림한 패턴과 호환된다는 수준으로 기록하며 실제 편집 로그를 확보했다고 쓰지 않는다.

이후 원본 증빙·수정 통계 실행 아카이브를 수집한다. 원자료가 같고 출처 설명·문구만 보완된다면 재학습이 필요하지 않을 수 있다. 가격·label·window·scaler·mask가 달라지면 영향 범위를 먼저 명시하고 새 결과가 필요한 주장만 대상으로 별도 승인을 요청한다. 라이선스 문제 자체를 수치 재실험으로 해결하지 않는다.

## 지도교수에게 우선 보고할 위험과 조치

1. 원고 CfC와 실제 LTC가 다르다. 핵심 모델명·제목·방법 절부터 정합화한다.
2. 가격은 사용자 제공 최종 시계열이며 공급처/PIT 인증이 아니다. A/B 병렬 유지와 출처·vintage 한계 문구를 확정한다.
3. Primary BA 유의 우월성은 미확립이고 baseline 유의성은 미검정이다. 통계적 우월성 표현을 낮춘다.
4. LTC24/100 단일클래스 및 τ 연관은 관측 진단의 기여로 활용하되 인과·투자효과를 주장하지 않는다.
5. 원형 Ensemble 중심 제목을 유지할지 최신 F1 진단 방향으로 바꿀지 학문적 목적을 먼저 정한다. 성능이 높은 후보를 이유로 선택하지 않는다.

STEP10C 권고 방향A를 유지한다. 방향B의 추가효과 주장을 고수하면 bridge가 조건부 필요하나 출처·외부변수·버전 증거 확보 및 별도 실행 승인 전에는 BLOCKED_PENDING_EVIDENCE다. 이 보고서는 원고 자체를 수정하거나 새 금융 실험을 승인하지 않는다.

## 공통 근거와 확인 한계

우선 근거: [STEP10_MASTER_AUDIT_KO.md](STEP10_MASTER_AUDIT_KO.md), [STEP10_DATA_PIT_GAP_AUDIT_KO.md](STEP10_DATA_PIT_GAP_AUDIT_KO.md), [STEP10_STATISTICAL_EVIDENCE_KO.md](STEP10_STATISTICAL_EVIDENCE_KO.md), [STEP10A_PRICE_PROVENANCE_AUDIT_KO.md](STEP10A_PRICE_PROVENANCE_AUDIT_KO.md), [STEP10A_HISTORICAL_PIT_AUDIT_KO.md](STEP10A_HISTORICAL_PIT_AUDIT_KO.md), [STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md](STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md), [STEP10B_MASTER_COMPARISON_KO.md](STEP10B_MASTER_COMPARISON_KO.md), [STEP10C_FINAL_RECOMMENDATION_KO.md](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP10C_STATISTICAL_RECONCILIATION_KO.md](STEP10C_STATISTICAL_RECONCILIATION_KO.md).

STEP11 확인일은 위와 같다. 기존 외부 조회의 확인일·접근 제한은 STEP10A 및 provenance 원기록을 따른다. 이번에는 외부 가격·새 공급처 인증 자료를 수집하지 않았다. 기존 문서의 주장과 외부 원자료로 입증된 사실을 분리하며, 새 금융 결과를 산출하지 않았다.
