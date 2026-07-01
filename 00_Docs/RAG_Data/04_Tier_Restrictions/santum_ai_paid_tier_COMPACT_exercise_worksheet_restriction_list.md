# Santum AI Compact Paid-Tier Restriction List

This compact list restricts only explicit `cbt_exercise` and `worksheet_instruction` chunks from the Free tier.

It excludes Santum Core Platform, older duplicate files, broad keyword-only flags, psychoeducation, and Socratic dialogue chunks.

## Recommended rule

- Free tier: deny listed chunk IDs and show upgrade prompt.

- Standard/Premium: allow.

- Keep one vector DB; enforce with metadata filter or ID deny-list.


## Summary by pack

| Pack | Source file | Total chunks | Restricted | Free allowed |
|---|---|---:|---:|---:|
| Assertiveness | `santum_ai_cbt_assertiveness_vector_index_v1_EMBED_READY.json` | 142 | 46 | 96 |
| Bipolar Support / Keeping Your Balance | `santum_ai_cbt_bipolar_support_vector_index_v1_EMBED_READY.json` | 86 | 38 | 48 |
| Body Acceptance / BDD | `santum_ai_cbt_body_acceptance_vector_index_v1_EMBED_READY.json` | 146 | 46 | 100 |
| Body Image / Caring Less About Your Looks | `santum_ai_cbt_body_image_vector_index_v1_EMBED_READY.json` | 116 | 47 | 69 |
| Depression / Back from the Bluez | `santum_ai_cbt_depression_vector_index_v1_EMBED_READY.json` | 112 | 34 | 78 |
| Eating Disorder Recovery | `santum_ai_cbt_eating_disorder_recovery_vector_index_v1_EMBED_READY.json` | 184 | 98 | 86 |
| Generalised Anxiety / What Me Worry | `santum_ai_cbt_gad_vector_index_v1_EMBED_READY.json` | 126 | 45 | 81 |
| Self-Esteem | `santum_ai_cbt_self_esteem_vector_index_v1_EMBED_READY.json` | 308 | 0 | 308 |
| Social Anxiety | `santum_ai_cbt_social_anxiety_vector_index_v1_EMBED_READY.json` | 162 | 105 | 57 |

## Restricted chunk IDs by pack


### Assertiveness

| Chunk ID | Topic | Chunk type |
|---|---|---|
| `cbt_assertiveness_m01_cbt_exercise_011` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m01_cbt_exercise_014` | saying_no | cbt_exercise |
| `cbt_assertiveness_m02_cbt_exercise_011` | passive_aggressive_assertive | cbt_exercise |
| `cbt_assertiveness_m03_cbt_exercise_012` | passive_aggressive_assertive | cbt_exercise |
| `cbt_assertiveness_m03_cbt_exercise_017` | unhelpful_beliefs | cbt_exercise |
| `cbt_assertiveness_m03_cbt_exercise_025` | rights_beliefs | cbt_exercise |
| `cbt_assertiveness_m04_cbt_exercise_011` | relaxation | cbt_exercise |
| `cbt_assertiveness_m04_cbt_exercise_012` | saying_no | cbt_exercise |
| `cbt_assertiveness_m04_cbt_exercise_013` | clear_requests | cbt_exercise |
| `cbt_assertiveness_m04_cbt_exercise_014` | compliments | cbt_exercise |
| `cbt_assertiveness_m04_cbt_exercise_015` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_003` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_004` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_006` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_007` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_008` | relaxation | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_009` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_011` | relaxation | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_012` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_013` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_014` | body_awareness | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_015` | calm_assertiveness | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_018` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_019` | physical_tension | cbt_exercise |
| `cbt_assertiveness_m05_cbt_exercise_021` | saying_no | cbt_exercise |
| `cbt_assertiveness_m06_cbt_exercise_002` | guilt_and_obligation | cbt_exercise |
| `cbt_assertiveness_m06_cbt_exercise_012` | dealing_with_criticism | cbt_exercise |
| `cbt_assertiveness_m07_cbt_exercise_012` | dealing_with_criticism | cbt_exercise |
| `cbt_assertiveness_m07_cbt_exercise_017` | dealing_with_criticism | cbt_exercise |
| `cbt_assertiveness_m07_cbt_exercise_024` | saying_no | cbt_exercise |
| `cbt_assertiveness_m08_cbt_exercise_006` | compliments | cbt_exercise |
| `cbt_assertiveness_m09_cbt_exercise_007` | compliments | cbt_exercise |
| `cbt_assertiveness_m09_cbt_exercise_008` | compliments | cbt_exercise |
| `cbt_assertiveness_m09_cbt_exercise_011` | compliments | cbt_exercise |
| `cbt_assertiveness_m09_cbt_exercise_012` | compliments | cbt_exercise |
| `cbt_assertiveness_m10_cbt_exercise_003` | nonverbal_assertiveness | cbt_exercise |
| `cbt_assertiveness_m10_cbt_exercise_004` | dealing_with_criticism | cbt_exercise |
| `cbt_assertiveness_m10_cbt_exercise_009` | maintenance_plan | cbt_exercise |
| `cbt_assertiveness_m10_cbt_exercise_010` | unhelpful_beliefs | cbt_exercise |
| `cbt_assertiveness_m10_cbt_exercise_011` | saying_no | cbt_exercise |
| `cbt_assertiveness_m10_cbt_exercise_013` | saying_no | cbt_exercise |
| `cbt_assertiveness_worksheet_001` | assertive_communication_plan | worksheet_instruction |
| `cbt_assertiveness_worksheet_002` | saying_no_script | worksheet_instruction |
| `cbt_assertiveness_worksheet_003` | criticism_response_record | worksheet_instruction |
| `cbt_assertiveness_worksheet_004` | assertive_belief_challenge | worksheet_instruction |
| `cbt_assertiveness_worksheet_005` | practice_and_maintenance_plan | worksheet_instruction |

