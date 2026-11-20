# STEP8A DEGENERACY_TAU_STRATIFIED

이번 단계는 저장 결과·checkpoint-level τ 요약의 읽기 전용 감사와 기술통계/설계다. checkpoint는 byte SHA만 대조하며 역직렬화·forward하지 않았다. NN500·Test500·STEP5C600행·HMM100후보/최종10·τ99 PASS/1 BLOCKED를 보존한다. τ 전체 분류는 퇴화24/100, 유효 퇴화23개/사용23개, 비퇴화76/76, 전체99/100이다. 기존 확률 exact99개를 유지하고 중단1개를 재시도·대체·0채움하지 않았다. 신규 NN/기준모형 학습·checkpoint load/forward·Test 재생성·HMM fit/refilter·τ추가계측·금융bootstrap/Holm/p값·Ensemble·GPU·2026시장관측 사용0. master flags=false. 가격 BOTH_UNVERIFIED, historical18KST available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING. O1~O4 Test와 후속 Validation의 역사적 중복 및 Origin/Seed/뉴런/window 의존성을 유지한다.

checkpoint별 solver-substep τ_effective median을 하나의 요약값으로 사용했다. 전체 평균은 퇴화 0.02909928, 비퇴화 0.04902215, 차이 -0.01992287다. 이것은 p값/인과 추정이 아니다.

|구분|퇴화 n|비퇴화 n|방향/판정|
|---|---:|---:|---|
|O1|12|8|D_LOWER|
|O2|6|14|D_LOWER|
|O3|1|18|SMALL_CELL_PRIVATE|
|O4|4|16|D_LOWER|
|O5|0|20|NOT_COMPARABLE|

|구분|퇴화 n|비퇴화 n|방향/판정|
|---|---:|---:|---|
|A|12|38|DESCRIPTIVE_ONLY|
|B|11|38|DESCRIPTIVE_ONLY|

|구분|퇴화 n|비퇴화 n|방향/판정|
|---|---:|---:|---|
|2|0|10|NOT_COMPARABLE|
|12|5|4|D_LOWER|
|22|0|10|NOT_COMPARABLE|
|32|2|8|D_LOWER|
|42|2|8|D_LOWER|
|52|4|6|D_LOWER|
|62|0|10|NOT_COMPARABLE|
|72|4|6|D_LOWER|
|82|4|6|D_LOWER|
|92|2|8|D_LOWER|

|구분|퇴화 n|비퇴화 n|방향/판정|
|---|---:|---:|---|
|O1/A|6|4|D_LOWER|
|O1/B|6|4|D_LOWER|
|O2/A|3|7|D_LOWER|
|O2/B|3|7|D_LOWER|
|O3/A|1|9|SMALL_CELL_PRIVATE|
|O3/B|0|9|NOT_COMPARABLE|
|O4/A|2|8|D_LOWER|
|O4/B|2|8|D_LOWER|
|O5/A|0|10|NOT_COMPARABLE|
|O5/B|0|10|NOT_COMPARABLE|

10개 Origin×Price 중 양군 유효 τ가 공존하는 셀은 7개이고 모든 공존셀에서 평균 차이 D−N은 음수다. 그중 양군 n≥2인 셀은 6개다. O3의 퇴화 유효 τ는1개로 세부값/차이를 공개하지 않으며 private에 보존한다. O5에는 퇴화군이 없어 집단 차이를 계산하지 않는다. Origin별 평균·중앙값·범위는 공개JSON(단일모델은억제)과 private 원표에 있다.

공통지지 셀에 제한한 pooled 차이 -0.01476266 = 대칭적 within-cell 항 -0.01270112 + 구성 항 -0.00206154. 이는 관측 평균의 산술 항등식이다. 동일 셀 가중 평균 차이는 -0.01337540다. 전체10셀의 구성 독립 효과는 **NOT_IDENTIFIABLE**: 한군 없는 셀의 반사실 값을 만들지 않았다. 구성만으로 차이가 완전히 사라진다고도, τ 독립효과가 입증됐다고도 할 수 없다.

Seed의 Origin별 퇴화 집중표와 중단 identity의 Origin/Price/Seed/분류는 ignored private에만 보존한다. B후보의 퇴화1개 누락으로 A/B·Origin/Seed 구성은 대칭이 아니며 MCAR로 간주하지 않는다. 알려진 중단 원인은 UNKNOWN이다. 퇴화 유효23개를 원래24개의 완전대표로 일반화하지 않고 민감도 범위/누락값을 임의 생성하지 않았다. 재실행에는 새 사용자 승인·추가 예산이 필요하다.


확인일 2026-11-20 KST. 근거: 보존 STEP4D/5B/5C/6B/7B 보고서·execution manifest 및 checkpoint-level 요약. 신규 공식 원천확인·금융실험은 수행하지 않았다.

Seeds2·22·62에는 유효 퇴화 τ가 없어 군간 차이는 계산하지 않았다. Seed12는 τ가 유효한9개 중 퇴화5개이며 다른 여러Seed에도 퇴화가 분포한다. Origin×Seed 집중도와 중단 원분류 상세는 private 구성표에서 확인했다. 동일Seed 내에서도 Origin·가격이 달라 공동요인을 분리한 효과로 해석할 수 없다. 두모델만 있는 공개군은 개별 최솟값/최댓값/SD를 억제하고 평균·중앙값만 공개했다.

공개 분할군 수치를 전체 평균에서 빼 단일모델 값을 역산하지 못하도록 Origin·Seed·Origin×Price의 퇴화군 수치와 gap은 보완억제했다. 해당 평균·중앙값·범위·차이는 모두 ignored private 원표에 보존하며 공개표는 모델 수와 확인된 방향만 제공한다. 가격별 다중모델 집계 및 전체 산술 분해는 공개JSON에 있다.
