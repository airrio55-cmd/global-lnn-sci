# 수정 전후 검증 계획

현재까지: 원본 JSON·소스 정적 비교, 독립 pandas 재현 및 합성 검사7개 PASS. 모델/HMM 미실행. 모델 성능·수렴·GPU 재현성은 미검증이다.

| 항목 | 수정 전 증거 | 수정 후 합격 기준 | 시점 |
|---|---|---|---|
| 원본 보존 | 8개 입력 SHA-256 | 모든 원본 해시 동일; 보호경로 변경0 | 매 변경 |
| Target tail | 마지막20개가0으로 잘못 확정 | nullable20개, 평가 제외, 기존 확정 label 동일 | 학습 전 |
| trading calendar | 20행 shift | 검증된 KRX 세션20개 label_end, 중복·누락·휴장 구분 | 학습 전 |
| PIT feature | 날짜 join, bfill 위험 | 모든 available_at<=decision_at; NY DST·미/한 휴일·조기폐장 fixtures | 학습 전 |
| 미래값 불변성 | bfill sentinel이 과거를 바꿈 | cutoff 뒤 원천 값을 극단값/삭제로 바꿔도 과거 피처·예측용 입력 동일 | 학습 전 |
| fill 정책 | US101개씩 ffill, bfill0 | bfill 금지, feature별 max_age/flow 규칙, 채움 lineage·건수 | 학습 전 |
| split/purge | 원시경계 다음 구간에 label_end 존재 | train/valid label_end가 해당 다음 cutoff보다 이전; label/window 날짜 key | 학습 전 |
| scaler | 기존 train-only fit | future sentinel 변경 시 train 통계 동일; train 밖 fit 금지 | 학습 전 |
| 입력 품질 | NaN0이나 KOSPI0값·SOX Volume0 | 범위/단위/공급처/개정·비유한값 검증; 금지 필드 사용 중단 | 학습 전 |
| 사양 동등성 | AMP/log offset/Hybrid 차이 | config snapshot, 모델 식·feature order·dtype·seed 동일 | 학습 전 |
| EarlyStopping | 순서에 따라 재정의 | 단일 정의, 고정 score sequence로 best deepcopy·patience·동점 검증 | 수정 구현 후 |
| scheduler | 100epoch OneCycle+earlystop | batch step 수 일치, LR trace, AMP skip 처리 규칙 | 승인된 smoke |
| 모델 smoke | 미실행 | 작은 합성 자료 forward/backward·shape·finite gradient·parameter count | 학습 승인 후 |
| 재현성 | deterministic 실패 무시 | 같은 env/seed 두 실행 예측 동등 또는 사전 tolerance, 로그 보존 | 학습 승인 후 |
| test 격리 | train 함수가 Xte 받음 | 학습 함수 test 미수신, test label 변조가 checkpoint 선택에 영향0 | 승인된 smoke |
| HMM causal | 전체 test predict+test median | 뒤 관측 perturb 시 앞 filtering 상태/확률 불변; train-only state map | HMM 승인 후 |
| HMM collapse | test median으로 위장 | 실패/collapse 명시, 해당 비교 제외 규칙 고정, fallback 별도명 | HMM 승인 후 |
| 시드 pooling | 같은 날짜를5/10회 복제 | 복제만으로 시장 날짜 수·유효 표본 증가 금지, date-key paired bootstrap | 통계 구현 후 |
| 통계 | iid exact 검정·다중비교 | toy null·paired block·Holm 검증, block20/40/60 사전 지정 | 통계 구현 후 |
| LTC tau | 원본 없음 | 버전 소스 확인, 단위·양수·finite, 고정 conductance toy식과 일치 | 분석 승인 후 |
| 보고 무결성 | 주석/실제20일 불일치 | fold·seed·사양·제외수·실패수 모두 표기; 결과 선택 보고 금지 | 최종 |

순서: 원본 증거 보존 → 정적 수정·데이터 gate → 수정 사양 검토 → 명시적 학습/HMM 승인 → smoke·budget → 전체 고정 실험. 수정 전후의 성능 수치는 현재 생성하지 않는다. 모델 smoke나 HMM causal 검사는 실제 fit를 포함할 수 있으므로 이번 단계에 실행하지 않는다.
