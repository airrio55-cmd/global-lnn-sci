# S&P500 COMMON_LOCAL + walk-forward 최종 결과

전체 실험 완료: 모델 3개 × 손실함수 3개 × seed 5개 = 45개 학습 결과, baseline 3개.

Persistence Test Balanced Accuracy: 0.515074; Macro F1: 0.514657.

| Model | Loss | Test BA mean ± SD | Macro F1 mean ± SD | Δ BA vs Persistence | Seeds above Persistence |
|---|---|---:|---:|---:|---:|
| LSTM | MILD_FOCAL | 0.453608 ± 0.014671 | 0.439141 ± 0.018581 | -0.061466 | 0/5 |
| LNN | CE | 0.452067 ± 0.021289 | 0.408978 ± 0.039541 | -0.063007 | 0/5 |
| LNN | MILD_WCE | 0.447646 ± 0.019094 | 0.407318 ± 0.034275 | -0.067428 | 0/5 |
| LSTM | MILD_WCE | 0.443781 ± 0.022746 | 0.436983 ± 0.025099 | -0.071293 | 0/5 |
| LNN | MILD_FOCAL | 0.441273 ± 0.021742 | 0.409770 ± 0.034984 | -0.073801 | 0/5 |
| Transformer | CE | 0.439778 ± 0.052137 | 0.434146 ± 0.054181 | -0.075296 | 1/5 |
| LSTM | CE | 0.437473 ± 0.010966 | 0.420261 ± 0.020439 | -0.077601 | 0/5 |
| Transformer | MILD_FOCAL | 0.436937 ± 0.038119 | 0.433651 ± 0.039673 | -0.078137 | 0/5 |
| Transformer | MILD_WCE | 0.403550 ± 0.021916 | 0.388084 ± 0.034714 | -0.111524 | 0/5 |

## 저장 파일

- SCI_v1_4_WALKFORWARD.completed.ipynb: 처음부터 끝까지 실행한 노트북과 결과 출력
- final_results.csv: 모델·손실함수별 평균·표준편차 및 baseline 차이
- seed_results.csv: 45개 학습 결과와 baseline 3개
- persistence_comparison.csv: seed별 Persistence 대비 성능 차이
- baselines.csv, formatted_summary.csv: baseline 및 원본 형식 요약표
- run_manifest.json: 환경·원본 해시·실험 설정

## 변경 내용

원본 노트북의 모델, seed, 손실함수, epoch, 데이터 구간, threshold 선택 방식은 변경하지 않았습니다. 완료 노트북에는 결과 검증·Persistence 비교·CSV 저장 셀을 추가했습니다. nbformat이 누락된 cell ID를 보완했습니다. 이전 Yahoo 프록시 403은 네트워크 설정 적용으로 해결됐습니다.

Δ BA는 성능 차이이며 통계적 유의성을 뜻하지 않습니다. preflight_ 파일은 별도 사전 점검 데이터이고 최종 실험 결과와 구분합니다.
