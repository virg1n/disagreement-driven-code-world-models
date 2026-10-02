# Results (48 episodes, envs=['disease', 'egg', 'gravity', 'grow', 'ice', 'magnets', 'paint', 'wind'], policies=['disagree', 'llm', 'random'])

## Overall (mean ± s.e.m. over env×seed episodes)

| metric | Disagreement | LLM-direct | Random |
|---|---|---|---|
| coverage | 0.509 ± 0.064 | 0.409 ± 0.064 | 0.736 ± 0.063 |
| ho_acc | 0.516 ± 0.079 | 0.430 ± 0.065 | 0.501 ± 0.074 |
| ho_acc_chg | 0.306 ± 0.089 | 0.091 ± 0.038 | 0.284 ± 0.084 |
| ho_oracle | 0.519 ± 0.078 | 0.446 ± 0.067 | 0.518 ± 0.075 |
| ho_oracle_chg | 0.308 ± 0.089 | 0.145 ± 0.059 | 0.290 ± 0.085 |
| ho_pool_mean | 0.489 ± 0.072 | 0.395 ± 0.059 | 0.477 ± 0.069 |
| best_fit | 0.679 ± 0.088 | 0.782 ± 0.076 | 0.883 ± 0.037 |
| reset_share | 0.045 ± 0.009 | 0.128 ± 0.016 | 0.203 ± 0.013 |
| noop_share | 0.019 ± 0.007 | 0.009 ± 0.004 | 0.241 ± 0.022 |
| reset_noop | 0.064 ± 0.013 | 0.138 ± 0.018 | 0.444 ± 0.020 |
| n_decisions | 38.188 ± 0.368 | 33.312 ± 0.930 | 31.062 ± 0.544 |
| llm_calls | 191.625 ± 1.809 | 188.812 ± 7.403 | 141.688 ± 6.934 |
| gen_tokens | 57333.375 ± 4208.646 | 42252.188 ± 2694.795 | 51479.875 ± 4641.529 |
| frac_Hmax0 | 0.000 ± 0.000 | 0.018 ± 0.011 | 0.028 ± 0.018 |
| frac_blind | 0.000 ± 0.000 | 0.014 ± 0.008 | 0.013 ± 0.010 |
| cand_unan_wrong | 0.166 ± 0.026 | 0.130 ± 0.032 | 0.100 ± 0.021 |
| chosen_unan_wrong | 0.010 ± 0.004 | 0.052 ± 0.029 | 0.078 ± 0.017 |
| mean_H_chosen | 0.915 ± 0.150 | 0.595 ± 0.116 | 0.392 ± 0.045 |
| ho_unanimous_wrong_of_failed | 0.591 ± 0.089 | 0.517 ± 0.100 | 0.423 ± 0.074 |
| ho_unanimous_wrong | 0.310 ± 0.075 | 0.343 ± 0.079 | 0.191 ± 0.052 |
| ho_all_wrong | 0.464 ± 0.081 | 0.540 ± 0.071 | 0.454 ± 0.080 |
| identity_acc | 0.396 ± 0.060 | 0.396 ± 0.060 | 0.396 ± 0.060 |

## Paired differences (same env & seed)

| metric | comparison | mean diff | 95% bootstrap CI | wins/ties/losses | sign-test p |
|---|---|---|---|---|---|
| coverage | disagree − llm | +0.100 | [+0.006, +0.204] | 6/7/3 | 0.508 |
| coverage | disagree − random | -0.227 | [-0.379, -0.081] | 2/4/10 | 0.039 |
| ho_acc | disagree − llm | +0.086 | [+0.018, +0.163] | 8/6/2 | 0.109 |
| ho_acc | disagree − random | +0.015 | [-0.038, +0.083] | 5/3/8 | 0.581 |
| ho_acc_chg | disagree − llm | +0.215 | [+0.059, +0.393] | 9/6/1 | 0.021 |
| ho_acc_chg | disagree − random | +0.022 | [-0.077, +0.160] | 2/6/8 | 0.109 |
| ho_oracle | disagree − llm | +0.072 | [+0.004, +0.150] | 8/6/2 | 0.109 |
| ho_oracle | disagree − random | +0.001 | [-0.050, +0.063] | 4/3/9 | 0.267 |
| ho_oracle_chg | disagree − llm | +0.163 | [+0.020, +0.328] | 8/6/2 | 0.109 |
| ho_oracle_chg | disagree − random | +0.018 | [-0.082, +0.144] | 4/3/9 | 0.267 |
| reset_noop | disagree − llm | -0.073 | [-0.111, -0.034] | 2/1/13 | 0.007 |
| reset_noop | disagree − random | -0.380 | [-0.422, -0.338] | 0/0/16 | 0.000 |
| ho_unanimous_wrong | disagree − llm | -0.033 | [-0.119, +0.042] | 9/1/6 | 0.607 |
| ho_unanimous_wrong | disagree − random | +0.120 | [+0.023, +0.234] | 10/1/5 | 0.302 |

