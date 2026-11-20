# STEP10A historical18KST PIT 증빙 감사

감사일: **2026-11-21, Asia/Seoul**. 대상: `airrio55-cmd/global-lnn-sci`, `audit/kookmin-kospi200-20261116`, `experiments/kookmin_kospi200/`.

STEP10A는 기존 가격 provenance와 historical PIT 증빙의 읽기 전용 감사다. 신규 금융 학습·checkpoint load/forward·Test 예측/성능 재평가·HMM fit/refilter·τ 계측·bootstrap/draw·p값/CI는0이며 원본·기존 결과·설정을 변경하지 않는다. master training_enabled=false / hmm_fit_enabled=false / new_fit_execution_enabled=false를 유지한다. 2026년 날짜가 있는 파일 속성은 입수·편집 메타데이터로만 읽으며 2026 시장 관측은 사용하지 않는다.

가격 상태는 **BOTH_UNVERIFIED**, primary price **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**다. SHA 일치는 무결성 증거이지 외부 공급처·공표시각·과거 vintage 인증이 아니다. Test 성능으로 A/B를 고르지 않는다.

## 세 종류의 시각과 개정 버전

관측 기준일(session date), 지수 산출/공표시각(published_at), 실제 공급처 공개·사용자 수신/적재시각(received_at/ingested_at)은 다르다. 종가가 장 종료 후 산출된다는 사실만으로 익명 CSV/Excel 값이 당시18시에 도착했다고 할 수 없다. 기간별 정규장 제도·특수세션·수정 배포가 달라 한 현재 장종료시각을2010~2025 모든 날짜에 대입하지 않는다.

보존된 현행 KRX 상품 안내는1차16:00/2차18:10 전송으로 요약돼 있다(E08, 과거확인2026-11-16). 이는 해당 제품의 현재 일정에 대한 과거 웹도구 기록이며, 원천 HTML 직접조회는403이었다. 이 일정의 역사적 적용기간·제품과 A/B의 연결·공급처지연·그날 사용한 버전은 미확인이다. 1차가18시 전이라고 현재 최종본을 사용 가능하다고 선언할 수 없고, 2차18:10 값을18시로 앞당길 수도 없다. 현행 안내를2010~2025의 일괄 최초 공표시각으로 사용하지 않는다.

기존 저장소 보조코드의 Close_available_at=Seoul day-end는 보수적 분석 convention이다. 실제 receipt 기록이 아니며 현재의18시 계약과도 다르다. 이런 날짜+시각 생성값을 사실의 증빙으로 승격하지 않는다. provider delay=0도 가정하지 않는다.

## F1 입력의 실제 가격 의존성과 cutoff

원형 Notebook과 새 F1은 같은 설명으로 묶지 않는다. 원형 t제외 window와 달리 현재 동결 F1은 **t-19~t**의20개 입력이고 순서는 **[Log_Ret, Disparity]**다(E10).

- Log_Ret[s]=ln(C[s]/C[s-1])이므로 s와 직전세션의 가격이 필요하다.
- Disparity[s]=C[s]/mean(C[s-19:s])-1이므로 s포함20세션 가격이 필요하다.
- 따라서20개 F1 입력 전체의 가격 의존 범위는 공식세션 기준 최대 t-38~t다. 이는 코드의 trailing 식에서 도출한 정적 의존성 설명이며 가격 배열 계산을 실행한 결과가 아니다.
- Vol_Regime=Log_Ret.rolling(40).std(ddof=1)는 NN 입력이 아니라 공통 적격 마스크/수동 레짐 보조변수다. 기존20window 공통 적격 마스크는 더 긴 종가 이력(t-59~t)을 참조할 수 있다. 이를 제3 신경망 입력으로 표시하지 않는다. 적격성·Train threshold의 개정 의존성도 별도로 검증해야 한다.

각 가격 C[s,v]는 해당 시각까지 공급처에 공개·수신·적재된 버전 v여야 한다. 단순히 미래 날짜가 입력에 없다는 사실만으로 과거 가격의 사후 개정이 배제되지는 않는다. 매 기준일 t의18:00 KST를 d라 하면 필요한 각 s에 대해 (i) 동일 제품·필드의 당시 버전이 식별되고, (ii) published_at 및 실제 received_at/ingested_at가 d 이전이고, (iii) 피처 계산완료시각이 d 이전임을 확인해야 한다. 계산 지연도0으로 가정하지 않는다. 각 피처의 available_at은 필요한 가격 버전의 가용시각 최댓값과 계산/적재 지연에 의해 결정된다.

