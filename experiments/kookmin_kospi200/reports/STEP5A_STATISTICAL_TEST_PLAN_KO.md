# STEP5A_STATISTICAL_TEST_PLAN_KO

확인시각(KST): 2026-11-20T08:10:41.245073+09:00. 기존 완료500fit, 이번 신규학습0/Test 예측0/Test 성능0/금융 통계검정0/checkpoint load0/모델forward0/HMM0/Ensemble0/τactual0/GPU0/2026관측 사용0. 기존 원본·결과·모델·master flags는 보존한다. 이 문서는 준비·동결 감사이며 계획은 실행 결과가 아니다.

동결 master_statistics.py / statistics.py는 수정하지 않았다. paired moving-block bootstrap은 세션연속20/40/60,각10000회,RNG20261116. 동일 Origin 안에서 모든 모델과10Seed에 같은 날짜 indices, 각Seed 지표 후Seed평균, Origin 동일가중. probability평균으로 새Ensemble을 만들지 않는다. Seed10개가 시장 날짜를10배 늘리지 않는다.

5모델10쌍×A/B=BA20가족, Secondary4지표×20=80가족, Origin별BA5×20=100가족에 각각Holm. 각block별 별도보정하며 유리한block선택 금지. Origin별Secondary·수동/HMM레짐·τ p값가족 추가 금지. 날짜블록은 원 session_id가 실제 연속일 때만 허용하고 gap을 가로지르지 않는다.

알고리즘 감사: 기존 paired_packet은 candidate 필드/단조유일session_id 검사가 없어 혼합 가능성이 있었다. 새 STEP5A 합성 wrapper는 candidate별 입력·정렬·중복·고정10Seed·단조유일session ID를 차단검사한다. 기존 frozen 파일은 바꾸지 않았다. 실제 금융 runner는 아직 릴리스하지 않았으므로 이 wrapper가 금융 실행을 승인하지 않는다.

중요 BLOCKED: master_statistics.metric는 한 실제클래스일 때 Brier 외 BA/MacroF1/Recall0/Recall1을 전부NaN으로 처리한다. 기존 manual/evaluator 계약은 BA/MacroF1 null, **지원 있는 클래스 Recall은 정의**, 없는 클래스만null이다. 이번 합성시험에서 차이를 재현했다. 성능을 보고 정책을 고르지 말고 통계용 Recall null정책을 학습 전 계약과 일치시킬지 별도 명시/승인해야 한다. 동결masterSHA를 조용히 변경하지 않는다. 새버전/계약해시를 남긴 후 실제금융추론 전에 해소한다.

재표집무효율과 유효/무효횟수를 보존하고 >10%이면 BLOCKED,0대체/유리한재표집만선택 금지. 현재 master의 한클래스 Recall 무효율 해석도 위차이를 반영해 해결해야 한다. centered bootstrap tail fraction은 근사값이며 exact/확증적인 iid p값이 아니다. percentile95%CI는 동시CI 아님. 현재 Origin마다 독립적으로 날짜블록을 뽑는 구현은 Origin 간 공유시장/겹친endpoint/동일연도의 Train·Val 노출 의존을 제거하지 못한다. equal-Origin weighting이 독립성보장은 아니다.

합성 시험은 고정지표,20/40/60블록,동일seed 재현,짝지은index,세션gap거절,한클래스무효율차단,Holm 수치 및20/80/100가족 누락거절을 수행했다. 금융 Test 라벨/확률 읽기0, 금융통계검정0. 합성 p값을 논문 근거로 쓰지 않는다.

공개 범위: 개별500개 identity와 체크포인트/입력/소스 해시를 연결한 동결 roster 및 상세 Test job plan은 자동 공개 승인 검토에서 외부 공개가 거부되어 로컬에만 보존한다. GitHub에는 코드·집계·구조적 달력 계약·요약 보고서만 게시한다. 거부된 개별 매핑을 다른 파일명으로 재게시하지 않는다.
