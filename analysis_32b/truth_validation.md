# Ground-truth audit for /public/bsuvernev2_autumn/results_32b

| statistic | disagree | llm | random |
|---|---|---|---|
| candidates contaminated | 0.101 | 0.040 | 0.018 |
| decisions with contaminated chosen action | 0.177 | 0.071 | 0.018 |
| [clean] candidates unanimous-wrong | 0.163 | 0.120 | 0.098 |
| [clean] decisions where a shared error is exposable | 0.647 | 0.430 | 0.483 |
| [clean] P(expose | exposable) | 0.008 | 0.078 | 0.239 |
| [clean] executed actions refuting >=1 program | 0.980 | 0.760 | 0.413 |
| [clean] candidates unanimous-wrong, actions 1-13 | 0.128 | 0.080 | 0.077 |
| [clean] candidates unanimous-wrong, actions 14-27 | 0.185 | 0.148 | 0.103 |
| [clean] candidates unanimous-wrong, actions 28-40 | 0.173 | 0.137 | 0.111 |

Contaminated candidate share by environment: disease 0.000, egg 0.172, gravity 0.112, grow 0.000, ice 0.000, magnets 0.140, paint 0.000, wind 0.000
