# STEP7BR TAU_RECOVERY_RESULTS

STEP7B-R 독립 단일 checkpoint 복구를 완료했다. 신규load1/금융forward1/완료1,기존확률float32 exact equality PASS,parameter/Python·NumPy·Torch RNG 불변 PASS. 기존99개계측은재계산/재로드하지않고원STEP7B99 PASS/1 BLOCKED도그대로보존했다. 별도versioned100개통합은퇴화24/24·비퇴화76/76이다. 이전9997프로젝트파일과원STEP7B scratch40파일 변경0. 신규학습/HMM/기존Test성능재계산/금융Bootstrap·Holm·p값/Ensemble/GPU/AMP/2026자료사용은0이다. master flags=false. 가격BOTH_UNVERIFIED,주가격PENDING,historical18시available_at UNKNOWN,production-PIT BLOCKED와역사적Test노출한계를유지한다.

실제20 observation-entry와각6개ODE substep을수집했다. entryτ와substep0 exact일치,128뉴런shape·finite positive τ·hidden update연속성·최종hidden일치를검사했다. τ_raw=positive(cm)/positive(gleak),τ_eff=positive(cm)/(positive(gleak)+sensory합+recurrent합)이며constraints=True의positive를정확1회적용했다. cm_t는적분항이며τ분모에더하지않았다. 단위model_observation_step,초/경제기억/Jacobian고유시간아님. rawτ는모델당1회,같은sensory합은6step exact일치확인후관측당저장하고recurrent/hidden/effτ는모든실제substep에보존했다. 실제단일τ/hidden/확률/metadata는ignored private에만저장한다.

확인일:2026-11-20 KST. 상세단일복구identity와수치는private보존.