### Bipolar Support / Keeping Your Balance

| Chunk ID | Topic | Chunk type |
|---|---|---|
| `cbt_bipolar_m01_cbt_exercise_004` | early_warning_signs | cbt_exercise |
| `cbt_bipolar_m01_cbt_exercise_014` | routine_support | cbt_exercise |
| `cbt_bipolar_m01_cbt_exercise_021` | treatment_options | cbt_exercise |
| `cbt_bipolar_m02_cbt_exercise_002` | medication_psychoeducation | cbt_exercise |
| `cbt_bipolar_m02_cbt_exercise_003` | medication_psychoeducation | cbt_exercise |
| `cbt_bipolar_m02_cbt_exercise_009` | medication_psychoeducation | cbt_exercise |
| `cbt_bipolar_m02_cbt_exercise_011` | medication_psychoeducation | cbt_exercise |
| `cbt_bipolar_m02_cbt_exercise_014` | medication_psychoeducation | cbt_exercise |
| `cbt_bipolar_m02_cbt_exercise_016` | treatment_options | cbt_exercise |
| `cbt_bipolar_m02_cbt_exercise_020` | medication_psychoeducation | cbt_exercise |
| `cbt_bipolar_m03_cbt_exercise_003` | self_monitoring | cbt_exercise |
| `cbt_bipolar_m03_cbt_exercise_007` | early_warning_signs | cbt_exercise |
| `cbt_bipolar_m03_cbt_exercise_009` | early_warning_signs | cbt_exercise |
| `cbt_bipolar_m03_cbt_exercise_016` | self_monitoring | cbt_exercise |
| `cbt_bipolar_m03_cbt_exercise_018` | early_warning_signs | cbt_exercise |
| `cbt_bipolar_m04_cbt_exercise_010` | treatment_options | cbt_exercise |
| `cbt_bipolar_m04_cbt_exercise_012` | behavioural_strategies_depression | cbt_exercise |
| `cbt_bipolar_m04_cbt_exercise_013` | support_plan | cbt_exercise |
| `cbt_bipolar_m04_cbt_exercise_015` | depression_coping | cbt_exercise |
| `cbt_bipolar_m04_cbt_exercise_016` | behavioural_strategies_depression | cbt_exercise |
| `cbt_bipolar_m04_cbt_exercise_021` | activity_scheduling | cbt_exercise |
| `cbt_bipolar_m05_cbt_exercise_005` | thought_challenging | cbt_exercise |
| `cbt_bipolar_m05_cbt_exercise_011` | depression_coping | cbt_exercise |
| `cbt_bipolar_m05_cbt_exercise_012` | thought_challenging | cbt_exercise |
| `cbt_bipolar_m05_cbt_exercise_016` | thought_challenging | cbt_exercise |
| `cbt_bipolar_m06_cbt_exercise_004` | sleep_routine | cbt_exercise |
| `cbt_bipolar_m06_cbt_exercise_008` | cognitive_strategies_mania | cbt_exercise |
| `cbt_bipolar_m07_cbt_exercise_002` | self_monitoring | cbt_exercise |
| `cbt_bipolar_m07_cbt_exercise_006` | manic_thoughts | cbt_exercise |
| `cbt_bipolar_m07_cbt_exercise_007` | thought_challenging | cbt_exercise |
| `cbt_bipolar_m08_cbt_exercise_006` | support_plan | cbt_exercise |
| `cbt_bipolar_m08_cbt_exercise_009` | sleep_routine | cbt_exercise |
| `cbt_bipolar_m08_cbt_exercise_011` | thought_challenging | cbt_exercise |
| `cbt_bipolar_worksheet_001` | mood_monitoring | worksheet_instruction |
| `cbt_bipolar_worksheet_002` | early_warning_signs | worksheet_instruction |
| `cbt_bipolar_worksheet_003` | sleep_routine_protection | worksheet_instruction |
| `cbt_bipolar_worksheet_004` | depression_activity_plan | worksheet_instruction |
| `cbt_bipolar_worksheet_005` | mania_decision_pause | worksheet_instruction |

