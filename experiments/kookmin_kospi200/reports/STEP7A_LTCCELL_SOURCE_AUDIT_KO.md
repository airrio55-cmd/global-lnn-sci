# STEP7A LTCCELL_SOURCE_AUDIT

설치 Cell SHA: 167a9d6e1f4dc653ce21420010709e1c995716e53ad0d8bbc2d53c19c40b123f
Wrapper SHA: bbf3127013d3969994ecf0debf4eb37b56db750475ee71646a9decdf1aaf3026

LTC wrapper는 implicit constraints=True이나 직접 Cell 생성 기본값은 False다. F1 모델은 입력2, FullyConnected hidden128, mixed_memory=False, batch_first=True, return_sequences=True, affine input/output mapping, 기본 zero hidden이다. cm/gleak shape128, recurrent w/mu/sigma/erev128×128, sensory 대응2×128, mapping 입력2/출력128, mask는 wiring에서 결정한다. 실제 금융 payload의 파라미터 내용/shape 재로드 검증은 금지 범위라 STEP7B로 남긴다.

입력 affine 변환→sensory gate와 mask→positive cm_t/w→6회 recurrent gate와 mask→원래 분자/분모/epsilon 업데이트 순서다. timespans 생략 시 scalar1.0. 현재 adapter는 고정 CPU FP32 계약을 대상으로 하며 임의 batched timespans 지원을 인증하지 않는다.

기존 tau.time_constants의 NumPy 공식은 참조로 재사용한다. 기존 master_tau.supplied_tau_snapshot의 메타데이터 검사만으로 실제 substep 계측을 증명할 수 없고 SHA 형식·날짜/session lineage·파라미터 변조 검사를 강화할 필요가 있다. frozen 두 파일은 수정하지 않았다.

확인일: 2026-11-20 KST. 설치 ncps 1.0.1의 정적 소스 및 독립 합성 입력만 사용했다. 금융 checkpoint는 bytes SHA만 읽었고 torch.load하지 않았다. 기존 8,635개 파일 SHA 및 500개 best checkpoint SHA가 일치한다. NN500·Test500·통계600행·HMM100후보/최종10을 보존했다. 가격 BOTH_UNVERIFIED, 과거 18:00 KST 가용성 UNKNOWN, production-PIT BLOCKED를 유지한다. 금융 τ·신규 NN/HMM 학습·금융 p값·GPU 실행은 모두 0이다. STEP7B는 자동 실행하지 않는다.


공식 소스: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py 및 https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc.py . 사용 기준은 설치 파일 SHA 대조이며 원격 commit과 설치 배포물의 완전한 공급망 동일성 또는 원본 논문의 과거 ncps 버전을 소급 인증하지 않는다.
