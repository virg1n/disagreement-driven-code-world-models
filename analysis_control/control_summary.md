# Positive control: true program + single-rule-deletion mutants

Distinguishable mutants per env: disease 6, egg 6, gravity 9, grow 7, ice 4, magnets 6, paint 6, wind 6

| policy | n | eliminated @10 | @20 | @40 | area under curve | identified within 40 | actions to identify (41 = not) | reset share | no-op share | rule coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| Disagreement (H/cost) | 24 | 0.70 | 0.80 | 0.92 | 0.73 | 0.62 | 26.7 | 0.005 | 0.073 | 0.92 |
| Disagreement (raw H) | 24 | 0.71 | 0.79 | 0.90 | 0.72 | 0.54 | 27.9 | 0.005 | 0.080 | 0.89 |
| Disagreement, no reset | 24 | 0.62 | 0.78 | 0.87 | 0.69 | 0.50 | 27.9 | 0.000 | 0.070 | 0.89 |
| LLM-direct | 24 | 0.25 | 0.36 | 0.46 | 0.32 | 0.00 | 41.0 | 0.185 | 0.069 | 0.58 |
| Random | 24 | 0.39 | 0.56 | 0.72 | 0.50 | 0.17 | 38.2 | 0.178 | 0.229 | 0.80 |

| metric | comparison | mean diff | 95% CI | W/T/L |
|---|---|---|---|---|
| auc | disagree − disagree_nocost | +0.012 | [-0.024, +0.048] | 10/5/9 |
| auc | disagree − disagree_noreset | +0.046 | [-0.007, +0.100] | 12/4/8 |
| auc | disagree − llm | +0.418 | [+0.359, +0.476] | 24/0/0 |
| auc | disagree − random | +0.239 | [+0.182, +0.296] | 23/0/1 |
| at10 | disagree − disagree_nocost | -0.007 | [-0.062, +0.048] | 8/8/8 |
| at10 | disagree − disagree_noreset | +0.080 | [-0.016, +0.185] | 11/6/7 |
| at10 | disagree − llm | +0.453 | [+0.347, +0.554] | 21/2/1 |
| at10 | disagree − random | +0.316 | [+0.210, +0.421] | 18/4/2 |
| at20 | disagree − disagree_nocost | +0.007 | [-0.046, +0.059] | 7/12/5 |
| at20 | disagree − disagree_noreset | +0.015 | [-0.054, +0.083] | 9/8/7 |
| at20 | disagree − llm | +0.440 | [+0.356, +0.522] | 23/1/0 |
| at20 | disagree − random | +0.237 | [+0.165, +0.306] | 22/1/1 |
| final | disagree − disagree_nocost | +0.019 | [-0.038, +0.076] | 7/12/5 |
| final | disagree − disagree_noreset | +0.048 | [-0.027, +0.128] | 8/10/6 |
| final | disagree − llm | +0.462 | [+0.389, +0.529] | 23/1/0 |
| final | disagree − random | +0.204 | [+0.128, +0.290] | 16/8/0 |
| t_id | disagree − disagree_nocost | -1.208 | [-7.458, +4.667] | 8/10/6 |
| t_id | disagree − disagree_noreset | -1.250 | [-7.708, +5.208] | 7/9/8 |
| t_id | disagree − llm | -14.333 | [-20.250, -8.542] | 0/9/15 |
| t_id | disagree − random | -11.542 | [-17.000, -6.083] | 1/9/14 |

## Per environment: fraction of distinguishable mutants eliminated by 20 actions

| env | Disagreement (H/cost) | Disagreement (raw H) | Disagreement, no reset | LLM-direct | Random |
|---|---|---|---|---|---|
| disease | 0.94 | 0.89 | 0.94 | 0.56 | 0.61 |
| egg | 0.83 | 0.94 | 0.72 | 0.28 | 0.61 |
| gravity | 0.70 | 0.74 | 0.85 | 0.44 | 0.37 |
| grow | 0.62 | 0.52 | 0.57 | 0.19 | 0.33 |
| ice | 1.00 | 1.00 | 1.00 | 0.33 | 0.83 |
| magnets | 1.00 | 0.89 | 0.78 | 0.50 | 0.61 |
| paint | 0.50 | 0.44 | 0.39 | 0.22 | 0.33 |
| wind | 0.78 | 0.89 | 1.00 | 0.33 | 0.78 |
