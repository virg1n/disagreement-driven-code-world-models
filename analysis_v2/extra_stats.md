| statistic | disagree | llm | random |
|---|---|---|---|
| falsify_rate | 0.969 | 0.550 | 0.582 |
| P(expose | shared error exposable) | 0.044 | 0.238 | 0.206 |
| repeat_rate | 0.206 | 0.073 | 0.129 |
| max_run | 4.719 | 2.000 | 2.750 |
| reset_has_max_raw_H | 0.203 | 0.078 | 0.083 |
| requery_rate | 0.015 | 0.333 | 0.361 |
| final_fit_best | 0.506 | 0.792 | 0.760 |
| n_consistent_final | 0.000 | 0.438 | 0.094 |
| origin_repair_share | 0.948 | 0.901 | 0.938 |

## Offline re-synthesis (96 histories, 16 samples each)

| policy | best-fit: fit | best-fit: held-out acc | best-fit: acc (changing) | oracle acc | oracle acc (changing) | mean sample acc (changing) |
|---|---|---|---|---|---|---|
| disagree | 0.373 | 0.384 | 0.168 | 0.435 | 0.186 | 0.058 |
| llm | 0.637 | 0.349 | 0.095 | 0.409 | 0.118 | 0.047 |
| random | 0.651 | 0.403 | 0.123 | 0.430 | 0.142 | 0.053 |

| metric | comparison | mean diff | 95% CI | W/T/L |
|---|---|---|---|---|
| best-fit acc | disagree − llm | +0.035 | [-0.010, +0.082] | 16/4/12 |
| best-fit acc | disagree − random | -0.019 | [-0.062, +0.022] | 13/4/15 |
| best-fit acc (chg) | disagree − llm | +0.073 | [-0.012, +0.168] | 15/11/6 |
| best-fit acc (chg) | disagree − random | +0.045 | [-0.050, +0.148] | 12/8/12 |
| oracle acc (chg) | disagree − llm | +0.068 | [-0.007, +0.150] | 14/13/5 |
| oracle acc (chg) | disagree − random | +0.044 | [-0.019, +0.115] | 11/10/11 |
| mean sample acc (chg) | disagree − llm | +0.012 | [-0.008, +0.033] | 19/0/13 |
| mean sample acc (chg) | disagree − random | +0.005 | [-0.014, +0.024] | 17/3/12 |
