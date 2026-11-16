# CHANGELOG — draft

## 2026-11-16 / 준비·정적 감사

추가: 별도 프로젝트 경로, 원본 노트북3개·CSV5개의 manifest, 18셀 비교·diff·행번호 증거, 데이터 inventory, 실제 Target/fill/split 재현, 데이터 전용7개 regression 검사(PASS), 심각도별 감사, 수정안·Rolling-Origin·피처 ablation·HMM 분리·LTC 시간상수 프로토콜, 수정 전후 테스트 계획, 실행 비활성 config.

보존: 원본8개 바이트와 해시. V14/V15 Journal of Forecasting 실험, 기존 잠금 파일, main 및 워크플로 미수정.

미구현 제안: nullable20일 target, PIT/as-of 데이터 가용성, flow 결측 정책, date-key split 및 purging, 통합 모델·AMP·seed·Hybrid 사양, forward HMM filtering·train-only 임계값·collapse 처리, 시드 의존성을 반영한 block 통계, LTC 유효 시간상수 추출.

미실행: 모델/HMM 학습0, 전체 실험0, 성능 재평가0, 결과 기반 튜닝0, main 병합0. 이번 검사는 정적·데이터 전용이며 성능 향상을 주장하지 않는다.

## STEP2 / 2026-11-16

사용자 확정: 분석기간2010-01-01~2025-12-31,2026관측 모든 단계·타깃보완 제외. 원본 바이트 보존, 파생자료 cutoff 선적용. 이전의2026종가 보완 제안 폐기.

추가: cutoff/검증KRX달력 nullable target/PIT·US schedule/lineage/strict purge·5origin/Train-only scaler/10모델·6ablation 선언형사양/keyed ensemble/HMM forward·Train계획/date block bootstrap·Holm/LTC snapshot 인터페이스, config2개, manifest, 테스트23개, STEP2 보고3개.

통일: 원본 단일은 CUDA AMP자동·log offsets111/211/311/411/511·Hybrid=.7LNNensemble+.3RNNensemble. 원본 다중은 AMPoff·log offsets102/202/302/402/502·Hybrid=.7LNNensemble+.3RNNraw. 신규는 FP32/AMPoff·다중offset·다중Hybrid로 고정. RAW/LOG feature순서와동일seed 결합을검증. 원본 t-20..t-1와신규 t-19..t를config분리하며같은조건결과라고하지않음.

실행: 데이터·합성23PASS/0FAIL, 실자료7BLOCKED. KOSPI3935→3894,2026제외41,마지막unknown20,기준일후보2025-12-01. 공식KRX달력과공표시각미확정으로확정표본수null.

이전STEP1 전체기간재현 runner비활성화. STEP1 evidence·원본·기존결과·main·JOF V14/V15·lock·workflow미수정. 모델/HMM fit·GPU·실제model forward·checkpoint로드·실자료검정·결과기반튜닝0.
