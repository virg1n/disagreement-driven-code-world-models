# Results (96 episodes, envs=['disease', 'egg', 'gravity', 'grow', 'ice', 'magnets', 'paint', 'wind'], policies=['disagree', 'llm', 'random'])

## Overall (mean ± s.e.m. over env×seed episodes)

| metric | Disagreement | LLM-direct | Random |
|---|---|---|---|
| coverage | 0.769 ± 0.036 | 0.603 ± 0.045 | 0.765 ± 0.042 |
| ho_acc | 0.501 ± 0.051 | 0.446 ± 0.047 | 0.504 ± 0.051 |
| ho_acc_chg | 0.319 ± 0.059 | 0.197 ± 0.048 | 0.285 ± 0.054 |
| ho_oracle | 0.514 ± 0.050 | 0.477 ± 0.050 | 0.522 ± 0.053 |
| ho_oracle_chg | 0.320 ± 0.059 | 0.244 ± 0.054 | 0.318 ± 0.059 |
| ho_pool_mean | 0.467 ± 0.050 | 0.428 ± 0.045 | 0.459 ± 0.047 |
| best_fit | 0.506 ± 0.055 | 0.792 ± 0.033 | 0.760 ± 0.036 |
| reset_share | 0.040 ± 0.006 | 0.181 ± 0.010 | 0.184 ± 0.009 |
| noop_share | 0.037 ± 0.008 | 0.087 ± 0.008 | 0.264 ± 0.014 |
| reset_noop | 0.077 ± 0.010 | 0.268 ± 0.015 | 0.448 ± 0.013 |
| n_decisions | 38.406 ± 0.237 | 32.531 ± 0.389 | 31.719 ± 0.424 |
| llm_calls | 193.000 ± 1.179 | 189.969 ± 3.469 | 158.000 ± 2.022 |
| gen_tokens | 97278.812 ± 2393.662 | 79844.281 ± 2739.062 | 80715.062 ± 2421.752 |
| frac_Hmax0 | 0.013 ± 0.008 | 0.022 ± 0.009 | 0.029 ± 0.011 |
| frac_blind | 0.012 ± 0.008 | 0.014 ± 0.006 | 0.010 ± 0.005 |
| cand_unan_wrong | 0.083 ± 0.015 | 0.081 ± 0.012 | 0.054 ± 0.008 |
| chosen_unan_wrong | 0.016 ± 0.006 | 0.092 ± 0.015 | 0.063 ± 0.011 |
| mean_H_chosen | 1.352 ± 0.089 | 0.513 ± 0.034 | 0.592 ± 0.041 |
| ho_unanimous_wrong_of_failed | 0.365 ± 0.051 | 0.340 ± 0.060 | 0.293 ± 0.047 |
| ho_unanimous_wrong | 0.180 ± 0.033 | 0.176 ± 0.034 | 0.133 ± 0.022 |
| ho_all_wrong | 0.452 ± 0.054 | 0.496 ± 0.054 | 0.457 ± 0.055 |
| identity_acc | 0.396 ± 0.041 | 0.396 ± 0.041 | 0.396 ± 0.041 |

## Paired differences (same env & seed)

| metric | comparison | mean diff | 95% bootstrap CI | wins/ties/losses | sign-test p |
|---|---|---|---|---|---|
| coverage | disagree − llm | +0.166 | [+0.085, +0.247] | 20/6/6 | 0.009 |
| coverage | disagree − random | +0.004 | [-0.053, +0.058] | 11/14/7 | 0.481 |
| ho_acc | disagree − llm | +0.055 | [+0.005, +0.107] | 18/3/11 | 0.265 |
| ho_acc | disagree − random | -0.003 | [-0.040, +0.033] | 17/1/14 | 0.720 |
| ho_acc_chg | disagree − llm | +0.122 | [+0.039, +0.219] | 19/4/9 | 0.087 |
| ho_acc_chg | disagree − random | +0.034 | [-0.040, +0.107] | 20/3/9 | 0.061 |
| ho_oracle | disagree − llm | +0.037 | [+0.003, +0.075] | 16/5/11 | 0.442 |
| ho_oracle | disagree − random | -0.008 | [-0.039, +0.019] | 14/4/14 | 1.000 |
| ho_oracle_chg | disagree − llm | +0.077 | [+0.010, +0.147] | 16/7/9 | 0.230 |
| ho_oracle_chg | disagree − random | +0.002 | [-0.064, +0.057] | 15/5/12 | 0.701 |
| reset_noop | disagree − llm | -0.191 | [-0.226, -0.155] | 1/0/31 | 0.000 |
| reset_noop | disagree − random | -0.370 | [-0.401, -0.341] | 0/0/32 | 0.000 |
| ho_unanimous_wrong | disagree − llm | +0.004 | [-0.061, +0.068] | 16/5/11 | 0.442 |
| ho_unanimous_wrong | disagree − random | +0.048 | [-0.023, +0.121] | 14/4/14 | 1.000 |

