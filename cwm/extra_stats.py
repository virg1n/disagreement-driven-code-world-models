"""Extra exploration statistics: falsification, exposure of shared errors, repetition traps, reset counterfactuals,
and the offline re-synthesis summary."""
import collections
import glob
import json
import os
import random
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import res  # noqa: E402
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # tables contain non-ASCII; Windows consoles default to cp125x

RES = sys.argv[1] if len(sys.argv) > 1 else res("results_v2")
POLS = ["disagree", "llm", "random", "disagree_noreset"]


def boot(diffs, n=10000):
    rng = random.Random(0)
    ms = sorted(st.mean(rng.choices(diffs, k=len(diffs))) for _ in range(n))
    return ms[250], ms[9750]


rs = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(RES, "*__*__s*.json")))]
rows = collections.defaultdict(lambda: collections.defaultdict(list))
for r in rs:
    a = rows[r["policy"]]
    log = r["log"]
    fals, shared_hit, repeat, runs = [], [], [], []
    run = 1
    reset_best_raw, reset_best_raw_n = 0, 0
    for k, l in enumerate(log):
        ch = next(c for c in l["cands"] if c["label"] == l["chosen"])
        fals.append(ch["n_correct"] < ch["n_valid"])
        if l["n_unanimous_wrong"] > 0:
            shared_hit.append(l["chosen_unanimous_wrong"])
        if k > 0:
            same = l["chosen"] == log[k - 1]["chosen"]
            repeat.append(same)
            run = run + 1 if same else 1
        runs.append(run)
        resets = [c for c in l["cands"] if c["kind"] == "reset"]
        prims = [c for c in l["cands"] if c["kind"] != "reset"]
        if resets and prims:
            reset_best_raw_n += 1
            reset_best_raw += max(c["H"] for c in resets) > max(c["H"] for c in prims) + 1e-9
    a["falsify_rate"].append(st.mean(fals))
    a["P(expose | shared error exposable)"].append(st.mean(shared_hit) if shared_hit else float("nan"))
    a["repeat_rate"].append(st.mean(repeat))
    a["max_run"].append(max(runs))
    a["reset_has_max_raw_H"].append(reset_best_raw / max(1, reset_best_raw_n))
    seen, rq, n = set(), 0, 0
    for s in r["history"]:
        g = tuple(s["init"])
        for act, g2 in s["steps"]:
            rq += (g, act) in seen
            n += 1
            seen.add((g, act))
            g = tuple(g2)
    a["requery_rate"].append(rq / n)
    a["final_fit_best"].append(max(p["fit"] for p in r["final_pool"]))
    a["n_consistent_final"].append(sum(p["fit"] == 1.0 for p in r["final_pool"]))
    a["origin_repair_share"].append(sum(p["origin"] == "repair" for p in r["final_pool"]) / len(r["final_pool"]))

print("| statistic | " + " | ".join(p for p in POLS if p in rows) + " |")
print("|---|" + "---|" * len([p for p in POLS if p in rows]))
for k in next(iter(rows.values())):
    print(f"| {k} | " + " | ".join(f"{st.mean([x for x in rows[p][k] if x == x]):.3f}" for p in POLS if p in rows) + " |")

rdir = os.path.join(RES, "resynth")
rsy = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(rdir, "*.json")))]
if rsy:
    print(f"\n## Offline re-synthesis ({len(rsy)} histories, {rsy[0]['n']} samples each)\n")
    M = {(d["env"], d["policy"], d["seed"]): d for d in rsy}
    print("| policy | best-fit: fit | best-fit: held-out acc | best-fit: acc (changing) | oracle acc | oracle acc (changing) | mean sample acc (changing) |")
    print("|---|---|---|---|---|---|---|")
    for p in POLS:
        ds = [d for d in rsy if d["policy"] == p]
        if not ds:
            continue
        f = lambda g: st.mean(g(d) for d in ds)  # noqa: E731
        print(f"| {p} | {f(lambda d: d['best_by_fit']['fit']):.3f} | {f(lambda d: d['best_by_fit']['acc']):.3f} | "
              f"{f(lambda d: d['best_by_fit']['acc_changing']):.3f} | {f(lambda d: d['oracle']['acc']):.3f} | "
              f"{f(lambda d: d['oracle']['acc_changing']):.3f} | {f(lambda d: d['mean_acc_changing']):.3f} |")
    print("\n| metric | comparison | mean diff | 95% CI | W/T/L |")
    print("|---|---|---|---|---|")
    for key, g in [("best-fit acc", lambda d: d["best_by_fit"]["acc"]), ("best-fit acc (chg)", lambda d: d["best_by_fit"]["acc_changing"]),
                   ("oracle acc (chg)", lambda d: d["oracle"]["acc_changing"]), ("mean sample acc (chg)", lambda d: d["mean_acc_changing"])]:
        for p2 in ["llm", "random", "disagree_noreset"]:
            diffs = [g(M[(e, "disagree", s)]) - g(M[(e, p2, s)]) for (e, p, s) in M if p == "disagree" and (e, p2, s) in M]
            if diffs:
                lo, hi = boot(diffs)
                w = sum(x > 1e-12 for x in diffs)
                l_ = sum(x < -1e-12 for x in diffs)
                print(f"| {key} | disagree − {p2} | {st.mean(diffs):+.3f} | [{lo:+.3f}, {hi:+.3f}] | {w}/{len(diffs) - w - l_}/{l_} |")