## Per environment (mean over seeds)


**coverage**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.92 | 0.83 | 1.00 |
| egg | 0.43 | 0.29 | 0.71 |
| gravity | 0.67 | 0.78 | 0.78 |
| grow | 0.44 | 0.38 | 0.56 |
| ice | 0.38 | 0.25 | 1.00 |
| magnets | 0.75 | 0.25 | 0.50 |
| paint | 0.17 | 0.17 | 0.33 |
| wind | 0.33 | 0.33 | 1.00 |

**ho_acc**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.61 | 0.54 | 0.69 |
| egg | 0.87 | 0.49 | 0.74 |
| gravity | 0.40 | 0.30 | 0.30 |
| grow | 0.34 | 0.34 | 0.37 |
| ice | 0.15 | 0.15 | 0.20 |
| magnets | 0.82 | 0.69 | 0.82 |
| paint | 0.85 | 0.85 | 0.80 |
| wind | 0.08 | 0.08 | 0.08 |

**ho_acc_chg**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.30 | 0.17 | 0.45 |
| egg | 0.78 | 0.00 | 0.49 |
| gravity | 0.15 | 0.00 | 0.00 |
| grow | 0.02 | 0.01 | 0.07 |
| ice | 0.06 | 0.05 | 0.12 |
| magnets | 0.90 | 0.25 | 0.90 |
| paint | 0.24 | 0.24 | 0.24 |
| wind | 0.00 | 0.00 | 0.00 |

**ho_oracle_chg**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.31 | 0.28 | 0.49 |
| egg | 0.78 | 0.00 | 0.56 |
| gravity | 0.15 | 0.00 | 0.01 |
| grow | 0.02 | 0.01 | 0.11 |
| ice | 0.06 | 0.05 | 0.13 |
| magnets | 0.90 | 0.58 | 0.90 |
| paint | 0.24 | 0.24 | 0.12 |
| wind | 0.00 | 0.01 | 0.00 |

**reset_noop**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.14 | 0.24 | 0.41 |
| egg | 0.05 | 0.14 | 0.53 |
| gravity | 0.01 | 0.17 | 0.47 |
| grow | 0.06 | 0.12 | 0.44 |
| ice | 0.12 | 0.05 | 0.49 |
| magnets | 0.10 | 0.14 | 0.41 |
| paint | 0.00 | 0.11 | 0.38 |
| wind | 0.03 | 0.12 | 0.43 |

**ho_unanimous_wrong_of_failed**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.25 | 0.43 | 0.46 |
| egg | 1.00 | 0.00 | 0.78 |
| gravity | 0.38 | 0.71 | 0.09 |
| grow | 0.79 | 0.92 | 0.64 |
| ice | 0.82 | 0.78 | 0.75 |
| magnets | 0.61 | 0.46 | 0.35 |
| paint | 0.05 | 0.00 | 0.09 |
| wind | 0.83 | 0.85 | 0.22 |

## Action distribution (share of primitive actions)

| policy | up/down/left/right | click | noop | reset |
|---|---|---|---|---|
| Disagreement | 0.312 | 0.623 | 0.019 | 0.045 |
| LLM-direct | 0.053 | 0.809 | 0.009 | 0.128 |
| Random | 0.287 | 0.269 | 0.241 | 0.203 |

## Final program pool on held-out transitions

| policy | all correct | some correct | all wrong, disagree | all wrong, UNANIMOUS |
|---|---|---|---|---|
| Disagreement | 0.432 | 0.103 | 0.154 | 0.310 |
| LLM-direct | 0.320 | 0.141 | 0.197 | 0.343 |
| Random | 0.397 | 0.149 | 0.263 | 0.191 |

## Per rule (on-clause) on held-out: share of first-firing transitions where the final pool is unanimously wrong

