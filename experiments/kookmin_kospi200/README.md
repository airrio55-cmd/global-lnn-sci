# 국민대학교 박사학위논문 KOSPI 200 별도 프로젝트

상태: 정적 감사와 프로토콜 초안. **학습·HMM fit·결과 기반 튜닝 금지.**
기준: `airrio55-cmd/global-lnn-sci@3324ead54266b07df176d312b6604289b50523a8`.
작업 브랜치: `audit/kookmin-kospi200-20261116`. 기존 V14/V15, lock, workflow에는 변경하지 않는다.

- `reports/AUDIT_KO.md`: 18셀 비교, 심각도, 코드 위치, 실제 데이터 재현.
- `reports/PROTOCOL_KO.md`: 수정안·Rolling-Origin·피처 ablation·LTC 시간상수·규모.
- `reports/TEST_PLAN_KO.md`: 수정 전후 gate.
- `evidence/input_manifest.json`: 첨부8파일 SHA-256·크기.
- `evidence/data_inventory.json`: CSV별 범위·결측·중복·0값·출처 상태.
- `evidence/data_only_checks.json`, `static_tests.json`: 학습 없는 재현·7검사.
- `evidence/*_cells.txt`, `cell_comparison.csv`, `*.diff`: 원본 셀 증거.
- `configs/proposed.json`: 비실행 사양; 승인 또는 preregistration lock가 아님.
- `CHANGELOG.md`: 이번 준비 작업과 미구현 수정안.

첨부 원본8개는 작업 환경의 `originals/`에 바이트 그대로 보존했다. 새 공개 브랜치에는 원본 데이터를 재업로드하지 않고 manifest와 감사 문서·정적 도구만 저장한다. 재현 시 manifest에 맞는 원본8개를 `originals/`에 배치한다. 저장소 기존 KOSPI CSV는 첨부 KOSPI 파일과 해시가 일치하지만 원천 공급처 증거는 별도 필요하다.

`python experiments/kookmin_kospi200/tools/static_audit.py`는 pandas/numpy를 사용하여 소스·데이터만 읽고 evidence를 재생성한다. 모델 패키지 import, notebook execution, fit, GPU 작업은 없다. 데이터와 SHA-256을 먼저 검증해야 한다. 학습 진입점과 자동 workflow는 제공하지 않는다.

저장된 과거 notebook 출력은 새 실행 결과가 아니다. 미확정 target 제거·PIT 결합·purging 등 모델 코드 수정은 **제안** 상태다. main 병합·학습은 승인되지 않았다.

