# STEP5B_NEXT_GATES_KO

회고적 Rolling-Origin F1 A/B Test-only 평가. 기존500fit 보존; 실제완료500, 실패0, BLOCKED0. 신규학습/재학습0, HMM0, Ensemble0, GPU0, τactual0, 금융bootstrap/Holm/p값0,2026관측 사용0. A/B BOTH_UNVERIFIED, historical available_at UNKNOWN, production-PIT BLOCKED, 주가격 PENDING이다. Validation으로선택한best checkpoint를고정해사용했으며Test결과로사양·모델·Seed·가격을바꾸지않았다.

이번승인은500개F1 A/B회고적Test평가와기술집계까지만이다. STEP5B종료후추가실험을자동시작하지않는다. 가격/PIT미확정은사용자승인으로PASS가되지않는다.

후속STEP5C는실제공개된Test결과를보고가설/가족/검정법을바꾸지않고,사전bootstrap20/40/60·각10000·seed20261116·Seed별지표후평균·Origin동일가중·Holm20/80/100가족을유지해야한다. 한클래스Recall의versioned평가정책을통계용metric에도명시적으로연결·검증하고,동일날짜indices/model/seed/A-B분리/session연속성·무효재표집율>10%BLOCKED를사전검사한뒤별도승인필요다. 이번financialbootstrap/Holm/p값은0이며Test확률/label/date/session은후속검사용ignoredprivate에보존했다.

HMM Train-only2stateGaussian/초기화목록/선정/상태명/실패BLOCKED/forwardfiltering과별도승인이필요하며현재HMM0이다. RAW5/LOG2 LNN원형Ensemble은Foreign_Net정의·공급처·가용성및Nasdaq/SOX PIT,채널별별도모델학습예산과승인없이시작하지않는다. 현재F1 LTC2(seed+401)는LTC_RAW5/LOG2(+402)대체아니다.τactual forward도별도승인전0유지한다.

회고적Test결과가독립전향적확증이나실시간투자성능을뜻하지않는다. 지표차이/퇴화/Origin·가격민감성모두함께보고하고성능에따라model/Seed/price/threshold를선택하지않는다.
공개 범위: 다중 fit 집계만 포함한다. 개별identity/checkpoint/input매핑·일별확률/Target·원가격·실제scaler/Train임계값·개별상세지표·레짐classsupport는ignored로컬에보존한다. 원본/기존보고서/논문표/main/JOF는변경하지않았다.