### Body Acceptance / BDD

| Chunk ID | Topic | Chunk type |
|---|---|---|
| `cbt_body_acceptance_m01_cbt_exercise_022` | understanding_bdd | cbt_exercise |
| `cbt_body_acceptance_m02_cbt_exercise_009` | understanding_bdd | cbt_exercise |
| `cbt_body_acceptance_m02_cbt_exercise_017` | negative_predictions | cbt_exercise |
| `cbt_body_acceptance_m02_cbt_exercise_021` | avoidance | cbt_exercise |
| `cbt_body_acceptance_m02_cbt_exercise_022` | mirror_checking | cbt_exercise |
| `cbt_body_acceptance_m02_cbt_exercise_029` | attention_training | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_003` | external_attention | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_008` | understanding_bdd | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_010` | comparison_behaviours | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_016` | attention_training | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_017` | attention_training | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_018` | attention_training | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_020` | attention_training | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_024` | appearance_preoccupation | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_026` | attention_training | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_029` | appearance_preoccupation | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_030` | appearance_preoccupation | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_031` | appearance_preoccupation | cbt_exercise |
| `cbt_body_acceptance_m03_cbt_exercise_035` | appearance_preoccupation | cbt_exercise |
| `cbt_body_acceptance_m04_cbt_exercise_003` | checking_reduction | cbt_exercise |
| `cbt_body_acceptance_m04_cbt_exercise_004` | checking_reduction | cbt_exercise |
| `cbt_body_acceptance_m04_cbt_exercise_010` | mirror_checking | cbt_exercise |
| `cbt_body_acceptance_m04_cbt_exercise_012` | checking_reduction | cbt_exercise |
| `cbt_body_acceptance_m04_cbt_exercise_014` | checking_reduction | cbt_exercise |
| `cbt_body_acceptance_m04_cbt_exercise_015` | checking_reduction | cbt_exercise |
| `cbt_body_acceptance_m04_cbt_exercise_030` | mirror_checking | cbt_exercise |
| `cbt_body_acceptance_m05_cbt_exercise_002` | avoidance | cbt_exercise |
| `cbt_body_acceptance_m05_cbt_exercise_009` | avoidance | cbt_exercise |
| `cbt_body_acceptance_m05_cbt_exercise_011` | negative_predictions | cbt_exercise |
| `cbt_body_acceptance_m05_cbt_exercise_022` | negative_predictions | cbt_exercise |
| `cbt_body_acceptance_m05_cbt_exercise_025` | avoidance | cbt_exercise |
| `cbt_body_acceptance_m05_cbt_exercise_027` | behavioural_experiments | cbt_exercise |
| `cbt_body_acceptance_m05_cbt_exercise_028` | behavioural_experiments | cbt_exercise |
| `cbt_body_acceptance_m05_cbt_exercise_033` | safety_behaviours | cbt_exercise |
| `cbt_body_acceptance_m06_cbt_exercise_008` | appearance_assumptions | cbt_exercise |
| `cbt_body_acceptance_m06_cbt_exercise_010` | behavioural_experiments | cbt_exercise |
| `cbt_body_acceptance_m06_cbt_exercise_013` | appearance_assumptions | cbt_exercise |
| `cbt_body_acceptance_m06_cbt_exercise_016` | appearance_assumptions | cbt_exercise |
| `cbt_body_acceptance_m06_cbt_exercise_020` | understanding_bdd | cbt_exercise |
| `cbt_body_acceptance_m07_cbt_exercise_007` | appearance_preoccupation | cbt_exercise |
| `cbt_body_acceptance_m07_cbt_exercise_009` | attention_training | cbt_exercise |
| `cbt_body_acceptance_worksheet_001` | appearance_preoccupation_log | worksheet_instruction |
| `cbt_body_acceptance_worksheet_002` | checking_reassurance_reduction_plan | worksheet_instruction |
| `cbt_body_acceptance_worksheet_003` | appearance_assumption_test | worksheet_instruction |
| `cbt_body_acceptance_worksheet_004` | avoidance_safety_behaviour_experiment | worksheet_instruction |
| `cbt_body_acceptance_worksheet_005` | self_management_body_acceptance_plan | worksheet_instruction |

