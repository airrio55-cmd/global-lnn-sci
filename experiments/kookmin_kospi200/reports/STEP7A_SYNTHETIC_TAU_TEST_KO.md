# STEP7A SYNTHETIC_TAU_TEST

33 PASS / 0 FAIL. raw/effective 공식, positive 1회, sensory/recurrent gate, sparsity, affine/broadcast, hidden timing, 실제6 substep, elapsed/cm_t, finite/positive, dtype, 원본 logits/hidden, 재현성, 입력/hidden 의존성, 잘못된 constraints/metadata/SHA/identity 차단, 변조 감지, 일반 hook 한계, 금융 I/O 차단을 검사했다.

추가 검증은 NumPy frozen 참조와 모든 실제 substep 비교(rtol=2e-6, atol=2e-7), 관측 entry=substep0, reversal 처리, 원본 Notebook LNNModel(input2,hidden128)의 정확한 추출 소스 재사용, 배치 행별 lineage, 3종 RNG 불변, training mode 차단이다. 합성 gate 검증 결과이며 금융 τ 결과가 아니다.

확인일: 2026-11-20 KST. 설치 ncps 1.0.1의 정적 소스 및 독립 합성 입력만 사용했다. 금융 checkpoint는 bytes SHA만 읽었고 torch.load하지 않았다. 기존 8,635개 파일 SHA 및 500개 best checkpoint SHA가 일치한다. NN500·Test500·통계600행·HMM100후보/최종10을 보존했다. 가격 BOTH_UNVERIFIED, 과거 18:00 KST 가용성 UNKNOWN, production-PIT BLOCKED를 유지한다. 금융 τ·신규 NN/HMM 학습·금융 p값·GPU 실행은 모두 0이다. STEP7B는 자동 실행하지 않는다.


공식 소스: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py 및 https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc.py . 사용 기준은 설치 파일 SHA 대조이며 원격 commit과 설치 배포물의 완전한 공급망 동일성 또는 원본 논문의 과거 ncps 버전을 소급 인증하지 않는다.
