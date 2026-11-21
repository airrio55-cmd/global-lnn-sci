# STEP13 검색·보존·공개 실행 감사

확인일·검색 상한: **2026-11-21, Asia/Seoul**. Repository `airrio55-cmd/global-lnn-sci`, Branch `audit/kookmin-kospi200-20261116`, Project `experiments/kookmin_kospi200/`.

STEP13은 문헌 검색과 기존 근거의 논증 정리다. 새 금융 fit/forward/evaluation·HMM·τ 계측·bootstrap draw·p값/CI는 모두0이다. master 실행 flags=false, 기존 NN500/Test500·Baseline40·HMM100중선택10·STEP5C600·τ100을 유지한다. 연구기간2010-01-01~2025-12-31 및2026 시장 관측 사용 금지는 그대로다. 2026년 **학술문헌**을 읽는 것은2026 시장 관측을 실험에 입력하는 것과 다르다. JOF 연구와 혼합하지 않는다.

가격 **BOTH_UNVERIFIED**, primary **PENDING**, historical18KST available_at **UNKNOWN**, production-PIT **BLOCKED**, Primary BA 우월성 미확립, 통계방법 **METHOD_NOT_VALIDATED**, baseline 통계 비교 **NOT_TESTED**를 유지한다. 문헌의 주장이 현재 연구의 미검증 상태를 PASS로 만들지는 않는다. 제목·기여는 교수 승인 전 검토안이다.

## 실제 수행

사용자 지정 기존8개 보고서와 STEP13 요청 전문을 읽었다. 기존 결과에서 수치를 새로 생성하지 않고 STEP10~12의 동결 사실을 인용했다. 공개 웹 검색·공식 출판사/학회·KCI·기관 저장소·Crossref로 문헌을 확인하고33개 서로 다른 논문을 후보 등록했다.18편 전문을 실제 확보해 관련 절을 비교했고15편은 서지/초록 등 제한 검토로 남겼다. 원문 접근 실패·challenge·구독 preview를 전문 검토로 표시하지 않았다.

문헌 원응답·PDF/HTML·관련 텍스트·접근상태/URL/확인일·SHA는 비공개 로컬에 보존했다. 공개 보고서에는 서지·근거 위치·제한된 한국어 요약만 작성했다. 논문 전문·장문 인용·첨부 식별자·비공개 파일 경로는 게시하지 않는다. 검색 결과의 블로그/특허/동음이의 CFC는 검증 논문으로 세지 않았다. 이번 접근이 포괄적 systematic review나 최초성 인증은 아니다.

## 제한 준수

| 항목 | 실행 범위 |
| --- | --- |
| 신규 금융 fit/forward/evaluation |0/0/0 |
| 신규 HMM/τ measurement |0/0 |
| 신규 bootstrap draw/pvalue/CI |0/0/0 |
| 금융 원자료/예측배열·checkpoint 수치 읽기 | 없음; 문헌/기존 보고서만 사용 |
| 기존 NN500/Test500/Baseline40/HMM100선택10/STEP5C600/τ100 | 보존, 재계산0 |
| master training_enabled/hmm_fit_enabled/new_fit_execution_enabled | false 유지 |
| 새로운 project 산출물 | 요청한 STEP13 보고서12개만 |
| 기존 파일 시작 snapshot |10126개; byte SHA-256 일치·변경/삭제0 확인 |
| main/JOF/초기원문·Notebook/기존보고서 수정 |0 |
| 교수 발송·승인/후속 금융 자동실행 |0 |

검색 기간의2026 출판물은 문헌으로만 읽었으며 시장관측을 모델/검정에 사용하지 않았다. Crossref13응답 성공/13실패와 DOI미사용7편을 구분했다. 서지의 DOI 존재는 해당 연구의 과학적 타당성 인증이 아니다.

문서 범위·서지/실제 전문 확보·용어·제약 유지·민감정보 제외·보존 검사 **52개 PASS / FAIL0**을 확인했다. 이 문서 검사는 금융 검정 타당성·최초성·학위 충분성의 PASS가 아니다.

## Git 공개 계약

현재 audit 브랜치 head와 main SHA를 기록하고, 허용12개 신규 보고서의 staged bytes와 민감정보 제외를 확인한다. branch head를 새로 읽어 expected_sha로 보호하여 commit/push하고 원격 diff가12개뿐인지 재확인한다. 상세 문헌 다운로드·비공개 inventory·기존 denied 금융 자료를 대신 게시하지 않는다. commit SHA·최종 검증은 최종응답 및 외부 로컬 영수증에 남긴다.

## 근거 사용 규칙

L번호의 서지·DOI·URL·확인 범위는 [검증 서지](STEP13_VERIFIED_BIBLIOGRAPHY_KO.md), 항목별 비교는 [선행연구 비교](STEP13_PRIOR_ART_COMPARISON_KO.md), 검색 범위·접근 실패는 [검색 프로토콜](STEP13_LITERATURE_SEARCH_PROTOCOL_KO.md)에 기록했다. NR은 확인한 관련 절에 보고가 없다는 제한된 뜻이며 원문 미확보 항목은 UNKNOWN이다. 검색 미발견을 선행연구의 전 세계적 부재나 최초성 증명으로 해석하지 않는다. 기존 실증 근거는 STEP10/10C/11/12 보고서를 따르고 새로 계산하지 않았다.
