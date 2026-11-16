# STEP2.6 종가 대조·보완

확인일: 2026-11-16 KST. 기준 commit: `ea94ddc242fbd07c8ae0aa4f7a99df020e2824b6`. STEP1·STEP2·STEP2.5의 보고서, 코드, manifest를 먼저 확인했다. 원본과 과거 결과를 보존했으며 모델·HMM 학습, GPU, 실제 모델 forward는 실행하지 않았다.

## 입력 파일과 대조 범위

| 파일 | 실제 존재 | 검증 결과 |
|---|---|---|
| KOSPI 200 종가.xlsx — 전체 자료 | **없음** | **BLOCKED** |
| KOSPI200_누락45일_종가_보완.csv | 있음 | 45행, 날짜·가격 검사 PASS |
| KOSPI200_누락45일_종가_보완.xlsx | 있음 | 45행, CSV와 날짜·가격 일치 |

/workspace의 첨부·라이브러리·공유·작업 영역에서 전체 Excel을 찾지 못했다. 보완 Excel의 ‘출처 및 검증’ 시트에는 전체 파일 이름, 3939행, 코드 I.101/I31000040F라는 서술이 있지만 그 서술을 실제 파일의 존재나 검증으로 간주하지 않았다. **전체 Excel 업로드가 필요하다.** 전체 Excel의 총 거래일 수, 중복·정렬·가격 품질, 3939세션 완전성은 현재 미확인이다.

신규 Excel과 공통3894일의 가격 비교는 **수행0건**이며 가격충돌 건수는 **UNKNOWN(null)**이다. ‘0건 충돌’ 또는 ‘전부 일치’가 아니다. `manifests/kospi_price_reconciliation.csv`는 3894개 날짜를 BLOCKED_FULL_EXCEL_MISSING으로 기록하고, 새 가격·차이를 비워 둔다. 실제 파일이 제공되면 시트와 날짜·종가 열을 명시적으로 지정해 exact, 1e-9 허용오차, 소수2자리 일치를 각각 대조하도록 구현했다. 신규 Excel도 자동 정답으로 취급하지 않고 가격 차이를 별도 기록한다.

## 실제 수행한 45일 보완

보완45일은 STEP2.5 누락감사45일과 정확히 같고 모두 공식 KRX 세션이다. 기존3894일과 겹치지 않는다. CSV와 XLSX는 동일 데이터의 두 표현으로 검사했고, **CSV만 한 번 병합**했다. 중복·종가 결측·비유한값·0이하·기간 밖 관측은0개이며 날짜는 오름차순이다.

원본의2026년41행을 먼저 제외하고 기간 내3894개 종가를 그대로 보존한 뒤45개만 추가했다. 파생파일 `data/derived/kospi200_close_completed_2010_2025.csv`는3939행으로 공식 세션과 일대일 일치하며 종가 결측은0개다. OHLC·Volume은 생성하지 않았다. 필드는 Date, Close, source_type, source_file, original_or_supplement, verified_session, source_sha256이다.

보완값 상태는 **USER_SUPPLIED_VERIFIED_MATCH**다. 이는 사용자 CSV/XLSX·누락날짜·거래일의 정합성을 확인했다는 뜻이며 KRX 공식 가격 인증이 아니다. 기존값은 USER_SUPPLIED_ORIGINAL_PRESERVED로 보존했다. KRX_OFFICIAL_VERIFIED로 표시한 가격은0개다. 공급처·공식 원천URL·추출일·수정정책은 아직 UNKNOWN이다.

입력 두 파일의 바이트 수·SHA-256, 출처 시트의 주장과 한계는 `step26_cutoff_label_audit.json`에 기록했다. 공식 달력의 출처와 해시는 기존 `provenance/krx_calendar_provenance.json`을 사용하며, 달력 PASS를 가격 원천 PASS로 확대하지 않는다.

## 공개 범위와 보존

라이선스·공급처가 미확정이므로 사용자 원본, 보완45일 가격, 완성 종가, 전체 일별 Target·수치 피처는 로컬 data/user_supplied·data/derived에 보존한다. 공개 GitHub에는 코드, 날짜·상태 감사, 집계와 해시만 게시한다. `.gitignore`와 명시적 게시 목록으로 원자료·파생가격을 제외한다. 실제 가격 충돌이 발견되면 원본값·신규값·차이가 있는 상세표는 로컬에 보존하고 공개 요약과 분리한다.

검사52개는 PASS, FAIL0이며 실자료/공개 범위 gate7개는 BLOCKED다. 전체 Excel이 없을 때 올바르게 차단하는 기능검사의 PASS는 실제 Excel 검증 완료를 뜻하지 않는다.
