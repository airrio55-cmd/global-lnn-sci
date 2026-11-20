# STEP8BR STORAGE_RECOVERY

원 STEP8B BLOCKED40·실패NPZ·승인·source·ledger를그대로보존하고독립STEP8B-R40개identity를실행했다. 새완료40/BLOCKED0,Logistic Train-only fit10,Climatology추정10,가격규칙평가20이다. 과거NN학습횟수500에Logistic/Climatology/규칙을추가하지않는다. 기존NN500/Test500·통계600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED 및 이전9799파일/STEP8B scratch46파일 변경0. NN재학습·checkpoint load/forward·HMM fit/refilter·τ추가계측·새금융Bootstrap/Holm/p값·Ensemble/GPU·2026시장관측사용0. master flags=false.

이번 결과는 retrospective exploratory benchmark다. 가격BOTH_UNVERIFIED,주가격PENDING,historical18:00 available_at UNKNOWN,production-PIT BLOCKED는storage복구로변하지않는다. O1~O4 Test와후속Validation의역사적중복,Origin·Seed·중첩label의존성을유지한다. 거래수익성·전향적일반화·통계적우월성을인증하지않으며가격/모델/Seed/threshold를사후선택하지않는다.

이전price_dates는object dtype였고allow_pickle=False가정상차단했다. 원실패파일은수정/삭제하지않았다. 새디렉터리에서float/int 금융수치와기존non-object 필드는완전히같게복사하고price_dates만명시적 `np.asarray([str(d)[:10] for d in dates],dtype="U10")`로재생성했다.

원object 필드를pickle로역직렬화하지않았다. 대신원생성코드의price-prefix index 계약과변경없는원후보CSV의동일공식session prefix를대조해canonical 날짜를복원했고기존가격수치와exact일치를확인했다. 이전object배열자체를안전하게읽었다고주장하지않는다. 현재새날짜는공식session일자및저장전canonical배열과exact일치한다. object/구조화객체/예상외필드/비유한/잘못된날짜·shape는거부한다. 수치변경·결측보정·allow_pickle=True는사용하지않았다. 동결baseline프로토콜SHA `d7ff05bdfa45691d7f2535c240dd7f522c429b521974aa7ba1b31e82eb512bf2`를유지했다.

확인일:2026-11-20 KST. 근거:원STEP8B동결사양·실패lineage,STEP8BR안전재읽기검사/실행ledger,기존STEP5BNN저장지표. 새공식가격/PIT출처검증은하지않았다.
