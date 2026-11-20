# STEP7BR OUTPUT_EQUIVALENCE

STEP7B-R 독립 단일 checkpoint 복구를 완료했다. 신규load1/금융forward1/완료1,기존확률float32 exact equality PASS,parameter/Python·NumPy·Torch RNG 불변 PASS. 기존99개계측은재계산/재로드하지않고원STEP7B99 PASS/1 BLOCKED도그대로보존했다. 별도versioned100개통합은퇴화24/24·비퇴화76/76이다. 이전9997프로젝트파일과원STEP7B scratch40파일 변경0. 신규학습/HMM/기존Test성능재계산/금융Bootstrap·Holm·p값/Ensemble/GPU/AMP/2026자료사용은0이다. master flags=false. 가격BOTH_UNVERIFIED,주가격PENDING,historical18시available_at UNKNOWN,production-PIT BLOCKED와역사적Test노출한계를유지한다.

identity/date/session_id/label_end/Target exact를사전에대조하고동일cohort 전체를CPU FP32 eval/no_grad로딱1회처리했다. 계측softmax확률은기존STEP5Bfloat32 배열과exact동일했다. 파라미터fingerprint와Python/NumPy/Torch RNG전후동일,forward실행중소스/가중치/입력변경0이다. 기존금융logits저장본이없어logits exact비교를주장하지않는다. 새확률로원Test파일을덮어쓰지않았고새BA/F1등Test성능을계산하지않았다.

확인일:2026-11-20 KST. 상세단일복구identity와수치는private보존.
