# STEP10B 학위논문 집필·제목·RQ 함의

감사일: **2026-11-21, Asia/Seoul**. 저장소 airrio55-cmd/global-lnn-sci, 브랜치 audit/kookmin-kospi200-20261116, 프로젝트 experiments/kookmin_kospi200/.

STEP10B는 정적 코드·저장 출력·동결 결과의 비교 감사다. 금융 fit/forward/추론/모델생성/Notebook 실행/HMM fit/refilter/τ계측/bootstrap draw/p값/CI 신규계산은0이다. 기존파일과 master flags=false를 유지한다. 가격 BOTH_UNVERIFIED, primary price PENDING, historical18KST UNKNOWN, production-PIT BLOCKED와 STEP9B1R METHOD_NOT_VALIDATED도 유지한다. 2026 관측은 새로 파싱·사용하지 않으며 과거 포함 사실은 보존된 감사기록으로만 인용한다.

초기 DOCX 원본은 **BLOCKED_NOT_LOCATED**다. 문서 절·표의 내용을 Notebook로 대신 채우지 않는다. 아래 초기 코드의 확인은 사용자가 제공한3개 Notebook의 파일 내 순차실행 사양 및 저장 출력에 한정된다. 그 파일이 DOCX 집필 시 실제로 사용된 동일 버전인지는 미확인이다. 셀 번호는1부터 시작하는 실제 셀 배열 번호이며 주석 Cell번호와 다르다.

| 최종질문 | 증거에근거한답 |
| --- | --- |
| 1. 같은 연구인가? | 큰 주제는같지만동일실험은아니다. 단일구간 RAW5/LOG2 원형과5Origin F1은데이터/정보/모델구성/estimand가달라직접비교NOT_COMPARABLE이다. |
| 2. 초기1/5/10Seed 재현성? | 설정·저장로그·일부주요수치는확인된다. 동일Seed독립재학습/아카이브예측동일성·DOCX원문정합은미검증이며실패로도성공으로도단정하지않는다. |
| 3. 최신500에서 왜달라졌나? | 공식세션/기간/label/window/F1/분할/집계/loader 등여러설계차이가확인됐다. 실제수치차이의요인별인과기여는PARTIALLY_EXPLAINED이지완전분해가아니다. |
| 4. 초기LNN과최신LTC는같은가? | 제공Notebook의최종LNN은LTC이고핵심class SHA도같다. 그러나RAW5 vsF1_2와조건/가중치가다르다. CfC별도모델;원문CfC서술은DOCX없어미확인. |
| 5. 왜Ensemble 제외? | 외부피처/PIT미해결과사용자명시F1 제한/CPU scope 및후속500범위동결때문이다. 낮은Test성능때문에삭제했다는근거는없고원형검증은별도미실행. |
| 6. 무엇을주결과로? | 현재집필권고는최신STEP10을회고적F1·안정성·레짐·τ의주결과로명시하는안이다. A/B둘다보고선택금지. 원형앙상블제목/RQ유지는지도교수검토와추가근거가필요. |
| 7. 초기결과보조사용? | Historical Baseline/설계변경이력으로한계를붙여분리가능하나문서·표·코드버전확인전수치를논문원문확정값으로인용하지않는다. 결함/pooling/시점한계도병기. |
| 8. 최소bridge 필요? | 원형Ensemble추가효과가핵심RQ이면조건부필요;현재F1의기술적집필에는자동필수아님.3fit/한가격/한구간/한Seed제안이나모든gate와별도승인전예산0. |
| 9. 제목·RQ 수정? | 현재500을주근거로한다면앙상블우월성을암시하는제목은조정검토가필요하다. 실제DOCX목차/주장과교수결정전자동수정하지않는다. |
| 10. 교수님께통합결론? | 원형과최신은동일실험의재현성실패로판정할상태가아니라,추적가능한설계변경과미해결원문/출처공백이있는별도분석이다. 동일화하지않고기술·탐색결론으로통합한다. |

## 권장 집필 구조

본문은최신F1 연구의5개RQ(신경망비교,Seed/Origin안정성,레짐,LTCτ,baseline비교)를기준으로동결된결과·반대증거·가격/PIT·통계한계를기술하는안을교수검토에제시한다. 원형앙상블결과는별도Historical Baseline 절에서자료/label/분할/지표/검정한계를명시한다. 초기5Seed숫자를최신5Origin BA와동일평가표에넣어성능개선/하락이라고쓰지않는다.

제목후보는‘KOSPI200 방향성예측을위한신경망비교와 LTC 학습안정성·내부동역학분석’처럼현재증거범위를드러내는안이다. 실제학위논문제목을수정한것은아니며최종결정은원본문서확인과지도교수검토후다. ‘LNN앙상블기반’이핵심이면미실행RAW5/LOG2 검증을별도과제로정직하게남기거나추가bridge의필요성을결정한다.

초기반복Seed의분산과단일대표Seed 유의성은5개시장구간에대한확증이아니다. 최신NN간BA기각0은초기주장이틀렸다는자동증거도,모형동등성증명도아니다. 낮은τ가퇴화원인이라는표현,실시간PIT 인증, JOF다국가연구와의데이터/표혼합을하지않는다.

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
