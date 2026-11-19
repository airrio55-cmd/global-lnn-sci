# STEP4D_NEXT_GATES 공개 집계 요약

국민대학교 BIT전문대학원 KOSPI200 LNN STEP4D 회고적·탐색적 CPU Train/Validation 진단이다. A/B=BOTH_UNVERIFIED, historical18:00 KST production-PIT=BLOCKED다. Validation은 checkpoint 선택에 사용돼 독립 일반화 성능이 아니다. Seed를 독립 시장 표본으로 연결하지 않았으며 결과로 가격·모델·Seed·설정을 선택하지 않았다.

실제 누적500개 완료, 전체500개 계획 대비 남은F1 fit0개다. 전부성공한경우만500완료/F1잔여0으로보고한다. 추가fit·Test·HMM·Ensemble은자동시작하지않는다. [가격/PIT] 공급처·정의·개정·historical18:00가용성증빙이필요하다. [RAW5/LOG2 LNNEnsemble] 현재F1과구분하며외부피처PIT·채널/같은Seed앙상블사양·추가예산동결및별도승인이필요하다. [HMM] Train-only2state선정·초기화·상태명·실패정책·forwardfiltering과별도fit승인이필요하다. [독립Test/확증검정] 날짜/label/purge·출처·입력가용성·모델과확률추출사양·별도실행승인이필요하다. 과거Test연도가후속Validation으로관찰돼전향적미관측holdout이라고주장하지않는다. bootstrap20/40/60·10000회·seed20261116·Holm20/80/100은보존했고계산0이다.

공개본은 여러 Seed의 집계와 비민감 해시만 포함한다. 개별 Seed/fit 성능·epoch 이력·클래스 support·실제 Train 분위수 임계값·상세 보고서와 그림은 로컬에 보존했다. 원본 가격·일별Target·확률·weights/checkpoint는 게시하지 않았다.
