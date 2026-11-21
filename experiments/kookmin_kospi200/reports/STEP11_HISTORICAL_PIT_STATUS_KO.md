# STEP11 historical18KST PIT 상태

확인일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci` / `audit/kookmin-kospi200-20261116` / `experiments/kookmin_kospi200/`. 

이번 STEP11은 기존 문서·정적 코드·저장된 감사 결과를 읽는 보완 감사다. 금융 fit/forward/새 평가·HMM 실행·τ 계측·bootstrap draw·신규 p값/CI는 모두 **0**이다. 기존 보고서·결과·설정은 수정하지 않으며 master 실행 flags=false를 유지한다. 연구기간 2010-01-01~2025-12-31과 2026 시장 관측 사용 금지를 유지한다. JOF 다국가 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, 주 분석 가격 **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, STEP9B1R **METHOD_NOT_VALIDATED**를 유지한다. 파일 무결성·코드 계약 확인을 공급처 인증·PIT·통계적 타당성 인증으로 해석하지 않는다. 아래 판정은 해당 증거 범위에 한정된다.

## 예측 시각과 필요한 vintage

예측시각은 한국 거래일 t의 **18:00 Asia/Seoul**이다. F1의 실제 입력은 `[Log_Ret, Disparity]`이며 Vol_Regime은 공통 적격 마스크·레짐용 보조 변수다. `src/kospi200/data.py`의 local_features 정의는 다음과 같다.

- Log_Ret = log(Close[t] / Close[t-1]).
- Disparity = Close[t] / mean(Close[t-19:t]) − 1.
- Vol_Regime = Log_Ret.rolling(40).std(ddof=1).

입력 window는 t-19~t다. F1 window에 필요한 종가 이력은 최장 t-38~t이며, 공통 Vol_Regime 적격 마스크의 window 이력은 더 길다. 당일 t 종가만 확인하면 충분한 것이 아니다. 계산에 필요한 과거 종가도 당시 이용 가능한 vintage여야 한다.

| 단계 | 확인 범위 | 판정 | 부족한 증거 |
| --- | --- | --- | --- |
| 거래 세션/종가 산출 | 세션 정렬과 일별 종가라는 정의 | PARTIALLY_VERIFIED | 시기별 장 종료·특수 세션·지수 최종 산출 규칙 |
| 지수 최초 배포 | 현행 상품 일정에 관한 기존 기록 존재 | UNKNOWN (historical 계약) | 2010~2025 해당 제품의 최초 배포 및 수정 배포 기록 |
| 공급처 공개·수신 | A/B 공급처 자체 미확정 | UNKNOWN | 공급처별 공개·수신·수집시각과 timezone/시계 동기화 |
| 과거 revision | 현재 최종 시계열만 확보 | UNKNOWN | as-of archive와 revision 식별자·effective time |
| 피처 생성 완료 | 정적 계산식·과거 window | VERIFIED (계산 계약) | 실제 과거 입력 준비완료/적재 로그는 UNKNOWN |
| 18:00 이전 실제 사용 가능 | 위 자료를 결합해야 판단 가능 | BLOCKED | 모든 필요 값의 published/received/ingested/feature-ready 시각이 cutoff 이하여야 함 |

거래 종료, 지수 확정, 배포, 공급처 수신, 사용 준비는 다른 사건이다. 종료시각을 임의로 available_at으로 쓰거나 공개 지연을0으로 놓지 않는다. 기존 현행 KRX 1차16:00/2차18:10 안내 기록은 적용 제품·역사적 기간·A/B 연결이 없으므로 18시 PASS나 모든 날짜 FAIL의 직접 증거로 쓰지 않는다. STEP10A에 보존된 2026-11-16 확인 기록이며 직접 HTML 조회403 한계도 유지한다.

## 검증 가능 조건과 복구 불가능 조건

원 제품과 A/B의 hash 연결 후, 적용기간별 배포 규칙·원시 수신/적재 로그·시간대·vintage를 세션별로 맞춘다. 실제 이용 가능시각은 해당 시스템의 필요한 배포·수신·적재·계산 완료 제약을 모두 만족해야 한다. 이후 revised close와 당시 값이 다르면 영향을 받는 피처·label·학습/평가 구간의 버전을 따로 감사한다. 신규 계산·재실험은 별도 승인 전 실행하지 않는다.

현재 다운로드한 파일이나 공급처의 현행 설명서만으로 historical PIT는 복원되지 않는다. 과거 로그/vintage가 소실됐다면 일부 또는 전체 기간을 UNKNOWN으로 유지해야 한다. 앞으로 로그를 수집하는 일은 과거 인증이 아니다. t 제외 window나 다음 세션 예측도 한계 완화 후보일 뿐 출처·지연·개정 증거의 대체물이 아니며, 승인 없이 계약을 변경하지 않는다.

## 초기 RAW5의 별도 문제

Foreign_Net은 시장 범위·현물/선물·단위·잠정/확정·최초 공표·개정이 미확정이다. NASDAQ/SOX는 미국 세션·DST·조기폐장과 공급처 공개 지연을 구분해야 하며, 일부 달력 검증이 CSV의 historical 수신 인증은 아니다. 초기 같은 날짜 결합/ffill·bfill 위험은 최신 F1과 분리한다. F1은 이 외부 변수들을 사용하지 않지만 국내 종가 PIT까지 면제되지는 않는다.

## 공통 근거와 확인 한계

우선 근거: [STEP10_MASTER_AUDIT_KO.md](STEP10_MASTER_AUDIT_KO.md), [STEP10_DATA_PIT_GAP_AUDIT_KO.md](STEP10_DATA_PIT_GAP_AUDIT_KO.md), [STEP10_STATISTICAL_EVIDENCE_KO.md](STEP10_STATISTICAL_EVIDENCE_KO.md), [STEP10A_PRICE_PROVENANCE_AUDIT_KO.md](STEP10A_PRICE_PROVENANCE_AUDIT_KO.md), [STEP10A_HISTORICAL_PIT_AUDIT_KO.md](STEP10A_HISTORICAL_PIT_AUDIT_KO.md), [STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md](STEP10A_SOURCE_EVIDENCE_REQUEST_KO.md), [STEP10B_MASTER_COMPARISON_KO.md](STEP10B_MASTER_COMPARISON_KO.md), [STEP10C_FINAL_RECOMMENDATION_KO.md](STEP10C_FINAL_RECOMMENDATION_KO.md), [STEP10C_STATISTICAL_RECONCILIATION_KO.md](STEP10C_STATISTICAL_RECONCILIATION_KO.md).

STEP11 확인일은 위와 같다. 기존 외부 조회의 확인일·접근 제한은 STEP10A 및 provenance 원기록을 따른다. 이번에는 외부 가격·새 공급처 인증 자료를 수집하지 않았다. 기존 문서의 주장과 외부 원자료로 입증된 사실을 분리하며, 새 금융 결과를 산출하지 않았다.
