# STEP10 동결 manifest와 변경 통제

확인일: 2026-11-20 KST

이번 STEP10은 기존 저장 결과의 읽기 전용 감사와 논문 집필용 동결이다. 새 금융 fit / checkpoint load·forward / bootstrap draw / p값 / CI / Test 예측·성능 재계산 / HMM refit·refilter / LTC τ 계측 / Ensemble / GPU / 외부 금융 수집 / 2026 시장 관측 사용은 모두 0이다. master training_enabled=false, hmm_fit_enabled=false, new_fit_execution_enabled=false를 유지했다.

가격 A/B는 BOTH_UNVERIFIED, 주 분석 가격은 PENDING, historical 18:00 KST available_at은 UNKNOWN, production-PIT는 BLOCKED다. 재현성 snapshot의 PASS와 원천·PIT·통계적 타당성의 PASS는 서로 다르다. 기존 파일을 수정하지 않고 신규 STEP10 자료만 작성한다. 단일 복구 τ를 역산할 수 있는 새100개 정량집계·차이·분할값은 공개하지 않는다.

시작 snapshot은 기존 10,048개 project 파일의 byte SHA-256·크기·역할·근거경로를 private에 보존한다. 기존 stage의 이전 snapshot과 교차대조해 이미 변경된 결과를 시작값으로 정상화하지 않았고, 종료 때 같은 시작 snapshot을 다시 검사한다. 해당 private 전체목록과 checkpoint/identity/input/scaler/environment SHA 연결은 공개하지 않는다.

공개 step10_freeze_manifest.json은 과거 공개 승인된 report/manifest의 안전한 byte SHA·버전·상태와 lineage만 싣는다. 원4D처럼 로컬 상세보고서와 공개 축약본이 다른 경우, 공개 snapshot은 실제 과거 공개본 bytes를 해시한 것임을 명시한다. 로컬 전체 snapshot과 공개 subset을 혼동하지 않는다. 별도의 publication receipt는 실제 GitHub commit과 연결하고, 자기 SHA를 자기 JSON 안에 넣는 순환 manifest를 만들지 않는다.

모델·metric 계약은 STEP3C/5A/5B의 원본과 연결되며 fixed settings를 새 operational config로 바꾸지 않는다. τ99→100 복구·원baseline 실패40→복구40·기존 통계·방법론 미검증은 각 version별로 연결된다. 기존 통계 결과/합성 결과를 수정하지 않고 read-only로 인용한다.

후속 논문 문장 편집은 가능하지만 수치·실험설정 변경은 새로운 snapshot version과 감사를 요구한다. SHA 일치는 원천 가격이나 역사적 정보 가용성의 과학적 검증이 아니다. __pycache__ 제외를 명시하고 core 결과·원본·source·manifest·ledger를 포함했다. 원본 금융 파일은 수치 파싱하지 않고 byte hashing만 했다. 원격 main 보존과 새 commit의 신규 STEP10 경로 한정 여부를 별도 확인한다.

