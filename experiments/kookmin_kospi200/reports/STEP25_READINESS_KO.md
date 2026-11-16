# STEP2.5 준비도

**STEP3 모델/HMM Smoke Test 진행 불가.** 공식 세션 달력은 PASS지만 실제 가격·PIT·원본 라이브러리 및 checkpoint 단위 검증이 남았다. 신경망/HMM fit·GPU·실제 모델 forward·checkpoint 로드·패키지 설치는 이번 단계에 하지 않았다. 기존 `training_enabled=false`, `hmm_fit_enabled=false`를 유지한다.

실행 없이 가능한 다음 작업은 공식 가격·원본 공급처·가용시각·환경lock의 증빙 보완과 코드 리뷰다. 합성 숫자·소스·시간대·데이터 무결성 검증34개가 통과했으나 이를 실자료 smoke로 간주하지 않는다.

| 준비 요소 | 상태 |
|---|---|
| 공식 KRX2010~2025 날짜/휴장/세션id3939개 | PASS |
| 원본3894개 KOSPI 날짜의 거래일 여부·중복/비거래일 | PASS: 중복0·비거래일0 |
| 45개 누락일 거래일 판정 | PASS: 전부 개장일 |
| 누락45일·원본가격의 공식 종가 일치 | BLOCKED |
| 2025 마지막20세션 unknown·2026입력/타깃 금지 | PASS: 날짜 규칙, 원본가격 공식인증은 별도 |
| 미국2021~2025 종료시각·earlyclose10일 | PASS: 시장달력 범위 |
| 미국2010~2020 전체 시장달력 | BLOCKED: 특정 공식공지·clock규칙만 부분확인 |
| 실제 CSV의 provider-PIT mapping | BLOCKED: 공개지연·revision UNKNOWN |
| 외국인 당일 입력 | 사용 불가 |
| 가공파일 기본 입력 | 계속 제외 |
| LTC 공식 reference 식·solver·constraint 의미 | PASS: 정적 범위 |
| 원본ncps/hmmlearn 버전·실제 checkpoint·dt단위 | BLOCKED |
| 원본/기존결과/V14/V15/main 보존 | PASS: 이번 변경은 별도 프로젝트 안 |

최종 모델 표본 수는 **null**이다. 공식 달력상3939세션은 확정됐지만 현재원본가격만의 diagnostic label3833·t포함window2467을 확정실험 표본으로 보고하지 않는다.15개 origin/구간의 공식 경계와 진단 수는manifest에 있고 confirmed_samples는 비워 뒀다. 누락 가격이rolling에 전파되는 효과를 숨기거나 결과를 보고 필터를 바꾸지 않았다.

미국 날짜 mapping 비교는1224개 검증 가능한 시장종료 candidate 범위에서만1184/52/42건의 차이를 보고한다. 실제 provider-PIT 확정 수는0이다. 현행 방법론이나 미확인 공개지연을 사용해 전체2010~2025 입력을 확정하지 않는다.

구현상 보완: ncps1.0.1의 LTC wrapper는양수제약기본True이고 LTCCell 직접기본은False다. τ 도구가모드를추정하지않도록explicit bool을필수화했다.기존23회귀와새11검사가모두PASS다.실제모델을생성하거나forward한검사가아니다.

단계 진행 조건:

1. B02~B06의 필요한 실자료 증빙을 확보하고, 이전 source-row horizon 기반 가공자료는 재검증한다.
2. 원본 보존 상태에서 공식 가격 보완·PIT lineage·origin 표본을 파생물로 재생성하고 실제데이터 future-perturbation을 통과한다.
3. 원본ncps/hmmlearn 버전·checkpoint metadata·단위 계약과 STEP3 실행환경을 검토한다.
4. 별도 실행 승인을 받은 후에만 모델 smoke를 시작한다. main 병합은 이번 단계에 하지 않는다.

확인일과 공식 출처는 STEP25_DATA_VERIFICATION_KO.md 및 provenance/에 연결돼 있다. 이 문서는자기commit에포함되므로최종commit SHA는대화보고와GitHub기록으로제공한다.
