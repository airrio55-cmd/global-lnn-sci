# STEP8B BASELINE_PREFLIGHT

이번 결과는 **실제 기준모형 평가 전 BLOCKED**다. 동결40개 단위 모두 입력 재읽기에서 차단됐으며 완료0/BLOCKED40, Logistic fit0/10, Climatology 추정0, 규칙 평가0이다. 성능값을0으로 만들지 않고 null/NOT_EVALUATED로 유지한다. 기존 NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED와 이전9678파일을 보존한다. NN 재학습/checkpoint load/forward, HMM fit/refilter, τ추가계측, 금융bootstrap/Holm/p값, Ensemble/GPU/2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, 주가격PENDING, historical18KST available_at UNKNOWN, production-PIT BLOCKED. 회고적 비교 승인과 실시간 인증은 구분하며 O1~O4 Test와 후속Validation의 역사적 중복/Origin·Seed·중첩label 의존성을 유지한다.

메모리 내 데이터 검사1089개와 독립합성14개는통과했다. 공식KRX3939session/hash, A/B가격prefixSHA,Train+Test Target의정확20session endpoint,Train purge,200DMA200관측·Momentum61관측warmup,중복/결측/비유한차단,기존NN500개와Test날짜/Target/session/label_end일치,기존F1현재t피처일치와Train피처미래변경불변을확인했다. 시장데이터warmup과PIT공급처가용성은구분하며후자는UNKNOWN이다.

**중대한 누락:** 저장된NPZ를allow_pickle=False로전필드다시읽는gate가승인전에빠졌다. `np.array(DatetimeIndex.strftime(...))`로생성한파생`price_dates`가object dtype였다. 실제worker의안전한재읽기가이를거부했다. 사후헤더검사로10개코호트모두실패를재확인했고그각4모형=40단위를BLOCKED로유지했다. in-memory1089 PASS를전체financialGate PASS로해석하면안된다. 실패gate는PASS로바꾸지않았다.

수정안은price_dates를명시적UnicodeU10으로저장하고모든필드header+안전재읽기+날짜/session/Target/F1 SHA gate를승인전에추가하는것이다. 새storage gate의합성3개는PASS지만이는기존금융입력gate의PASS가아니다. 새입력생성/원40단위재실행은0이며원실패입력·승인·에러를보존한다.

확인일:2026-11-20 KST. 근거:동결STEP5B/5C/6B/7B/8A보고서와저장manifest·이번실패ledger. 새공식가격/PIT증빙을확보했다고주장하지않는다.