현재 A/B는 최종 다운로드 시계열이고 행별 최초공개·수신·vintage가 없다. 특히 t종가뿐 아니라 t이전 가격의 이후개정도 trailing 피처에 영향을 줄 수 있으므로 과거 창 전체를 as-of로 대조해야 한다. 현재 Close/피처 값의 SHA는 이 요건을 대신하지 못한다.

Target=I(C[t+20]>C[t])는 미래의 평가 정답이지 입력의 당시 관측가능 정보가 아니다. 실제KRX20세션, 기간종료2025-12-31 및 마지막20UNKNOWN 규칙은 보존한다. 타깃을 사후 확정하는 것과 미래 endpoint를 학습 입력·모델선택에 쓰는 것은 구분한다. 이번 단계는 기존 label·cutoff 진단을 읽기만 하고 새로 계산하지 않았다.

## PIT 하위 요건별 판정

| 항목 | 판정 | 확인 내용 / 부족 증빙 |
| --- | --- | --- |
| 시계열의 관측 기준일·공식 세션 | VERIFIED | 기존3939 날짜 정렬; 수치 진위/공표시각은 제외 |
| F1 trailing 수식·t포함20window·18:00 계약 | VERIFIED | 정적 계약; 원자료 최초 가용성 검증 아님 |
| 패키지 생성·수정 및 Refresh 시각 | PARTIALLY_VERIFIED | 표시값은 확인; 추출·공표·실수신과 구분 |
| 기간별 공식 종가 확정·개정 배포 | UNKNOWN | 해당 가격제품의 과거버전 배포 증빙 부재 |
| 공급처별 최초 공개시각/지연 | UNKNOWN | A/B 공급처 미확인; product/timezone/latency 기록 필요 |
| 사용자의 실제 수신·적재·계산완료 | UNKNOWN | 수신/서버/ingestion·피처 완료 로그 부재 |
| 과거 창의 as-of 수정/조정 이력 | UNKNOWN | 최종본과 각기준일 당시 버전 관계 미확인 |
| 당시18시 입력 적격·production-PIT | BLOCKED | 위 사실이 확인되기 전 인증 불가 |

## 보수적 대안은 제안일 뿐 적용하지 않음

기존 STEP28은18시 계약을 유지하되 입력을 t-20~t-1로 바꾸는 안과 다음 실제 KRX 세션의 의사결정으로 옮기는 안을 제시했다. 어느 안도 실제 과거 공급처 공개·개정 증빙을 면제하지 않는다. 다음 세션09:00 등은 제안 decision time이지 확인된 release time이 아니다. t종가를 target 기준값으로 두는지·결정시각과 label 기준일의 관계·영업일 규칙을 별도 동결해야 한다. 이번 감사에서 기존 계약을 변경하거나 대안을 사후 선택하지 않았다. 변경 시 기존 실험과 같은 조건의 재현으로 주장할 수 없다.

## 외부 피처는 별도 범위

Foreign_Net의 범위·단위·잠정/확정·공표/개정은 UNKNOWN이고 당일 입력 사용은 BLOCKED다. NASDAQ/SOX는 기존 세션/DST/조기폐장 일부 증거가 PARTIALLY_VERIFIED이지만 공급처 공개지연·과거vintage·전체기간 매핑은 별도 미해결이며 확정 입력은 BLOCKED다. 이 문제를 현재 F1에 외부 피처가 실제 들어갔다고 해석하지 않는다. 또한 F1만의 구조적 검증으로 RAW5/LOG2 Ensemble PIT를 인증하지 않는다. 원형5피처 문제와 국내가격의18시 문제는 서로 다른 gate다.

근거: E03/E08/E10/E11/E12 및 STEP10A_PRICE_PROVENANCE_AUDIT_KO.md의 증거표. 새 공식 공표/가격 수집은 수행하지 않았다.
