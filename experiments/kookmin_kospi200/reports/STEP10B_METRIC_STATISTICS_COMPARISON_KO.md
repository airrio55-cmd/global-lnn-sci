# STEP10B 지표·집계·검정 증거 비교

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

| 항목 | 초기저장코드 | 최신동결 | 직접비교 여부 |
| --- | --- | --- | --- |
| 성능 estimand | 단일Test, seed별metric mean±np.std(ddof0) | Origin별10Seed metric평균 후5Origin동일가중;Seed SD는ddof1 | NOT_COMPARABLE;기간·분모·집계다름 |
| BA/Accuracy | sklearn accuracy/balanced_accuracy | 동일 기본정의 | 같은정의라도다른날짜/Target은동일성능비교아님 |
| F1/Recall | Macro F1 별도, F1/Recall 기본positive1 | MacroF1·Recall0/1·Brier등분리 | PositiveF1과MacroF1 혼동금지 |
| 빈/한클래스 | 빈배열0벡터;zero_division0;BA한클래스정책미명시 | 빈/실제한클래스 BA/F1=null,unsupportedRecall=null | 레짐의유효분모 달라짐;0으로대체안함 |
| Ensemble/Seed mean | 같은Seed RAW/LOG확률 .5/.5;뒤에seedmetric평균 | 확률ensemble없음;Seedmetric평균만 | 확률평균과metric평균 불일치 |
| 단일 McNemar | LNN Ensemble기준,저장첫Seed,연속성보정χ²근사,10비교미보정 | NN5모델 모든쌍×A/B BA20가족 | 모델쌍·가설부터다름 |
| 다중 McNemar | 동일정답을Seed수만큼연결;exact binomial+Bonferroni/BH | date paired MBB,20/40/60블록,10000반복,Holm | 독립성/추론단위/검정대상다름 |
| HMM/수동 레짐 | Test30/70,Test전체Viterbi,Test상태명·fallback | Train-only q30/q70·HMM selection·forwardfilter | 층화기준도다름;레짐결과끼리도비동등 |

McNemar의paired correctness discordance는 오분류확률/Accuracy 차이에 관한 가설이며 BA차이의검정이아니다. 강한유의성을BA우월성또는5Origin재현으로확대할수없다. 다중Seed코드는정답을여러번복제해연결하므로 시장관측이늘어나지않는데도표면행수가늘어난다. exact binomial·Bonferroni/BH는 날짜/20D중첩·Seed의종속성을자동으로수리하지않는다. DOCX의‘대표Seed McNemar’와현재5Seed Notebook의pooled검정이같은표인지도원문없어확정불가다.

최신STEP5C는20/40/60별Primary BA20 기각0/0/0,Origin BA100 기각0/0/0,Secondary80 기각3/2/3이다. 기존600행을재계산하지않고저장summary로인용했다. 블록별같은가설은독립재현이아니며비유의는동등성/무효과증거가아니다. 이전McNemar p값과크기대조로어느연구가더옳다고판정하지않는다.

최신방법도완전한확증으로인증하지않는다. 20D중첩label·시계열자기상관·희소class·Origin간과거Test/후속Validation노출·반복Seed 의존성문제가남고STEP9B1R은METHOD_NOT_VALIDATED다. 기존STEP5C는EXISTING_APPROX_INFERENCE이며새NN-baseline STEP9B2는NOT_EXECUTED/NOT_TESTED다. 이번신규p값·CI·bootstrap draw는0이다.

## 증거 연결

| ID | 증거 | 위치 | 사용 범위·한계 |
| --- | --- | --- | --- |
| E01 | 초기 원본3 Notebook | originals의 단일/5개/10개시드 Notebook; 셀3,5~18 | 현재 파일 SHA·셀 source SHA와 저장출력 정적 확인; 재실행 아님 |
| E02 | 원형 데이터 분할의 과거 data-only 진단 | evidence/data_only_checks.json#/splits, /boundary_checks; reports/AUDIT_KO.md | 현재첨부CSV+코드에 대한 이전 진단; DOCX 실제기간으로 소급확정 불가 |
| E03 | 출처·정밀도·세션·label 이력 | STEP27_FULL_PRICE_AUDIT_KO, STEP28_DATA_DECISION_KO, STEP10A_PRICE_PROVENANCE_AUDIT_KO | 공급처/PIT 미확정; 가격·배열 재계산 없음 |
| E04 | 최신 고정모델·데이터 계약 | configs/step3c_master_experiment_config.json; STEP3C_MASTER_PROTOCOL_KO; runtime/step3b_worker.py, step3c_worker.py | FocalLoss와 최종모델 AST정의 SHA 일치; 실제금융함수 실행 없음 |
| E05 | 500학습 및 동결 Test | STEP4D/STEP5A/STEP5B 보고서·실행summary; step5b_public_aggregate_summary.json | 학습500/Test500, 가격·Origin별 저장지표와 날짜수 읽기만 |
| E06 | 최신 추론·반대증거 | step5c_execution_summary.json#/families; STEP10_STATISTICAL_EVIDENCE_KO; STEP9B1R_EXECUTION_READINESS_KO | 기존600행 및 기각수 보존; 새p값/Holm 없음 |
| E07 | 최종 성능과 기준모형 | step8br_public_aggregate_summary.json#/candidate_primary; STEP10_FROZEN_RESULT_TABLES_KO | 이미 동결된 다중Origin 요약만 인용; 상세 금융표 공개거부 범위 재게시 안함 |
| E08 | F1 제한·Ensemble 별도계약 | STEP28_F1_READINESS_KO, STEP29_READINESS_KO, STEP3A_EXECUTION_AUDIT_KO, STEP3C_LNN_ENSEMBLE_PLAN_KO | 새500결과 이전 F1 범위 문서·승인 이력; 미실행 RAW5/LOG2 계획과 구분 |
| E09 | 초기 DOCX 검색 | 로컬 workspace 파일검색; GitHub main/audit 고정head 재귀tree; 기본브랜치 텍스트검색 | DOCX 미확보; 현재2개 branch tree는 비잘림; 전체과거/외부보관소 부재를 증명한 것은 아님 |
| E10 | STEP10 freeze 및 최신 source/PIT | STEP10_MASTER_AUDIT_KO, FINAL_EXPERIMENT_INVENTORY, RQ_CONCLUSION_MATRIX, STEP10A 5보고서 | 내부무결성 동결과 과학적/PIT 인증은 별개 |
