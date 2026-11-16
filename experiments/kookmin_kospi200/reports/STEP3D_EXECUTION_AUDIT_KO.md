# STEP3D 실행·재사용 감사

설계2: A/B 병렬 회고적·탐색적 F1 CPU Train/Validation 연구다. A/B=BOTH_UNVERIFIED, production-PIT=BLOCKED를 유지한다. Validation으로 주 가격·모델·Seed·사양을 선택하지 않았다. 독립 Test/HMM/GPU/외부5피처/Ensemble/2026 관측 사용은 이번 단계0건이다.

최초 O3 실행은 2026-11-16T20:47:37.687511+09:00~2026-11-16T21:25:47.166648+09:00에 STEP4A-1로 완료됐다. 이번 STEP3D에는20개 신규 학습을 실행하지 않고 정확히 같은20개를 검증·재사용했다. 기존40개 checkpoint/latest/history/Validation 확률160개와 O3의100개 파일 해시를 대조했다.

Master SHA `f4ea7a18d7812b00b8c581191a110f63a6799a22e066484ec251ee32f7912c5c`. 학습 kernel SHA `676cff063a52141a62fef3f9cda96db582fb75a8a831f54b1a18d3aba91eff09`. O3 config/worker/manager와 원본 모델·환경 pin을 동결 manifest와 대조했다. master production 플래그는 모두false다.

O3 원래 staged 가격·배열·scaler·label/date·Train-only 수동 reference를 재구성했다. 별도 모델 생성/forward/checkpoint load/학습은0건이다. 원래 epoch1 logits/RNG 복원과 best 확률 복원 PASS20건의 증거 파일 SHA를 이번에 검증했으며 새로 복원 실행한 것으로 표현하지 않는다. 학습 runner를 새로 만들지 않아 신규 training runtime smoke는 해당 없음이다. 읽기 전용 보고 runner와 기존 O3 경계 회귀검사는 실제 실행했다.

기존 preflight12개 및 결과14개를 __main__ 기록 함수를 호출하지 않고 재실행했다. 기존 test결과 파일을 덮어쓰지 않는다. 새 검사와 회귀 결과는 [tests](../manifests/step3d_test_results.json)에 기록한다.

상세 원자료 경로/스케일러값/일별Target·확률/weights는 공개하지 않는다. 공개 execution manifest에는 identity·상태·해시·집계만 기록한다. 기존 모든 파일 byte 보존은 아래 preservation 검사로 확인한다. main/JOF/이전 보고서·성능표는 수정하지 않는다.
