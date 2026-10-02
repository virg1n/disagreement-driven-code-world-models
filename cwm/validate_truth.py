"""Audit of the render-side-effect bug in the ground-truth simulator.

Until the fix, `AutumnEnv.simulate` replayed the current segment without rendering, which in Autumn.cpp can change
the dynamics. Agent observations, held-out sets and coverage were never affected (the live env renders every step);
only the exploration-time statistics that compare pool predictions with the simulated truth were.

For every saved episode this replays the history and, for each non-reset candidate at each decision, computes the
truth both ways. A candidate's logged statistics are valid iff both agree. Reports the contamination rate and the
exploration-time statistics restricted to valid candidates.
"""
import collections
import glob
import json
import multiprocessing as mp
import os
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths import res  # noqa: E402
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # tables contain non-ASCII; Windows consoles default to cp125x

RES = sys.argv[1] if len(sys.argv) > 1 else res("results_v2")
POLS = ["disagree", "llm", "random", "disagree_noreset"]


def parse(label):
    if label.startswith("RESET, then replay "):
        return True, label[len("RESET, then replay "):].split("; ")
    if label.startswith("RESET, then "):
        return True, [label[len("RESET, then "):]]
    return False, [label]


def one(path):
    from autumn_env import AutumnEnv, apply_action, render, silence_cpp_stdout
    silence_cpp_stdout()
    r = json.load(open(path))
    env = AutumnEnv(r["env"])

    def old_sim(a):
        it = env._new()
        for x in env.segment_actions:
            apply_action(it, x)
        apply_action(it, a)
        return render(it)

    hist = [(a, tuple(g)) for s in r["history"] for a, g in s["steps"]]
    hi = 0
    out = []
    for l in r["log"]:
        valid = {}
        for c in l["cands"]:
            reset, acts = parse(c["label"])
            valid[c["label"]] = True if reset else old_sim(acts[0]) == env.simulate(acts, False)[0]
        reset, acts = parse(l["chosen"])
        if reset:
            env.reset()
        for a in acts:
            g = env.step(a)
            assert hist[hi] == (a, g), "replay does not reproduce the saved history"
            hi += 1
        ch = next(c for c in l["cands"] if c["label"] == l["chosen"])
        vc = [c for c in l["cands"] if valid[c["label"]]]
        out.append(dict(n=len(l["cands"]), n_valid=len(vc), chosen_valid=valid[l["chosen"]],
                        uw_valid=sum(c["unanimous_wrong"] for c in vc), chosen_uw=ch["unanimous_wrong"],
                        chosen_falsifies=ch["n_correct"] < ch["n_valid"], used=l["used"]))
    return dict(env=r["env"], policy=r["policy"], seed=r["seed"], decisions=out)


def main():
    files = sorted(glob.glob(os.path.join(RES, "*__*__s*.json")))
    with mp.get_context("fork").Pool(16) as pool:
        res = pool.map(one, files)
    os.makedirs(os.path.join(RES, "analysis"), exist_ok=True)
    json.dump(res, open(os.path.join(RES, "analysis", "truth_validation.json"), "w", encoding="utf-8"))
    agg = collections.defaultdict(lambda: collections.defaultdict(list))
    env_cont = collections.defaultdict(list)
    for e in res:
        d = e["decisions"]
        a = agg[e["policy"]]
        a["candidates contaminated"].append(1 - sum(x["n_valid"] for x in d) / sum(x["n"] for x in d))
        a["decisions with contaminated chosen action"].append(st.mean(not x["chosen_valid"] for x in d))
        env_cont[e["env"]].append(1 - sum(x["n_valid"] for x in d) / sum(x["n"] for x in d))
        a["[clean] candidates unanimous-wrong"].append(sum(x["uw_valid"] for x in d) / max(1, sum(x["n_valid"] for x in d)))
        dv = [x for x in d if x["chosen_valid"]]
        ex = [x for x in dv if x["uw_valid"] > 0]
        a["[clean] decisions where a shared error is exposable"].append(len(ex) / max(1, len(dv)))
        if ex:
            a["[clean] P(expose | exposable)"].append(st.mean(x["chosen_uw"] for x in ex))
        if dv:
            a["[clean] executed actions refuting >=1 program"].append(st.mean(x["chosen_falsifies"] for x in dv))
        for lo, hi, nm in [(0, 13, "1-13"), (13, 27, "14-27"), (27, 41, "28-40")]:
            b = [x for x in d if lo < x["used"] <= hi]
            if b and sum(x["n_valid"] for x in b):
                a[f"[clean] candidates unanimous-wrong, actions {nm}"].append(sum(x["uw_valid"] for x in b) / sum(x["n_valid"] for x in b))
    pols = [p for p in POLS if p in agg]
    lines = [f"# Ground-truth audit for {RES}\n", "| statistic | " + " | ".join(pols) + " |", "|---|" + "---|" * len(pols)]
    for k in agg[pols[0]]:
        lines.append(f"| {k} | " + " | ".join(f"{st.mean(agg[p][k]):.3f}" if agg[p][k] else "–" for p in pols) + " |")
    lines.append("\nContaminated candidate share by environment: " + ", ".join(f"{e} {st.mean(v):.3f}" for e, v in sorted(env_cont.items())))
    open(os.path.join(RES, "analysis", "truth_validation.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
