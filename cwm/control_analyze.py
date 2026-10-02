"""Summarise the positive-control runs (true program + single-rule-deletion mutants)."""
import collections
import glob
import json
import os
import random
import statistics as st
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import res  # noqa: E402
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # tables contain non-ASCII; Windows consoles default to cp125x

RES = sys.argv[1] if len(sys.argv) > 1 else res("results_control")
POLS = ["disagree", "disagree_nocost", "disagree_noreset", "llm", "random"]
NAMES = {"disagree": "Disagreement (H/cost)", "disagree_nocost": "Disagreement (raw H)",
         "disagree_noreset": "Disagreement, no reset", "llm": "LLM-direct", "random": "Random"}

rs = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(RES, "*__*__s*.json")))]
# a mutant counts as distinguishable if any run in that environment eliminated it
dist = collections.defaultdict(set)
for r in rs:
    dist[r["env"]] |= set(r["eliminated"])
grid = list(range(0, 41, 2))


def frac_curve(r):
    d = dist[r["env"]]
    if not d:
        return None
    pts = [(0, 0.0)]
    all_names = set(d)
    for l in r["log"]:
        pts.append((l["used"], len(all_names - set(l["alive"])) / len(d)))
    return [max([v for x, v in pts if x <= u]) for u in grid]


def actions_to_identify(r):
    d = dist[r["env"]]
    for l in r["log"]:
        if not (d & set(l["alive"])):
            return l["used"]
    return 41  # not identified within budget


rows = collections.defaultdict(lambda: collections.defaultdict(list))
M = {}
for r in rs:
    c = frac_curve(r)
    if c is None:
        continue
    m = dict(final=c[-1], at10=c[5], at20=c[10], auc=st.mean(c), t_id=actions_to_identify(r),
             identified=actions_to_identify(r) <= 40, reset=r["reset_share"], noop=r["noop_share"], coverage=r["coverage"])
    M[(r["env"], r["policy"], r["seed"])] = m
    for k, v in m.items():
        rows[r["policy"]][k].append(v)

lines = ["# Positive control: true program + single-rule-deletion mutants\n",
         "Distinguishable mutants per env: " + ", ".join(f"{e} {len(d)}" for e, d in sorted(dist.items())) + "\n",
         "| policy | n | eliminated @10 | @20 | @40 | area under curve | identified within 40 | actions to identify (41 = not) | reset share | no-op share | rule coverage |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
pols = [p for p in POLS if p in rows]
for p in pols:
    a = rows[p]
    lines.append(f"| {NAMES[p]} | {len(a['final'])} | {st.mean(a['at10']):.2f} | {st.mean(a['at20']):.2f} | {st.mean(a['final']):.2f} | "
                 f"{st.mean(a['auc']):.2f} | {st.mean(a['identified']):.2f} | {st.mean(a['t_id']):.1f} | {st.mean(a['reset']):.3f} | "
                 f"{st.mean(a['noop']):.3f} | {st.mean(a['coverage']):.2f} |")


def boot(d, n=10000):
    rng = random.Random(0)
    ms = sorted(st.mean(rng.choices(d, k=len(d))) for _ in range(n))
    return ms[250], ms[9750]


lines += ["\n| metric | comparison | mean diff | 95% CI | W/T/L |", "|---|---|---|---|---|"]
for k in ["auc", "at10", "at20", "final", "t_id"]:
    for p2 in [p for p in pols if p != "disagree"]:
        d = [M[(e, "disagree", s)][k] - M[(e, p2, s)][k] for (e, p, s) in M if p == "disagree" and (e, p2, s) in M]
        if d:
            lo, hi = boot(d)
            w, l_ = sum(x > 1e-12 for x in d), sum(x < -1e-12 for x in d)
            lines.append(f"| {k} | disagree − {p2} | {st.mean(d):+.3f} | [{lo:+.3f}, {hi:+.3f}] | {w}/{len(d) - w - l_}/{l_} |")

lines += ["\n## Per environment: fraction of distinguishable mutants eliminated by 20 actions\n",
          "| env | " + " | ".join(NAMES[p] for p in pols) + " |", "|---|" + "---|" * len(pols)]
for e in sorted(dist):
    lines.append(f"| {e} | " + " | ".join(
        f"{st.mean([M[k]['at20'] for k in M if k[0] == e and k[1] == p]):.2f}" if any(k[0] == e and k[1] == p for k in M) else "–"
        for p in pols) + " |")

out = os.path.join(RES, "analysis")
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "control_summary.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))

fig, ax = plt.subplots(figsize=(5.5, 3.6))
cols = {"disagree": "#2a6fdb", "disagree_nocost": "#7b4fd6", "disagree_noreset": "#6bb36b", "llm": "#e07a1f", "random": "#8a8a8a"}
for p in pols:
    cs = [frac_curve(r) for r in rs if r["policy"] == p and frac_curve(r) is not None]
    ax.plot(grid, [st.mean(c[i] for c in cs) for i in range(len(grid))], label=NAMES[p], color=cols[p], lw=2)
ax.set_xlabel("actions used")
ax.set_ylabel("distinguishable mutants eliminated")
ax.set_title("Positive control: exact hypotheses", fontsize=10)
ax.grid(alpha=0.3)
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(out, "control_curves.png"), dpi=150)