| env | clause | n | Disagreement | LLM-direct | Random |
|---|---|---|---|---|---|
| disease | 0 | 6 | 0.08 | 0.08 | 0.00 |
| disease | 1 | 6 | 0.00 | 0.00 | 0.00 |
| disease | 2 | 6 | 0.00 | 0.50 | 0.33 |
| disease | 3 | 5 | 0.00 | 0.50 | 0.20 |
| disease | 4 | 6 | 0.08 | 0.17 | 0.00 |
| disease | 5 | 6 | 0.50 | 0.00 | 0.17 |
| egg | 1 | 6 | 0.00 | 0.00 | 0.00 |
| egg | 2 | 6 | 0.50 | 0.00 | 0.00 |
| egg | 3 | 6 | 0.00 | 0.00 | 0.50 |
| egg | 4 | 6 | 0.50 | 0.00 | 0.50 |
| gravity | 0 | 1 | 0.50 | 1.00 | 0.00 |
| gravity | 1 | 3 | 0.17 | 0.33 | 0.00 |
| gravity | 2 | 2 | 0.25 | 0.50 | 0.00 |
| gravity | 3 | 6 | 0.00 | 0.00 | 0.00 |
| gravity | 4 | 6 | 0.00 | 0.00 | 0.00 |
| gravity | 5 | 1 | 0.50 | 0.50 | 0.50 |
| gravity | 6 | 3 | 0.00 | 0.17 | 0.17 |
| gravity | 7 | 2 | 0.00 | 0.25 | 0.25 |
| gravity | 8 | 2 | 0.50 | 0.50 | 0.50 |
| grow | 0 | 6 | 0.00 | 0.00 | 0.00 |
| grow | 1 | 4 | 0.88 | 1.00 | 0.88 |
| grow | 2 | 4 | 0.88 | 1.00 | 0.88 |
| grow | 3 | 6 | 1.00 | 1.00 | 0.08 |
| grow | 4 | 6 | 0.50 | 1.00 | 0.00 |
| grow | 5 | 6 | 0.00 | 0.00 | 0.00 |
| grow | 7 | 6 | 0.08 | 0.00 | 0.33 |
| ice | 0 | 6 | 1.00 | 1.00 | 0.50 |
| ice | 1 | 6 | 0.50 | 1.00 | 0.00 |
| ice | 2 | 6 | 1.00 | 1.00 | 0.33 |
| ice | 3 | 6 | 0.50 | 0.17 | 0.67 |
| magnets | 0 | 6 | 0.33 | 0.00 | 0.00 |
| magnets | 1 | 6 | 0.08 | 0.00 | 0.08 |
| magnets | 2 | 6 | 0.08 | 0.08 | 0.08 |
| magnets | 3 | 6 | 0.00 | 0.00 | 0.00 |
| magnets | 4 | 2 | 0.75 | 0.50 | 0.25 |
| magnets | 6 | 2 | 0.75 | 0.25 | 0.25 |
| magnets | 7 | 1 | 0.50 | 0.50 | 0.50 |
| paint | 0 | 6 | 0.00 | 0.00 | 0.00 |
| paint | 1 | 6 | 0.00 | 0.00 | 0.00 |
| paint | 2 | 6 | 0.00 | 0.00 | 0.00 |
| paint | 3 | 5 | 0.00 | 0.00 | 0.00 |
| paint | 4 | 2 | 0.00 | 0.00 | 0.00 |
| wind | 0 | 6 | 0.00 | 0.00 | 0.00 |
| wind | 1 | 5 | 0.90 | 1.00 | 0.20 |
| wind | 2 | 6 | 0.58 | 0.58 | 0.17 |
| wind | 3 | 6 | 0.67 | 0.67 | 0.00 |
| wind | 4 | 5 | 0.80 | 0.80 | 0.10 |
| wind | 5 | 6 | 0.92 | 0.83 | 0.75 |

## Exposure of shared wrong assumptions during exploration

Decisions where the executed action had a unanimous-but-wrong pool prediction (the only way a shared error gets exposed), and decisions where no candidate had any disagreement (H_max = 0).

| policy | decisions | chosen unanimous-wrong (exposures) | H_max = 0 | H_max = 0 while some candidate unanimous-wrong (blind spot) | candidates unanimous-wrong |
|---|---|---|---|---|---|
| Disagreement | 611 | 0.010 | 0.000 | 0.000 | 0.167 |
| LLM-direct | 533 | 0.054 | 0.019 | 0.015 | 0.139 |
| Random | 497 | 0.078 | 0.030 | 0.014 | 0.103 |
