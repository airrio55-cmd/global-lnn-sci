# STEP8B BASELINE_RESULTS

이번 결과는 **실제 기준모형 평가 전 BLOCKED**다. 동결40개 단위 모두 입력 재읽기에서 차단됐으며 완료0/BLOCKED40, Logistic fit0/10, Climatology 추정0, 규칙 평가0이다. 성능값을0으로 만들지 않고 null/NOT_EVALUATED로 유지한다. 기존 NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED와 이전9678파일을 보존한다. NN 재학습/checkpoint load/forward, HMM fit/refilter, τ추가계측, 금융bootstrap/Holm/p값, Ensemble/GPU/2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED. 회고적 비교 승인과 실시간 인증은 구분하며 O1~O4 Test와 후속Validation의 역사적 중복/Origin·Seed·중첩label 의존성을 유지한다.

기준모형별A/B 결과: 각후보에서Climatology/Logistic/200DMA/Momentum60은각5개BLOCKED, 완료0이다. Test BA/MacroF1/Recall0/Recall1/Accuracy/Brier 및 단일예측분류는 전부NOT_EVALUATED/null이다. Train단일클래스·비수렴이관측됐다는뜻이아니며실제fit까지도달하지못했다. 결과가없는것을부정적성능/BA0으로보고하지않는다. RQ1~RQ5는모두현재단계에서판정불가다.

확인일:2026-11-20 KST. 근거:동결STEP5B/5C/6B/7B/8A보고서와저장manifest·이번실패ledger. 새공식가격/PIT증빙을확보했다고주장하지않는다.
