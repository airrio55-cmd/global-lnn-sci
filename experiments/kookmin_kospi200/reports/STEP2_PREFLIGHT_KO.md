# STEP2 PREFLIGHT

결론: **구현 검사23 PASS / 0 FAIL / 실자료 필수 gate7 BLOCKED**. 단계 실행 허가 상태는 BLOCKED이며 training_enabled=false, hmm_fit_enabled=false다.

실행:

```bash
python experiments/kookmin_kospi200/tools/step2_preflight.py
python experiments/kookmin_kospi200/tests/test_step2.py
```

테스트 환경은 requirements-step2.txt에 기록했다. torch/ncps/hmmlearn을 import하거나 설치하지 않았다. 원본8개 무결성을 먼저 검증했다. 기존 STEP1 evidence는 덮어쓰지 않았고 새 결과는 manifests/에만 썼다.

| 상태 | 범위 | 증거 |
|---|---|---|
| PASS | 원본8 SHA-256 보존 | evidence/input_manifest.json 대조 |
| PASS | cutoff 선적용·2026 수정/삭제 불변 | test02, data_cutoff_manifest.json |
| PASS | nullable tail·calendar endpoint 합성 | test03·04; 미검증달력 요청은 정상 차단 |
| PASS | 미국 가용성·DST·조기폐장·미래 perturbation | test05~09 합성 schedule·release metadata |
| PASS | strict train/valid label_end·5origin·window | test10·11, 합성 달력15구간 |
| PASS | Train-only scaler·transform 순서 | test12·22; sklearn 합성 fit만 수행 |
| PASS | 모델설정·seed·6feature·앙상블 | test13·14·23;3000 job은 메타데이터 |
| PASS | HMM forward causality·Train reference·collapse | test15·16; supplied synthetic parameter만 사용 |
| PASS | seed복제시 시장날짜 증가 방지·bootstrap/Holm | test17·18;100개 합성날짜,30draw만 사용 |
| PASS | τ synthetic snapshot·미확정단위 차단 | test19; 실제 모델 forward 없음 |
| PASS | 금지 import/호출·실행 gate·BLOCKED 보존 | test20·21·22 |
| BLOCKED | 공식 KRX 전체달력 | B01 |
| BLOCKED | KOSPI 부재날짜45개 가격대조 | B02 |
| BLOCKED | KOSPI 종가 출처/공표시각·18시계약 | B03 |
| BLOCKED | NASDAQ/SOX 미국 schedule·latency·max_age | B04 |
| BLOCKED | 외국인 단위/시장/발표·개정 | B05 |
| BLOCKED | 가공파일 생성 provenance | B06; 기본 pipeline에서 제외 |
| BLOCKED | torch/ncps 실제 버전·LTC 단위 | B07 |

PASS/BLOCKED는 서로 다른 의미다. 예를 들어 가용시각이 없을 때 코드가 올바르게 차단하면 합성검사는 PASS지만 실제 변수의 입력 검증은 BLOCKED다. `confirmed_production_sample_count` 및15구간의 confirmed_samples를 임의 숫자로 채우지 않았다.

2026년 종가가 타깃 확인용으로 새로 들어오는 것을 허용하지 않는다. 원본기간을 포함하는 기존 노트북/기존결과는 역사적 보존 자료이며 신규 분석 입력이 아니다. 원본의 전체 실행을 통한 검증은 금지한다.
