# STEP6A_HMM_SELECTION_GATES_KO

STEP6A는 설계·동결·정적 감사·합성 시험 단계다. 실제 금융 HMM fit/filtering, 신경망 학습·재학습, Test 재추론, checkpoint load/forward, 금융 p값·bootstrap 재실행, RAW5/LOG2 Ensemble, LTC τactual, GPU 및2026가격 사용은 모두0이다. HMM100후보/최종10개는 계획이며 학습 완료가 아니다. hmm_fit_enabled=false/hmm_filtering_enabled=false를 유지한다.

동일10개 초기화를 모든 Origin/Candidate에 적용하고, 후보별 유한한 최종 Train model.score log likelihood, 실제 수렴, 유한한 초기확률/전이/평균/공분산, 양의 정부호 공분산, Train forward hard-state 두 상태 관찰, 재현성 증거를 확인한다. 부적격 사유는 목록으로 남긴다. 적격 중 Train LL 최댓값, 정확한 동률이면 작은 seed를 선택한다. Validation/Test BA·Recall·occupancy·수익률로 고르지 않는다.

hmmlearn의 monitor.converged는 iter==n_iter일 때에도 true다. 설치된0.3.3 소스를 정적으로 확인했다. 따라서 monitor flag만으로2000회 cap 도달을 수렴으로 오인하지 않는다. 동결한 운영 해석은 finite history≥2, monitor_converged=true, **0≤마지막 LL증분<1e-4**다. 음의 증분·큰 증분·수렴 미확인은 BLOCKED이며 tol을 완화하지 않는다. 새 상태수·seed·Test median 대체·실패후 성능을 본 재학습 우회는 없다.

Train hard-state 하나만 관찰되면 후보 부적격이다. Test에서 한 상태만 관찰되는 것은 후보 선택을 다시 하는 이유가 아니며 원 상태/점유율 그대로 보고한다. Test를 보고 강제로 두 상태를 만들지 않는다.

재현성은 고정 input/source/environment/seed SHA, 고정 CPU 설정과 합성 동일 Train/seed의 파라미터 재현 증거를 연결한다. 이번 금융 실제 반복적합 검증은0이다. 예정100개 fit을 모든 후보2회씩 적합하는200개로 조용히 늘리지 않는다. 금융 반복적합 추가 증명이 필요하면 별도 예산 승인 전 BLOCKED로 유지한다. 이 미실행 부분을 금융 재현성 완료로 인증하지 않는다.

공식 코드 참고: https://github.com/hmmlearn/hmmlearn/blob/0.3.3/src/hmmlearn/base.py . 확인일2026-11-20(KST), 사용기준은 설치된 ConvergenceMonitor.converged 소스의 정적 검사이며 외부 URL을 새로 조회했다고 주장하지 않는다. 확인 한계: 현재 라이브러리 동작 설명일 뿐 금융 데이터 수렴을 보장하지 않는다.

상세 금융 input/date/checkpoint/identity 매핑과 비공개 SHA 관계는 로컬 ignored 경로에만 보존한다. 공개본은 코드·구조적 계약·합성 결과·집계·비민감 해시만 포함한다.
