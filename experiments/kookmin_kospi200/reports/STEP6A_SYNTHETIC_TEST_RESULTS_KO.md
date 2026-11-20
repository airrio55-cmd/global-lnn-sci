# STEP6A_SYNTHETIC_TEST_RESULTS_KO

STEP6A는 설계·동결·정적 감사·합성 시험 단계다. 실제 금융 HMM fit/filtering, 신경망 학습·재학습, Test 재추론, checkpoint load/forward, 금융 p값·bootstrap 재실행, RAW5/LOG2 Ensemble, LTC τactual, GPU 및2026가격 사용은 모두0이다. HMM100후보/최종10개는 계획이며 학습 완료가 아니다. hmm_fit_enabled=false/hmm_filtering_enabled=false를 유지한다.

합성/구조 시험 24 PASS / 0 FAIL. 실제 hmmlearn GaussianHMM으로 동일 합성 Train 두 번 적합과 holdout 변경 후 같은 Train 적합을 수행해 총3개 합성 fit을 실행했다. 실제 금융 HMM fit/filter는0이다. GaussianHMM 설정은 동결된2state/full/2000/tol1e-4/mincov1e-4, seed2이며 후보선택/부적격 검사는 추가 fixture로 시험했다. 합성 데이터는 시장 데이터나 실제 성능을 모사한다고 주장하지 않는다.

| 합성 검사 | 결과 |
| --- | --- |
| test_01_actual_synthetic_fit_reproduces_parameters | PASS |
| test_02_holdout_changes_do_not_refit_Train | PASS |
| test_03_future_perturbation_past_posterior_exact | PASS |
| test_04_forward_is_not_smoothing | PASS |
| test_05_bridge_transition_omission_detected | PASS |
| test_06_state_label_permutation_preserves_economic_names | PASS |
| test_07_nonpositive_covariance_blocked | PASS |
| test_08_nonconvergence_and_maxiter_not_accepted | PASS |
| test_09_train_one_state_collapse_blocked | PASS |
| test_10_all_candidates_invalid_no_fallback | PASS |
| test_11_tie_selects_smallest_seed | PASS |
| test_12_AB_input_mixing_rejected | PASS |
| test_13_Origin_future_boundary_and_Train_dates | PASS |
| test_14_empty_and_one_actual_class_null_policy | PASS |
| test_15_same_predictions_regime_n_sum | PASS |
| test_16_duplicate_missing_nonmonotone_ids | PASS |
| test_17_regime_metric_definition_equals_STEP5B | PASS |
| test_18_no_reinference_or_threshold_tuning | PASS |
| test_19_future_targets_not_filter_inputs | PASS |
| test_20_nonfinite_parameters_and_repro_evidence_blocked | PASS |
| test_21_Test_one_state_kept_not_refit | PASS |
| test_22_financial_entrypoint_always_blocks_before_IO | PASS |
| test_23_no_new_seed_or_missing_candidate | PASS |
| test_24_raw_Train_names_equal_means_blocked | PASS |

미래 관측 변경에 따른 과거 posterior 불변, smoothing과 forward 차이, bridge 연속성·전이 누락 거절, label permutation 명명 일관성, 공분산·비수렴·붕괴 차단, 동일 예측의 레짐 분해 보존을 통과했다. actual financial entrypoint는 approved/fit 플래그를 임의로 넘겨도 I/O 전에 BLOCKED다. 이 시험 통과를 실제 금융 HMM 적합/누출 인증으로 바꾸지 않는다.

상세 금융 input/date/checkpoint/identity 매핑과 비공개 SHA 관계는 로컬 ignored 경로에만 보존한다. 공개본은 코드·구조적 계약·합성 결과·집계·비민감 해시만 포함한다.
