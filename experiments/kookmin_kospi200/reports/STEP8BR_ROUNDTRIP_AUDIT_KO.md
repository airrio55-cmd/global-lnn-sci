# STEP8BR ROUNDTRIP_AUDIT

원 STEP8B BLOCKED40·실패NPZ·승인·source·ledger를그대로보존하고독립STEP8B-R40개identity를실행했다. 새완료40/BLOCKED0,Logistic Train-only fit10,Climatology추정10,가격규칙평가20이다. 과거NN학습횟수500에Logistic/Climatology/규칙을추가하지않는다. 기존NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED 및 이전9799파일/STEP8B scratch46파일 변경0. NN재학습·checkpoint load/forward·HMM fit/refilter·τ추가계측·새금융Bootstrap/Holm/p값·Ensemble/GPU·2026시장관측사용0. master flags=false.

이번 결과는 retrospective exploratory benchmark다. 가격BOTH_UNVERIFIED,주가격PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED는storage복구로변하지않는다. O1~O4 Test와후속Validation의역사적중복,Origin·Seed·중첩label의존성을유지한다. 거래수익성·전향적일반화·통계적우월성을인증하지않으며가격/모델/Seed/threshold를사후선택하지않는다.

명시적schema는9필드다: train_x/test_x float64(N×2/M×2),train_y/test_y int64(N/M),session_id int64(M),price_close float64(K),dates/label_end U10(M),price_dates U10(K). source schemaSHA는execution manifest에있다.

각새NPZ는임시파일을exclusive 생성→flush/fsync→SHA기록→allow_pickle=False로모든9필드를실제읽기→dtype/shape/finite/날짜/session 검증→저장전배열과모든필드exact비교→SHA불변검사후최종경로로atomic rename했다. 10코호트90필드가PASS했고worker에서도다시전체안전재읽기했다. 헤더검사만으로통과시키지않았다. 원실패파일과새파일은별도경로/roster에있으며원40BLOCKED를완료로바꾸지않았다.

확인일:2026-11-20 KST. 근거:원STEP8B동결사양·실패lineage,STEP8BR안전재읽기검사/실행ledger,기존STEP5BNN저장지표. 새공식가격/PIT출처검증은하지않았다.
