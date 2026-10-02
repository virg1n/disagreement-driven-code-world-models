| statistic | disagree | llm | random |
|---|---|---|---|
| falsify_rate | 0.982 | 0.749 | 0.423 |
| P(expose | shared error exposable) | 0.015 | 0.096 | 0.240 |
| repeat_rate | 0.161 | 0.061 | 0.113 |
| max_run | 3.750 | 2.062 | 2.625 |
| reset_has_max_raw_H | 0.300 | 0.222 | 0.088 |
| requery_rate | 0.020 | 0.250 | 0.390 |
| final_fit_best | 0.679 | 0.782 | 0.883 |
| n_consistent_final | 0.250 | 0.938 | 0.438 |
| origin_repair_share | 0.865 | 0.755 | 0.812 |

## Offline re-synthesis (48 histories, 16 samples each)

| policy | best-fit: fit | best-fit: held-out acc | best-fit: acc (changing) | oracle acc | oracle acc (changing) | mean sample acc (changing) |
|---|---|---|---|---|---|---|
| disagree | 0.474 | 0.405 | 0.198 | 0.431 | 0.150 | 0.071 |
| llm | 0.734 | 0.432 | 0.107 | 0.450 | 0.142 | 0.051 |
| random | 0.771 | 0.441 | 0.169 | 0.457 | 0.180 | 0.074 |

| metric | comparison | mean diff | 95% CI | W/T/L |
|---|---|---|---|---|
| best-fit acc | disagree − llm | -0.028 | [-0.089, +0.027] | 3/7/6 |
| best-fit acc | disagree − random | -0.036 | [-0.089, +0.008] | 5/3/8 |
| best-fit acc (chg) | disagree − llm | +0.091 | [-0.022, +0.216] | 5/8/3 |
| best-fit acc (chg) | disagree − random | +0.029 | [-0.046, +0.117] | 5/6/5 |
| oracle acc (chg) | disagree − llm | +0.008 | [-0.052, +0.066] | 4/8/4 |
| oracle acc (chg) | disagree − random | -0.030 | [-0.076, +0.014] | 3/5/8 |
| mean sample acc (chg) | disagree − llm | +0.020 | [-0.007, +0.059] | 5/5/6 |
| mean sample acc (chg) | disagree − random | -0.004 | [-0.021, +0.013] | 5/2/9 |
