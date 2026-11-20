# STEP7A INSTRUMENTATION_DESIGN

새 versioned adapter src/kospi200/step7a_tau.py는 핀된 설치 solver AST에 읽기 callback만 삽입한다. callback을 제거한 AST가 원본과 정확히 같은지 검증하여 산술식·연산 순서·ODE 횟수를 보존한다. 설치 ncps 소스는 수정하지 않는다.

wrapper가 cell.forward를 직접 호출하므로 일반 cell hook으로 substep6개를 얻지 못한다. A는 각 관측 진입 hidden/input, B는 실제 ODE 업데이트 직전 hidden을 읽는다. 업데이트 후 hidden과 다음 단계 연결도 검사했다. 각 time_index당 substep0~5를 실제로 확보했고 A=첫 substep을 검증했다.

lineage: Origin/A·B/Seed/checkpoint SHA/Cell·계측 source SHA/constraints/elapsed/unfolds/관측일·session/window time_index/substep/예측 기준일/shape. 배치 행별 window 날짜와 session을 따로 유지한다. clone/detach만 사용하며 eval/no_grad, 파라미터 fingerprint 전후 일치, Python/NumPy/Torch RNG 불변을 검사한다. 오류 시 원래 bound method를 복원한다. 금융 entrypoint는 승인 flag와 무관하게 무조건 예외를 발생시켜 load/forward를 막는다.

확인일: 2026-11-20 KST. 설치 ncps 1.0.1의 정적 소스 및 독립 합성 입력만 사용했다. 금융 checkpoint는 bytes SHA만 읽었고 torch.load하지 않았다. 기존 8,635개 파일 SHA 및 500개 best checkpoint SHA가 일치한다. NN500·Test500·통계600행·HMM100후보/최종10을 보존했다. 가격 BOTH_UNVERIFIED, 과거 18:00 KST 가용성 UNKNOWN, production-PIT BLOCKED를 유지한다. 금융 τ·신규 NN/HMM 학습·금융 p값·GPU 실행은 모두 0이다. STEP7B는 자동 실행하지 않는다.


공식 소스: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py 및 https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc.py . 사용 기준은 설치 파일 SHA 대조이며 원격 commit과 설치 배포물의 완전한 공급망 동일성 또는 원본 논문의 과거 ncps 버전을 소급 인증하지 않는다.
