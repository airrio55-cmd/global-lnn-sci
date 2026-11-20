# STEP7A NEXT_GATES

STEP7B 전에 별도 사용자 승인, 정확100 identity 및 source/config/data/scaler/environment/계측 SHA 결합, 기존 Test 입력/window/날짜 경계, 100 forward 상한, 출력예산, committed ledger와 실패 정책을 확정해야 한다. 과거 결과를 덮어쓰지 않고 완료 identity를 재실행하지 않는다. 금융 payload 호환성과 저장 확률 동등성은 실제 승인 후 확인할 항목이다.

STEP7A의 합성 PASS는 금융 실행 승인이나 production-PIT PASS가 아니다. 원천 가격과 historical18시각 한계, 시드·Origin·뉴런 의존성을 유지한다. RAW5/LOG2 Ensemble을 대신 검증한 것이 아니다. 금융 bootstrap/Holm/p값, 신규 NN/HMM, Test 재평가·HMM refiltering은 별도 승인 없이 하지 않는다. 금융 τ는 STEP7B 승인 전 0으로 유지하고 종료한다.

확인일: 2026-11-20 KST. 설치 ncps 1.0.1의 정적 소스 및 독립 합성 입력만 사용했다. 금융 checkpoint는 bytes SHA만 읽었고 torch.load하지 않았다. 기존 8,635개 파일 SHA 및 500개 best checkpoint SHA가 일치한다. NN500·Test500·통계600행·HMM100후보/최종10을 보존했다. 가격 BOTH_UNVERIFIED, 과거 18:00 KST 가용성 UNKNOWN, production-PIT BLOCKED를 유지한다. 금융 τ·신규 NN/HMM 학습·금융 p값·GPU 실행은 모두 0이다. STEP7B는 자동 실행하지 않는다.


공식 소스: https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc_cell.py 및 https://github.com/mlech26l/ncps/blob/695ec22d7d1831f2ced67346ef7d2f08c525bd47/ncps/torch/ltc.py . 사용 기준은 설치 파일 SHA 대조이며 원격 commit과 설치 배포물의 완전한 공급망 동일성 또는 원본 논문의 과거 ncps 버전을 소급 인증하지 않는다.
