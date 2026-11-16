# STEP2.8 필수 / 확장 차단 항목과 STEP3 승인 범위

확인일 2026-11-16. **STEP3 Smoke Test: BLOCKED.** training_enabled=false, hmm_fit_enabled=false. B범주의미해결항목을F1의필수 요건으로사용하지않도록gate와코드를 분리했다. 기존72개+신규18개=90 PASS/0 FAIL. 테스트통과와실제PIT/모델lifecycle검증은구분한다.

## A. F1 실행 전 필수

|Gate|상태|남은조건|
|---|---|---|
|최종 가격 소스|BLOCKED|공식/공급처정의·개정/진위증빙과사용자의사전소스선택; A/B레이블동일은면제사유아님|
|공식달력·레이블·purge·국내입력구조|PASS|두후보의데이터전용진단수준; 최종소스선택후해시재확인|
|국내입력18:00 가용성|BLOCKED|실제공급처·과거최초 공표/개정vintage·전송/수집 지연확인; 임의시각생성금지|
|모델라이브러리구조·실행 호환|PARTIAL|설치/import/참조소스검사PASS; 실제 모델생성/forward/backward/checkpoint는미검증|
|실험사양동결|PASS(버전snapshot)|기간·모델·seed·F1·레짐·runner 해시동결; 자료 선택/최종 실행 승인보류|

A집계:2 PASS /0 FAIL /1 PARTIAL /2 BLOCKED. 이외에별도실행 승인은BLOCKED다. 실제 승인artifact는생성하지않았다. 테스트의SYNTHETIC guard fixture는실제 승인이아니며저장/실행에사용하지않는다.

## B. 특정 확장 실험 전 필요

Foreign_Net원천/단위/시장/공표시각, Nasdaq/SOX실제공급처PIT, 전체5피처, 전체Ablation, LTC τ실제forward/단위검증은BLOCKED다. 기존 원본ncps/hmmlearn버전·과거 checkpoint호환성도과거재현/해당분석에는필요하지만새 고정 환경F1의모든실행을자동차단하는조건은아니다. F1학습 gate는HMM패키지나외부변수검증을요구하지않는다.

국내종가자체PIT·가격 선택·실행호환성요건은면제하지않는다. F1이가능해지더라도전체5피처·Ablation·HMM fit·τ분석또는전체 학습까지허용된것으로해석하지않는다.

## STEP3 전에 사용자가 결정·승인할 사항

1. 출처·정의·개정증거를검토한주분석가격A/B와사전처리원칙. 필요하면둘을사전 지정민감도로관리하되Test 성능으로사후선택하지않는다.
2. t18:00·t포함계약의증빙 확정. 대안을원하면t제외/다음세션계약을새 config로명시적으로승인해야하며이번에는변경하지않았다.
3. 원본 환경동등성을주장하지않는별도F1·고정CPU참조환경과모델 실행호환성preflight범위. 미실행검사는증거 없이PASS로올리지않는다.
4. 모든필수A gate가PASS인후O1/Seed2/F1·5모델RAW/LOG·각1Train+1Validation batch·2회재현성·새로컬checkpoint만허용하는**별도STEP3 CPU Smoke 실행 승인**. Test 접근·실증 성능표·HMM fit·GPU·전체 실험·main병합은포함하지않는다.

현재 결과는증거와코드 검토용이다. STEP3승인파일은승인일/참조와config SHA-256·gate SHA-256에연결돼야한다. 설정플래그만바꾸거나누락gate를건너뛰어실행할수없도록작성했다. 모델호환성의미실행 부분에대한확인은별도 승인된preflight에서해결해야하며현재90개검사로 대체하지않는다.

공개자료는코드·해시·집계·출처/접근실패요약으로한정한다. 두날짜실제가·원자료·후보Close/Target/수치feature·checkpoint는로컬 ignored영역에만둔다. 기존Notebook/CSV/성능표/STEP1~2.7보고서/원래 config/잠금파일과JOF V14/V15/main은보존한다.
