# STEP4B_100FIT_BASELINE_AUDIT 공개 집계 요약

국민대학교 BIT전문대학원 KOSPI200 LNN STEP4B 회고적·탐색적 CPU Train/Validation 진단이다. A/B=BOTH_UNVERIFIED, historical18:00 KST production-PIT=BLOCKED다. Validation은 checkpoint 선택에 사용돼 독립 일반화 성능이 아니다. Seed를 독립 시장 표본으로 연결하지 않았으며 결과로 가격·모델·Seed·설정을 선택하지 않았다.

기존100개 보존, 신규 완료100·실패0·BLOCKED0, 실제 누적200개다. STEP3D O3 재사용20개는 중복 집계하지 않았다. 사전95개·사후14개 검사PASS, 신규checkpoint100건 검증PASS, 기존1464파일 변경0이다. 신규2136확정epoch/97111확정optimizer updates다. 독립Test/HMM/GPU/Ensemble/외부피처/τactual/확증p값/2026 사용0이다.

기존100개 고유identity·완료·checkpoint/history/확률·입력/scaler/source/config/environment 해시를 대조했다. STEP3D alias20개 해시60건도 충돌0이다. 기존100개 재학습0이다.

공개본은 여러 Seed의 집계와 비민감 해시만 포함한다. 개별 Seed/fit 성능·epoch 이력·클래스 support·실제 Train 분위수 임계값·상세 보고서와 그림은 로컬에 보존했다. 원본 가격·일별Target·확률·weights/checkpoint는 게시하지 않았다.
