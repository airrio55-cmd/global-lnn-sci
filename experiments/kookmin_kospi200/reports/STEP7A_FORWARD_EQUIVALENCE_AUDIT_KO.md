# STEP7A FORWARD_EQUIVALENCE_AUDIT

동일 합성 입력·seed·가중치·CPU FP32·eval·no_grad에서 원래 Cell과 계측 Cell의 logits/final hidden/전체20 hidden이 bitwise 동일하다. 원본 LNNModel hidden128에서도 logits와 hidden 전 단계 동일성을 확인했다. 파라미터 변경0, RNG 소비 차이0, backward/optimizer 호출0. AST 산술 동일성 검사도 통과했다. τ의 FP32Torch 대 FP64NumPy 비교 tolerance와 출력 bitwise 정책을 혼동하지 않는다.

실제 금융 모델의 동등성을 확인한 것은 아니다. 후속에는 이미 저장된 STEP5B 확률과 exact 비교하며 source/input/scaler/batch/dtype 해시를 결합한다. 과거 raw logits가 보존되지 않은 경우 logits 자체와의 직접 비교를 주장할 수 없다. 추가 baseline 금융 forward를 실행하지 않고 한 번 계측한 출력 확률을 저장본과 비교한다. 불일치는 BLOCKED이며 tolerance 확대나 재추론으로 통과시키지 않는다.

확인일: 2026-11-20 KST. 설치 ncps 1.0.1의 정적 소스 및 독립 합성 입력만 사용했다. 금융 checkpoint는 bytes SHA만 읽었고 torch.load하지 않았다. 기존 8,635개 파일 SHA 및 500개 best checkpoint SHA가 일치한다. NN500·Test500·통계600행·HMM100후보/최종10을 보존했다. 가격 BOTH_UNVERIFIED, 과거 18:00 KST 가용성 UNKNOWN, production-PIT BLOCKED를 유지한다. 금융 τ·신규 NN/HMM 학습·금융 p값·GPU 실행은 모두 0이다. STEP7B는 자동 실행하지 않는다.


공식 소스: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py 및 https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc.py . 사용 기준은 설치 파일 SHA 대조이며 원격 commit과 설치 배포물의 완전한 공급망 동일성 또는 원본 논문의 과거 ncps 버전을 소급 인증하지 않는다.
