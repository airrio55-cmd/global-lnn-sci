# STEP6B_FORWARD_FILTER_AUDIT_KO

회고적 HMM 상태 분해와 고정 Test 예측의 기술적 분석이다. HMM 후보 실제fit100/100, 적격100, 부적격0, 실패0, 최종선택/순차filtering10/10, 연결한 기존신경망Test500/500이다. HMM은 새 신경망이 아니며 기존NN500fit에 더하지 않는다. 신경망학습·재추론/checkpoint forward,새금융bootstrap/Holm/p값,RAW5·LOG2 Ensemble,GPU,τactual,2026사용은모두0이다.

고정theta_Train에서 p(z_t|x_1…x_t,theta_Train)을log-stable forward로계산했다. 전체Viterbi/smoothing은사용하지않았다. Trainposterior는각후보적격성검사에서100회계산됐고,선택된각HMM은마지막유지Train posterior부터연속관측을1회씩전파해10개cohortcontinuation을완료했다.

Train말단purge20관측과전체Validation(말단label purge포함),Test전체공식세션을누락없이연결했다. 첫후속session_id=마지막Train+1이며모든차분1,중복/누락0을확인했다. Test시작posterior재초기화0이다. filtering전후파라미터동일·posterior유한/정규화·공식날짜정렬검사를통과했다.

관측빌더는각Origin의Test연도마지막관측까지가격prefix만숫자로읽었다. HMM에는Target확인용다음해미래종가가필요하지않으므로그구간을읽지않았다.2025말단20세션도상태관측은있지만NN레짐평가는원래knownTarget기준일만사용해제외했다.2026관측0이다.

Forward코드의미래변형불변성/bridge누락거절/순차연결동등성은동결합성24검사에서확인했다. 금융파라미터를고정해관측을순차계산했으며미래관측으로과거posterior를재추정하지않았다. 단,theta자체는전체허용Train에서학습한조건부경로이고과거Train상태를전향적PIT예측으로주장하지않는다.

A/B BOTH_UNVERIFIED, historical available_at UNKNOWN, production-PIT BLOCKED, primary price PENDING을 유지한다. O1~O4 Test의 후속 Validation 노출 한계를 인정하며 이 결과를 전향적 미관측시장/PIT 인증으로 주장하지 않는다.

개별 Train 날짜/행 수/input·scaler·HMM parameter·posterior·Test Target/확률/identity·SHA 매핑은 ignored private에만 보존했다. 공개본은 여러fit/Origin의 집계·구조적 방법·비민감 해시만 포함한다. n/support0/support1의 개별 상세표는 private 감사자료에 있다.
