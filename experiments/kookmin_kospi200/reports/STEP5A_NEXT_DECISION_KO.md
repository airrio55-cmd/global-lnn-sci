# STEP5A_NEXT_DECISION_KO

확인시각(KST): 2026-11-20T08:10:41.245073+09:00. 기존 완료500fit, 이번 신규학습0/Test 예측0/Test 성능0/금융 통계검정0/checkpoint load0/모델forward0/HMM0/Ensemble0/τactual0/GPU0/2026관측 사용0. 기존 원본·결과·모델·master flags는 보존한다. 이 문서는 준비·동결 감사이며 계획은 실행 결과가 아니다.

다음 STEP5B 승인 제안은 **설계2의 F1 A/B 병렬 회고적 Test-only 평가**에 한정한다. 이미동결500개 best checkpoint×해당Origin Test1회(500evaluation identity), CPU FP32/AMP OFF, 보존scaler transform만 사용. 학습/재학습0, HMM/GPU/RAW5·LOG2/Ensemble/Ablation/τactual/금융통계검정0,2026사용0. 실제Test 성능은 retrospective rolling-origin evaluation으로만 보고하고 가격·모델·Seed 선택에 쓰지 않는다.

실행 전에 필요한 사용자결정: (1) BOTH_UNVERIFIED/historical available_at UNKNOWN 한계가 있는 A/B병렬 회고적 평가 범위를 명시적으로 승인할지, (2) 실제Test 입력검증이PASS된500개 identity/허용읽기경로/SHA/예산에 한정한 별도approval, (3) 한클래스 Recall null정책 불일치를 어떤 계약으로 해소할지 고정. 가격/PIT 미확정 자체를 PASS로 바꾸는 승인이 아니다. source선택을Test성능에 맡기지 않는다.

회고적 Test 준비와 bootstrap 실행승인은 분리한다. 통계는 null정책/가족/의존한계 검토·동결 후 별도 승인으로만 진행한다. 사용자 승인 전에는금융Test확률생성/성능/p값계산0유지한다.

원형LNN Single=LTC_RAW5(seed+401), LTC_LOG2(seed+402), Ensemble=.5RAW5+.5LOG2. 현재 F1 LTC2(seed+401)는 두채널원형대체가 아니다. Foreign_Net 시장범위/단위/잠정·확정/발표·개정 및 Nasdaq/SOX 공급처 historical PIT 해결,채널별원형정의/추가예산/승인전실행금지. HMM도 Train-only2stateGaussian·동일초기화목록/선정·Train상태명·forwardfilter·실패시BLOCKED 계약과별도fit승인이필요하다. LTCτ actual forward도독립승인대상이다.

STEP5A 완료 후 추가금융평가를자동시작하지 않는다.

공개 범위: 개별500개 identity와 체크포인트/입력/소스 해시를 연결한 동결 roster 및 상세 Test job plan은 자동 공개 승인 검토에서 외부 공개가 거부되어 로컬에만 보존한다. GitHub에는 코드·집계·구조적 달력 계약·요약 보고서만 게시한다. 거부된 개별 매핑을 다른 파일명으로 재게시하지 않는다.