## Per environment (mean over seeds)


**coverage**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.92 | 0.79 | 1.00 |
| egg | 0.86 | 0.54 | 0.79 |
| gravity | 0.94 | 1.00 | 0.81 |
| grow | 0.62 | 0.44 | 0.56 |
| ice | 0.88 | 0.50 | 1.00 |
| magnets | 0.69 | 0.31 | 0.59 |
| paint | 0.42 | 0.42 | 0.38 |
| wind | 0.83 | 0.83 | 1.00 |

**ho_acc**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.65 | 0.57 | 0.62 |
| egg | 0.88 | 0.65 | 0.86 |
| gravity | 0.30 | 0.31 | 0.35 |
| grow | 0.34 | 0.31 | 0.37 |
| ice | 0.12 | 0.11 | 0.13 |
| magnets | 0.66 | 0.73 | 0.74 |
| paint | 0.85 | 0.75 | 0.82 |
| wind | 0.22 | 0.13 | 0.13 |

**ho_acc_chg**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.45 | 0.26 | 0.34 |
| egg | 0.82 | 0.35 | 0.75 |
| gravity | 0.01 | 0.02 | 0.08 |
| grow | 0.10 | 0.03 | 0.07 |
| ice | 0.03 | 0.02 | 0.04 |
| magnets | 0.77 | 0.70 | 0.71 |
| paint | 0.21 | 0.16 | 0.22 |
| wind | 0.16 | 0.05 | 0.06 |

**ho_oracle_chg**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.46 | 0.28 | 0.34 |
| egg | 0.82 | 0.67 | 0.96 |
| gravity | 0.03 | 0.02 | 0.09 |
| grow | 0.08 | 0.03 | 0.11 |
| ice | 0.03 | 0.04 | 0.05 |
| magnets | 0.77 | 0.64 | 0.71 |
| paint | 0.21 | 0.22 | 0.22 |
| wind | 0.16 | 0.07 | 0.07 |

**reset_noop**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.11 | 0.29 | 0.44 |
| egg | 0.09 | 0.28 | 0.45 |
| gravity | 0.04 | 0.26 | 0.45 |
| grow | 0.06 | 0.23 | 0.45 |
| ice | 0.04 | 0.27 | 0.46 |
| magnets | 0.13 | 0.23 | 0.47 |
| paint | 0.12 | 0.26 | 0.44 |
| wind | 0.03 | 0.33 | 0.41 |

**ho_unanimous_wrong_of_failed**

| env | Disagreement | LLM-direct | Random |
|---|---|---|---|
| disease | 0.50 | 0.06 | 0.27 |
| egg | 0.00 | 0.00 | 0.25 |
| gravity | 0.41 | 0.54 | 0.24 |
| grow | 0.43 | 0.48 | 0.39 |
| ice | 0.42 | 0.47 | 0.27 |
| magnets | 0.44 | 0.36 | 0.22 |
| paint | 0.46 | 0.71 | 0.44 |
| wind | 0.25 | 0.10 | 0.27 |

## Action distribution (share of primitive actions)

| policy | up/down/left/right | click | noop | reset |
|---|---|---|---|---|
| Disagreement | 0.453 | 0.470 | 0.037 | 0.040 |
| LLM-direct | 0.155 | 0.577 | 0.087 | 0.181 |
| Random | 0.286 | 0.266 | 0.264 | 0.184 |

## Final program pool on held-out transitions

| policy | all correct | some correct | all wrong, disagree | all wrong, UNANIMOUS |
|---|---|---|---|---|
| Disagreement | 0.345 | 0.203 | 0.271 | 0.180 |
| LLM-direct | 0.344 | 0.160 | 0.320 | 0.176 |
| Random | 0.372 | 0.171 | 0.324 | 0.133 |

## Per rule (on-clause) on held-out: share of first-firing transitions where the final pool is unanimously wrong

