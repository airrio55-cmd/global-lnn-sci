# STEP2 BLOCKERS

현재 실험 실행 상태: **BLOCKED**. 아래를 임의 시간·가격·휴장으로 대체하지 않는다. 합성 검사가 PASS해도 실제 데이터 증빙은 별도다.

| ID | 상태 | 문제·영향 | 해소 자료/조건 |
|---|---|---|---|
| B01 | BLOCKED | 2010~2025 공식 KRX 세션 달력 미확보. 20행을20거래일로 인증 불가 | KRX 공식 세션 목록·원천 URL/추출일·SHA-256, 완전성 대조 |
| B02 | BLOCKED | 같은 기간 외국인 데이터에 있으나 KOSPI에는 없는 날짜45개. 특히 파일상2022 첫 관측이01-04이므로 fold 경계도 확정 불가 | 각 날짜의 실제 개장 여부와 KOSPI200 확정 종가 대조; 원본 수정 대신 별도 검증 보완 파일 |
| B03 | BLOCKED | KOSPI 종가 공급처·조정정책·확정 공개시각이 없으므로 t18:00의 확정 가용성 미증명 | source/symbol·close 정의·공개/수집 시각·개정정책. 사용자첨부 해시 일치는 공급처 증거와 다름 |
| B04 | BLOCKED | NASDAQ/SOX 날짜만 존재. 미국 timezone·세션 schedule·조기폐장·공개 latency·max_age 미확정 | 실제 미국 세션별 market_close와 provider available_at/지연 근거·최대허용age. 임의16:00 또는0지연 금지 |
| B05 | BLOCKED | 외국인 순매수의 단위·시장범위·잠정/확정 시각·개정 미상 | 원천 metadata·공표 이력. 확인 전 당일 사용 금지. 보수안은 외국인 제외, 또는 검증된 전세션 값+승인된max_age이며 단순하루lag를 가용성 증거로 대체하지 않음 |
| B06 | BLOCKED | processed_regression_data.csv 생성 lineage 없음 | 생성 코드/버전·입력해시·PIT 규칙. Target_Ret20은 cutoff내 원본행 계산과 일치하지만 실제 KRX20세션 증거가 아님. 기본 pipeline에서 사용 제외 |
| B07 | BLOCKED | 실제 torch/ncps 환경·ncps 버전·LTC elapsed_time 단위 미확정 | 설치/실행은 STEP3 승인 후. reference 소스 commit·파라미터 제약·입력 mapping·dt 의미를 실제 환경과 대조 |

B01/B02 해소 전 `Calendar.verified=False`, target 생성 production 함수는 예외로 중단한다. 실자료 fold manifest의 observed 경계·candidate 표본은 진단용이며 confirmed_samples는 비워 둔다. B03~B05 해소 전 실제 per-sample model 입력 lineage를 만들거나 가용시각을 발명하지 않는다. 18:00 KST 제안과 실제 공개시각이 충돌하면 해당 변수/실험은 계속 BLOCKED다.

2026 자료를 더 받아 target을 보완하는 방법은 승인된 종료일에 어긋나므로 해소 방법이 아니다. 마지막20세션은 unknown으로 유지·평가 제외한다. 미래 누락 가격은 bfill 또는 가격 ffill로 채우지 않는다.

STEP3: 구현 검토·증빙 수집은 가능하나 **모델/HMM 실행 준비 완료가 아니다**. 모든 필수 데이터 gate 해소와 별도 실행 승인 전 training_enabled=false·hmm_fit_enabled=false를 유지한다.
