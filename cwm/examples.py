"""Characterise shared wrong assumptions: held-out transitions where every program in the final pool makes the
same wrong prediction. Re-runs the saved final pools (so must run where the programs can execute)."""
import argparse
import collections
import glob
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autumn_env import silence_cpp_stdout  # noqa: E402
from progexec import Program  # noqa: E402
from prompts import fmt_changes  # noqa: E402
from paths import res  # noqa: E402
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # tables contain non-ASCII; Windows consoles default to cp125x


def akind(a):
    return "click" if a.startswith("click") else ("noop" if a == "noop" else "move")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", default=res("results_v2"))
    ap.add_argument("--n_examples", type=int, default=3)
    a = ap.parse_args()
    silence_cpp_stdout()
    rng = random.Random(0)
    table = collections.defaultdict(collections.Counter)  # policy -> (err_type, action_kind) counts
    env_table = collections.defaultdict(collections.Counter)
    examples = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(a.res, "*__*__s*.json"))):
        r = json.load(open(f))
        ho = json.load(open(os.path.join(a.res, "heldout", f"heldout_{r['env']}.json")))
        progs = [Program(p["code"], p["origin"], p["birth"]) for p in r["final_pool"]]
        H = len(ho["trajectories"][0]["init"])
        W = len(ho["trajectories"][0]["init"][0])
        preds = []
        for p in progs:
            pr_all = []
            for tj in ho["trajectories"]:
                acts = [x for x, _ in tj["steps"]]
                obs = [tuple(g) for _, g in tj["steps"]]
                pr, _, _ = p.run_segment(tuple(tj["init"]), acts, H, W, observed=obs)
                pr_all += pr
            preds.append(pr_all)
        i = 0
        for tj in ho["trajectories"]:
            g = tuple(tj["init"])
            for (act, g2), tags in zip(tj["steps"], tj["tags"]):
                g2 = tuple(g2)
                outs = [pp[i] for pp in preds]
                if all(o is not None for o in outs) and len(set(outs)) == 1 and outs[0] != g2:
                    pred = outs[0]
                    real_change = g2 != g
                    pred_change = pred != g
                    if real_change and not pred_change:
                        et = "missed change (predicted nothing happens)"
                    elif pred_change and not real_change:
                        et = "hallucinated change (nothing actually happens)"
                    else:
                        et = "wrong change"
                    table[r["policy"]][(et, akind(act))] += 1
                    env_table[r["env"]][(et, akind(act))] += 1
                    examples[(r["env"], et, akind(act))].append(dict(
                        policy=r["policy"], seed=r["seed"], action=act, tags=tags,
                        predicted=fmt_changes(g, pred), actual=fmt_changes(g, g2)))
                g = g2
                i += 1
    lines = ["# Shared wrong assumptions on held-out transitions (final pools, all programs agree and are wrong)\n"]
    kinds = ["move", "click", "noop"]
    ets = ["missed change (predicted nothing happens)", "hallucinated change (nothing actually happens)", "wrong change"]
    for title, tab in [("by policy", table), ("by environment", env_table)]:
        lines.append(f"\n## Error type × action kind, {title}\n")
        lines.append("| group | " + " | ".join(f"{e.split(' (')[0]} / {k}" for e in ets for k in kinds) + " | total |")
        lines.append("|---|" + "---|" * (len(ets) * len(kinds) + 1))
        for grp, c in sorted(tab.items()):
            lines.append(f"| {grp} | " + " | ".join(str(c[(e, k)]) for e in ets for k in kinds) + f" | {sum(c.values())} |")
    lines.append("\n## Examples\n")
    for key in sorted(examples):
        ex = examples[key]
        lines.append(f"\n### {key[0]} — {key[1]} — {key[2]} ({len(ex)} cases)\n")
        for e in rng.sample(ex, min(a.n_examples, len(ex))):
            lines.append(f"- [{e['policy']} s{e['seed']}] action `{e['action']}` (first-firing clauses {e['tags']})\n"
                         f"  - predicted: `{e['predicted'][:220]}`\n  - actual: `{e['actual'][:220]}`")
    out = os.path.join(a.res, "analysis", "shared_wrong.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))


if __name__ == "__main__":
    main()
