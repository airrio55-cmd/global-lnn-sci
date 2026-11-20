# STEP7A EXECUTION_READINESS

합성 계측 준비 PASS. 금융 실행 BLOCKED. 현재 financial_tau_enabled=false, training_enabled=false, hmm_fit_enabled=false, checkpoint load/forward 예산0, 허용 금융 read/write=[]이다. 승인 template approved=false. 금융 gate를 flag 하나로 열 수 없다.

후속 제안 100 checkpoint/100 cohort-batch forward 최대, worker1 CPU. 전체 24,100 window 기준 observation τ 61,696,000 float32값(246,784,000 bytes), substep τ 370,176,000값(1,480,704,000 bytes). raw τ는 모델×128=12,800값(51,200 bytes)만 저장한다. eff+h_pre는 약2.96GB; eff+h_pre+sensory/recurrent 합은 약5.92GB. 저장 예산8GiB를 제안한다. full synapse activation을 영구 보존하지 않는다. 최대 cohort 한 float32 substep tensor 약15.24MB, 주요6tensor 약91.42MB다. 순차/streaming RAM 예산1GiB는 계획값이며 금융 실행 전 실제 자원 gate를 다시 확인해야 한다. 이번에 금융 저장 공간을 할당하거나 데이터를 읽지 않았다.

개별 identity·checkpoint·data/scaler·stored probability/HMM 연결은 ignored private roster에만 둔다. 기존100 LTC roster 준비 완료이며 24 퇴화를 제외하지 않았다.

확인일: 2026-11-20 KST. 설치 ncps 1.0.1의 정적 소스 및 독립 합성 입력만 사용했다. 금융 checkpoint는 bytes SHA만 읽었고 torch.load하지 않았다. 기존 8,635개 파일 SHA 및 500개 best checkpoint SHA가 일치한다. NN500·Test500·통계600행·HMM100후보/최종10을 보존했다. 가격 BOTH_UNVERIFIED, 과거 18:00 KST 가용성 UNKNOWN, production-PIT BLOCKED를 유지한다. 금융 τ·신규 NN/HMM 학습·금융 p값·GPU 실행은 모두 0이다. STEP7B는 자동 실행하지 않는다.


공식 소스: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py 및 https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc.py . 사용 기준은 설치 파일 SHA 대조이며 원격 commit과 설치 배포물의 완전한 공급망 동일성 또는 원본 논문의 과거 ncps 버전을 소급 인증하지 않는다.
