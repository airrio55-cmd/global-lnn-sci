# CHANGELOG — draft

## 2026-11-16 / 준비·정적 감사

추가: 별도 프로젝트 경로, 원본 노트북3개·CSV5개의 manifest, 18셀 비교·diff·행번호 증거, 데이터 inventory, 실제 Target/fill/split 재현, 데이터 전용7개 regression 검사(PASS), 심각도별 감사, 수정안·Rolling-Origin·피처 ablation·HMM 분리·LTC 시간상수 프로토콜, 수정 전후 테스트 계획, 실행 비활성 config.

보존: 원본8개 바이트와 해시. V14/V15 Journal of Forecasting 실험, 기존 잠금 파일, main 및 워크플로 미수정.

미구현 제안: nullable20일 target, PIT/as-of 데이터 가용성, flow 결측 정책, date-key split 및 purging, 통합 모델·AMP·seed·Hybrid 사양, forward HMM filtering·train-only 임계값·collapse 처리, 시드 의존성을 반영한 block 통계, LTC 유효 시간상수 추출.

미실행: 모델/HMM 학습0, 전체 실험0, 성능 재평가0, 결과 기반 튜닝0, main 병합0. 이번 검사는 정적·데이터 전용이며 성능 향상을 주장하지 않는다.