| env | clause | n | Disagreement | LLM-direct | Random |
|---|---|---|---|---|---|
| disease | 0 | 6 | 0.04 | 0.00 | 0.00 |
| disease | 1 | 6 | 0.25 | 0.00 | 0.00 |
| disease | 2 | 6 | 0.12 | 0.00 | 0.12 |
| disease | 3 | 5 | 0.20 | 0.10 | 0.00 |
| disease | 4 | 6 | 0.25 | 0.00 | 0.29 |
| disease | 5 | 6 | 0.17 | 0.00 | 0.08 |
| egg | 1 | 6 | 0.00 | 0.00 | 0.00 |
| egg | 2 | 6 | 0.00 | 0.00 | 0.00 |
| egg | 3 | 6 | 0.00 | 0.00 | 0.00 |
| egg | 4 | 6 | 0.00 | 0.00 | 0.12 |
| gravity | 0 | 1 | 1.00 | 1.00 | 0.25 |
| gravity | 1 | 3 | 0.42 | 0.42 | 0.33 |
| gravity | 2 | 2 | 0.00 | 0.25 | 0.12 |
| gravity | 3 | 6 | 0.04 | 0.04 | 0.08 |
| gravity | 4 | 6 | 0.25 | 0.25 | 0.50 |
| gravity | 5 | 1 | 0.25 | 0.75 | 0.50 |
| gravity | 6 | 3 | 0.08 | 0.25 | 0.17 |
| gravity | 7 | 2 | 0.12 | 0.38 | 0.25 |
| gravity | 8 | 2 | 0.25 | 0.75 | 0.50 |
| grow | 0 | 6 | 0.00 | 0.00 | 0.00 |
| grow | 1 | 4 | 0.25 | 0.25 | 0.31 |
| grow | 2 | 4 | 0.25 | 0.25 | 0.31 |
| grow | 3 | 6 | 0.75 | 0.62 | 0.17 |
| grow | 4 | 6 | 0.08 | 0.21 | 0.00 |
| grow | 5 | 6 | 0.00 | 0.00 | 0.00 |
| grow | 7 | 6 | 0.29 | 0.00 | 0.46 |
| ice | 0 | 6 | 0.50 | 0.12 | 0.08 |
| ice | 1 | 6 | 0.00 | 0.33 | 0.04 |
| ice | 2 | 6 | 0.46 | 0.29 | 0.00 |
| ice | 3 | 6 | 0.54 | 0.62 | 0.33 |
| magnets | 0 | 6 | 0.25 | 0.08 | 0.08 |
| magnets | 1 | 6 | 0.12 | 0.04 | 0.04 |
| magnets | 2 | 6 | 0.04 | 0.12 | 0.04 |
| magnets | 3 | 6 | 0.00 | 0.00 | 0.25 |
| magnets | 4 | 2 | 0.50 | 0.62 | 0.25 |
| magnets | 6 | 2 | 0.75 | 0.38 | 0.25 |
| magnets | 7 | 1 | 0.25 | 0.75 | 0.75 |
| paint | 0 | 6 | 0.29 | 0.38 | 0.21 |
| paint | 1 | 6 | 0.00 | 0.00 | 0.00 |
| paint | 2 | 6 | 0.00 | 0.00 | 0.00 |
| paint | 3 | 5 | 0.00 | 0.00 | 0.00 |
| paint | 4 | 2 | 0.00 | 0.00 | 0.00 |
| wind | 0 | 6 | 0.00 | 0.00 | 0.00 |
| wind | 1 | 5 | 0.40 | 0.25 | 0.40 |
| wind | 2 | 6 | 0.21 | 0.04 | 0.21 |
| wind | 3 | 6 | 0.08 | 0.00 | 0.17 |
| wind | 4 | 5 | 0.35 | 0.20 | 0.35 |
| wind | 5 | 6 | 0.92 | 1.00 | 1.00 |

## Exposure of shared wrong assumptions during exploration

Decisions where the executed action had a unanimous-but-wrong pool prediction (the only way a shared error gets exposed), and decisions where no candidate had any disagreement (H_max = 0).

| policy | decisions | chosen unanimous-wrong (exposures) | H_max = 0 | H_max = 0 while some candidate unanimous-wrong (blind spot) | candidates unanimous-wrong |
|---|---|---|---|---|---|
| Disagreement | 1229 | 0.015 | 0.013 | 0.012 | 0.084 |
| LLM-direct | 1041 | 0.092 | 0.022 | 0.013 | 0.081 |
| Random | 1015 | 0.063 | 0.030 | 0.010 | 0.054 |