### Body Image / Caring Less About Your Looks

| Chunk ID | Topic | Chunk type |
|---|---|---|
| `cbt_body_image_m01_cbt_exercise_005` | mirror_checking | cbt_exercise |
| `cbt_body_image_m01_cbt_exercise_008` | appearance_overconcern | cbt_exercise |
| `cbt_body_image_m01_cbt_exercise_011` | body_image_cycle | cbt_exercise |
| `cbt_body_image_m02_cbt_exercise_005` | body_checking | cbt_exercise |
| `cbt_body_image_m02_cbt_exercise_007` | body_checking | cbt_exercise |
| `cbt_body_image_m02_cbt_exercise_008` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m02_cbt_exercise_009` | appearance_assumptions | cbt_exercise |
| `cbt_body_image_m02_cbt_exercise_011` | mirror_checking | cbt_exercise |
| `cbt_body_image_m03_cbt_exercise_008` | appearance_focused_attention | cbt_exercise |
| `cbt_body_image_m03_cbt_exercise_009` | appearance_focused_attention | cbt_exercise |
| `cbt_body_image_m03_cbt_exercise_011` | appearance_focused_attention | cbt_exercise |
| `cbt_body_image_m03_cbt_exercise_012` | appearance_focused_attention | cbt_exercise |
| `cbt_body_image_m03_cbt_exercise_013` | appearance_focused_attention | cbt_exercise |
| `cbt_body_image_m03_cbt_exercise_014` | appearance_focused_attention | cbt_exercise |
| `cbt_body_image_m03_cbt_exercise_017` | self_monitoring | cbt_exercise |
| `cbt_body_image_m03_cbt_exercise_018` | appearance_focused_attention | cbt_exercise |
| `cbt_body_image_m03_cbt_exercise_020` | body_checking | cbt_exercise |
| `cbt_body_image_m04_cbt_exercise_005` | body_checking | cbt_exercise |
| `cbt_body_image_m04_cbt_exercise_007` | body_checking | cbt_exercise |
| `cbt_body_image_m04_cbt_exercise_010` | mirror_checking | cbt_exercise |
| `cbt_body_image_m04_cbt_exercise_015` | mirror_checking | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_002` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_005` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_006` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_007` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_013` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_015` | appearance_focused_attention | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_016` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_017` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_018` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_019` | behavioural_experiments | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_020` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m05_cbt_exercise_021` | avoidance | cbt_exercise |
| `cbt_body_image_m06_cbt_exercise_002` | mirror_checking | cbt_exercise |
| `cbt_body_image_m07_cbt_exercise_007` | relapse_prevention | cbt_exercise |
| `cbt_body_image_m07_cbt_exercise_008` | overvaluing_appearance | cbt_exercise |
| `cbt_body_image_m07_cbt_exercise_012` | overvaluing_appearance | cbt_exercise |
| `cbt_body_image_m07_cbt_exercise_013` | appearance_altering_behaviours | cbt_exercise |
| `cbt_body_image_m07_cbt_exercise_018` | avoidance | cbt_exercise |
| `cbt_body_image_m07_cbt_exercise_019` | overvaluing_appearance | cbt_exercise |
| `cbt_body_image_m07_cbt_exercise_020` | overvaluing_appearance | cbt_exercise |
| `cbt_body_image_m07_cbt_exercise_021` | body_checking | cbt_exercise |
| `cbt_body_image_worksheet_001` | appearance_attention_log | worksheet_instruction |
| `cbt_body_image_worksheet_002` | checking_reassurance_log | worksheet_instruction |
| `cbt_body_image_worksheet_003` | appearance_safety_behaviour_experiment | worksheet_instruction |
| `cbt_body_image_worksheet_004` | self_worth_balance_map | worksheet_instruction |
| `cbt_body_image_worksheet_005` | setback_management_plan | worksheet_instruction |

### Depression / Back from the Bluez

| Chunk ID | Topic | Chunk type |
|---|---|---|
| `cbt_depression_m01_cbt_exercise_002` | depression_cycle | cbt_exercise |
| `cbt_depression_m01_cbt_exercise_009` | activity_scheduling | cbt_exercise |
| `cbt_depression_m02_cbt_exercise_001` | activity_scheduling | cbt_exercise |
| `cbt_depression_m02_cbt_exercise_003` | activity_scheduling | cbt_exercise |
| `cbt_depression_m02_cbt_exercise_004` | activity_scheduling | cbt_exercise |
| `cbt_depression_m02_cbt_exercise_006` | activity_scheduling | cbt_exercise |
| `cbt_depression_m02_cbt_exercise_018` | pleasure_mastery | cbt_exercise |
| `cbt_depression_m02_cbt_exercise_026` | activity_scheduling | cbt_exercise |
| `cbt_depression_m04_cbt_exercise_002` | abc_analysis | cbt_exercise |
| `cbt_depression_m04_cbt_exercise_003` | belief_challenging | cbt_exercise |
| `cbt_depression_m04_cbt_exercise_004` | abc_analysis | cbt_exercise |
| `cbt_depression_m04_cbt_exercise_008` | belief_challenging | cbt_exercise |
| `cbt_depression_m04_cbt_exercise_010` | support_plan | cbt_exercise |
| `cbt_depression_m05_cbt_exercise_012` | unhelpful_thinking_styles | cbt_exercise |
| `cbt_depression_m05_cbt_exercise_026` | evidence_for_against | cbt_exercise |
| `cbt_depression_m06_cbt_exercise_008` | abc_analysis | cbt_exercise |
| `cbt_depression_m07_cbt_exercise_005` | unhelpful_thinking_styles | cbt_exercise |
| `cbt_depression_m07_cbt_exercise_012` | balanced_thinking | cbt_exercise |
| `cbt_depression_m07_cbt_exercise_021` | evidence_for_against | cbt_exercise |
| `cbt_depression_m08_cbt_exercise_001` | balanced_thinking | cbt_exercise |
| `cbt_depression_m08_cbt_exercise_004` | core_beliefs | cbt_exercise |
| `cbt_depression_m08_cbt_exercise_006` | core_beliefs | cbt_exercise |
| `cbt_depression_m08_cbt_exercise_008` | balanced_thinking | cbt_exercise |
| `cbt_depression_m08_cbt_exercise_012` | balanced_thinking | cbt_exercise |
| `cbt_depression_m08_cbt_exercise_015` | behavioural_activation | cbt_exercise |
| `cbt_depression_m09_cbt_exercise_001` | relapse_prevention | cbt_exercise |
| `cbt_depression_m09_cbt_exercise_003` | support_plan | cbt_exercise |
| `cbt_depression_m09_cbt_exercise_005` | balanced_thinking | cbt_exercise |
| `cbt_depression_m09_cbt_exercise_006` | evidence_for_against | cbt_exercise |
| `cbt_depression_worksheet_001` | activity_scheduling | worksheet_instruction |
| `cbt_depression_worksheet_002` | abc_thought_record | worksheet_instruction |
| `cbt_depression_worksheet_003` | unhelpful_thinking_styles | worksheet_instruction |
| `cbt_depression_worksheet_004` | core_belief_review | worksheet_instruction |
| `cbt_depression_worksheet_005` | relapse_prevention | worksheet_instruction |

### Eating Disorder Recovery

| Chunk ID | Topic | Chunk type |
|---|---|---|
| `cbt_ed_recovery_m01_cbt_exercise_004` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m01_cbt_exercise_005` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m01_cbt_exercise_008` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m01_cbt_exercise_009` | purging_risk | cbt_exercise |
| `cbt_ed_recovery_m01_cbt_exercise_011` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m01_cbt_exercise_014` | setbacks | cbt_exercise |
| `cbt_ed_recovery_m02_cbt_exercise_013` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m03_cbt_exercise_004` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m03_cbt_exercise_005` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m03_cbt_exercise_010` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m03_cbt_exercise_015` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m03_cbt_exercise_017` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m04_cbt_exercise_003` | self_monitoring | cbt_exercise |
| `cbt_ed_recovery_m04_cbt_exercise_007` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m04_cbt_exercise_008` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m04_cbt_exercise_009` | self_monitoring | cbt_exercise |
| `cbt_ed_recovery_m04_cbt_exercise_010` | pattern_awareness | cbt_exercise |
| `cbt_ed_recovery_m04_cbt_exercise_011` | meal_support | cbt_exercise |
| `cbt_ed_recovery_m04_cbt_exercise_012` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m04_cbt_exercise_015` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m05_cbt_exercise_002` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m05_cbt_exercise_006` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m05_cbt_exercise_007` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m05_cbt_exercise_009` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m05_cbt_exercise_012` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m06_cbt_exercise_006` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m06_cbt_exercise_007` | regular_eating | cbt_exercise |
| `cbt_ed_recovery_m06_cbt_exercise_011` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m06_cbt_exercise_014` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_004` | eating_for_recovery | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_010` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_011` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_012` | eating_for_recovery | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_013` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_014` | fear_foods | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_016` | eating_for_recovery | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_018` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_019` | recovery_practice | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_022` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m07_cbt_exercise_023` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m08_cbt_exercise_002` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m08_cbt_exercise_005` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m08_cbt_exercise_007` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m08_cbt_exercise_008` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m08_cbt_exercise_011` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m08_cbt_exercise_012` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m08_cbt_exercise_013` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m08_cbt_exercise_015` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m08_cbt_exercise_020` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m09_cbt_exercise_011` | purging_risk | cbt_exercise |
| `cbt_ed_recovery_m09_cbt_exercise_014` | purging_risk | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_003` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_004` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_007` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_008` | purging_risk | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_009` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_010` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_011` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_012` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_013` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_015` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m10_cbt_exercise_016` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m11_cbt_exercise_006` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m11_cbt_exercise_008` | body_checking | cbt_exercise |
| `cbt_ed_recovery_m11_cbt_exercise_011` | body_checking | cbt_exercise |
| `cbt_ed_recovery_m11_cbt_exercise_012` | body_checking | cbt_exercise |
| `cbt_ed_recovery_m11_cbt_exercise_013` | body_checking | cbt_exercise |
| `cbt_ed_recovery_m11_cbt_exercise_015` | body_checking | cbt_exercise |
| `cbt_ed_recovery_m11_cbt_exercise_016` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m11_cbt_exercise_018` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m12_cbt_exercise_003` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m12_cbt_exercise_004` | body_avoidance | cbt_exercise |
| `cbt_ed_recovery_m12_cbt_exercise_006` | body_avoidance | cbt_exercise |
| `cbt_ed_recovery_m12_cbt_exercise_009` | graded_reengagement | cbt_exercise |
| `cbt_ed_recovery_m12_cbt_exercise_010` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m12_cbt_exercise_013` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m13_cbt_exercise_010` | core_beliefs | cbt_exercise |
| `cbt_ed_recovery_m13_cbt_exercise_017` | core_beliefs | cbt_exercise |
| `cbt_ed_recovery_m13_cbt_exercise_019` | core_beliefs | cbt_exercise |
| `cbt_ed_recovery_m14_cbt_exercise_002` | setbacks | cbt_exercise |
| `cbt_ed_recovery_m14_cbt_exercise_003` | purging_risk | cbt_exercise |
| `cbt_ed_recovery_m14_cbt_exercise_005` | binge_eating_cycle | cbt_exercise |
| `cbt_ed_recovery_m14_cbt_exercise_006` | body_checking | cbt_exercise |
| `cbt_ed_recovery_m14_cbt_exercise_007` | body_checking | cbt_exercise |
| `cbt_ed_recovery_m14_cbt_exercise_012` | professional_support | cbt_exercise |
| `cbt_ed_recovery_m15_cbt_exercise_002` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m15_cbt_exercise_016` | meal_support | cbt_exercise |
| `cbt_ed_recovery_m15_cbt_exercise_017` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m15_cbt_exercise_021` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m15_cbt_exercise_023` | recovery_resources | cbt_exercise |
| `cbt_ed_recovery_m15_cbt_exercise_025` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_m15_cbt_exercise_028` | professional_support | cbt_exercise |
| `cbt_ed_recovery_m15_cbt_exercise_033` | driven_exercise | cbt_exercise |
| `cbt_ed_recovery_m15_cbt_exercise_034` | reducing_scale_focus | cbt_exercise |
| `cbt_ed_recovery_worksheet_002` | urge_support_plan | worksheet_instruction |
| `cbt_ed_recovery_worksheet_003` | body_checking_reduction | worksheet_instruction |
| `cbt_ed_recovery_worksheet_004` | values_beyond_body | worksheet_instruction |
| `cbt_ed_recovery_worksheet_005` | relapse_prevention | worksheet_instruction |

### Generalised Anxiety / What Me Worry

| Chunk ID | Topic | Chunk type |
|---|---|---|
| `cbt_gad_m01_cbt_exercise_006` | worry_uncontrollability_beliefs | cbt_exercise |
| `cbt_gad_m01_cbt_exercise_017` | generalised_anxiety | cbt_exercise |
| `cbt_gad_m02_cbt_exercise_026` | unproductive_worry | cbt_exercise |
| `cbt_gad_m03_cbt_exercise_003` | worry_uncontrollability_beliefs | cbt_exercise |
| `cbt_gad_m03_cbt_exercise_010` | worry_uncontrollability_beliefs | cbt_exercise |
| `cbt_gad_m03_cbt_exercise_014` | worry_control | cbt_exercise |
| `cbt_gad_m03_cbt_exercise_015` | metacognitive_beliefs | cbt_exercise |
| `cbt_gad_m03_cbt_exercise_018` | worry_control | cbt_exercise |
| `cbt_gad_m03_cbt_exercise_019` | worry_uncontrollability_beliefs | cbt_exercise |
| `cbt_gad_m03_cbt_exercise_020` | worry_uncontrollability_beliefs | cbt_exercise |
| `cbt_gad_m03_cbt_exercise_023` | worry_uncontrollability_beliefs | cbt_exercise |
| `cbt_gad_m04_cbt_exercise_002` | attention_training | cbt_exercise |
| `cbt_gad_m04_cbt_exercise_003` | attention_training | cbt_exercise |
| `cbt_gad_m04_cbt_exercise_006` | attention_training | cbt_exercise |
| `cbt_gad_m04_cbt_exercise_007` | attention_training | cbt_exercise |
| `cbt_gad_m04_cbt_exercise_011` | attention_shifting | cbt_exercise |
| `cbt_gad_m04_cbt_exercise_013` | attention_training | cbt_exercise |
| `cbt_gad_m04_cbt_exercise_016` | attention_training | cbt_exercise |
| `cbt_gad_m04_cbt_exercise_017` | attention_training | cbt_exercise |
| `cbt_gad_m05_cbt_exercise_005` | worry_danger_beliefs | cbt_exercise |
| `cbt_gad_m05_cbt_exercise_006` | worry_danger_beliefs | cbt_exercise |
| `cbt_gad_m05_cbt_exercise_008` | worry_danger_beliefs | cbt_exercise |
| `cbt_gad_m05_cbt_exercise_014` | worry_danger_beliefs | cbt_exercise |
| `cbt_gad_m05_cbt_exercise_016` | worry_danger_beliefs | cbt_exercise |
| `cbt_gad_m06_cbt_exercise_003` | positive_beliefs_about_worry | cbt_exercise |
| `cbt_gad_m06_cbt_exercise_005` | problem_solving | cbt_exercise |
| `cbt_gad_m06_cbt_exercise_009` | worry_as_helpful | cbt_exercise |
| `cbt_gad_m06_cbt_exercise_011` | worry_myths | cbt_exercise |
| `cbt_gad_m06_cbt_exercise_012` | positive_beliefs_about_worry | cbt_exercise |
| `cbt_gad_m06_cbt_exercise_015` | worry_myths | cbt_exercise |
| `cbt_gad_m07_cbt_exercise_012` | problem_solving | cbt_exercise |
| `cbt_gad_m09_cbt_exercise_007` | accepting_uncertainty | cbt_exercise |
| `cbt_gad_m09_cbt_exercise_008` | accepting_uncertainty | cbt_exercise |
| `cbt_gad_m09_cbt_exercise_009` | accepting_uncertainty | cbt_exercise |
| `cbt_gad_m10_cbt_exercise_004` | accepting_uncertainty | cbt_exercise |
| `cbt_gad_m10_cbt_exercise_009` | accepting_uncertainty | cbt_exercise |
| `cbt_gad_m10_cbt_exercise_012` | self_management | cbt_exercise |
| `cbt_gad_m10_cbt_exercise_015` | accepting_uncertainty | cbt_exercise |
| `cbt_gad_m10_cbt_exercise_017` | accepting_uncertainty | cbt_exercise |
| `cbt_gad_m10_cbt_exercise_020` | self_management | cbt_exercise |
| `cbt_gad_worksheet_001` | worry_classification | worksheet_instruction |
| `cbt_gad_worksheet_002` | worry_belief_challenge | worksheet_instruction |
| `cbt_gad_worksheet_003` | attention_training_practice | worksheet_instruction |
| `cbt_gad_worksheet_004` | problem_solving_plan | worksheet_instruction |
| `cbt_gad_worksheet_005` | uncertainty_experiment | worksheet_instruction |

### Social Anxiety

| Chunk ID | Topic | Chunk type |
|---|---|---|
| `cbt_social_anxiety_m01_cbt_exercise_002` | symptoms | cbt_exercise |
| `cbt_social_anxiety_m01_cbt_exercise_009` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m01_cbt_exercise_012` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m01_cbt_exercise_017` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m01_cbt_exercise_022` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_004` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_005` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_006` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_008` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_011` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_012` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_013` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_015` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_016` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_017` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m02_cbt_exercise_018` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_003` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_004` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_005` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_006` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_007` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_008` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_009` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_011` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_012` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_013` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_014` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_017` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_018` | avoidance_cycle | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_020` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_022` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_023` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_024` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_025` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_026` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_027` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m03_cbt_exercise_028` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_002` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_003` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_004` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_005` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_006` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_007` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_009` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_010` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_011` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_012` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_013` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_014` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_015` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_016` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_017` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m04_cbt_exercise_018` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m05_cbt_exercise_004` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m05_cbt_exercise_005` | safety_behaviours | cbt_exercise |
| `cbt_social_anxiety_m05_cbt_exercise_012` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m05_cbt_exercise_013` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m05_cbt_exercise_015` | safety_behaviours | cbt_exercise |
| `cbt_social_anxiety_m05_cbt_exercise_016` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m06_cbt_exercise_002` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m06_cbt_exercise_004` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m06_cbt_exercise_008` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m06_cbt_exercise_011` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m06_cbt_exercise_013` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m06_cbt_exercise_014` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m06_cbt_exercise_015` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m07_cbt_exercise_006` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m07_cbt_exercise_007` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m07_cbt_exercise_008` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m07_cbt_exercise_011` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m07_cbt_exercise_013` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m07_cbt_exercise_014` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_m07_cbt_exercise_015` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m07_cbt_exercise_016` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m07_cbt_exercise_017` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_009` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_010` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_011` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_012` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_013` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_014` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_016` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_017` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_018` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_019` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_022` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m08_cbt_exercise_023` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m09_cbt_exercise_003` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m09_cbt_exercise_004` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m09_cbt_exercise_005` | negative_thinking | cbt_exercise |
| `cbt_social_anxiety_m09_cbt_exercise_007` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m09_cbt_exercise_008` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m09_cbt_exercise_010` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m10_cbt_exercise_002` | negative_self_imagery | cbt_exercise |
| `cbt_social_anxiety_m10_cbt_exercise_003` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m10_cbt_exercise_005` | attention_training | cbt_exercise |
| `cbt_social_anxiety_m10_cbt_exercise_006` | core_beliefs | cbt_exercise |
| `cbt_social_anxiety_m10_cbt_exercise_009` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m10_cbt_exercise_010` | avoidance | cbt_exercise |
| `cbt_social_anxiety_m10_cbt_exercise_011` | behavioural_experiments | cbt_exercise |
| `cbt_social_anxiety_worksheet_001` | social_anxiety_thought_record | worksheet_instruction |
| `cbt_social_anxiety_worksheet_002` | exposure_stepladder | worksheet_instruction |
| `cbt_social_anxiety_worksheet_003` | safety_behaviour_log | worksheet_instruction |
| `cbt_social_anxiety_worksheet_004` | attention_training_log | worksheet_instruction |
| `cbt_social_anxiety_worksheet_005` | core_belief_evidence_log | worksheet_instruction |