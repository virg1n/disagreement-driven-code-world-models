"""Aggregate episode results into tables, paired statistics, figures and the shared-wrong-assumption analysis."""
import sys
import argparse
import collections
import glob
import json
import os
import random
import statistics as st

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from paths import res  # noqa: E402
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # tables contain non-ASCII; Windows consoles default to cp125x

POL_ORDER = ["disagree", "llm", "random", "disagree_noreset"]
POL_NAME = {"disagree": "Disagreement", "llm": "LLM-direct", "random": "Random", "disagree_noreset": "Disagree (no reset)"}
COLORS = {"disagree": "#2a6fdb", "llm": "#e07a1f", "random": "#8a8a8a", "disagree_noreset": "#6bb36b"}


def load(d):
    rs = []
    for f in sorted(glob.glob(os.path.join(d, "*__*__s*.json"))):
        with open(f) as fh:
            rs.append(json.load(fh))
    return rs


def mean_sem(xs):
    xs = list(xs)
    if not xs:
        return float("nan"), float("nan")
    m = st.mean(xs)
    s = st.stdev(xs) / len(xs) ** 0.5 if len(xs) > 1 else 0.0
    return m, s


def boot_ci(diffs, n=10000, seed=0):
    rng = random.Random(seed)
    ms = sorted(st.mean(rng.choices(diffs, k=len(diffs))) for _ in range(n))
    return ms[int(0.025 * n)], ms[int(0.975 * n)]


def sign_test_p(diffs):
    pos = sum(d > 0 for d in diffs)
    neg = sum(d < 0 for d in diffs)
    n = pos + neg
    if n == 0:
        return 1.0
    from math import comb
    k = min(pos, neg)
    p = sum(comb(n, i) for i in range(k + 1)) / 2 ** n * 2
    return min(1.0, p)


def metrics(r):
    ho = r["heldout"]
    log = r["log"]
    n_dec = len(log)
    return dict(
        coverage=r["coverage"],
        ho_acc=ho["best_by_fit"]["acc"],
        ho_acc_chg=ho["best_by_fit"]["acc_changing"],
        ho_oracle=ho["oracle_best"]["acc"],
        ho_oracle_chg=ho["oracle_best"]["acc_changing"],
        ho_pool_mean=ho.get("mean_pool_acc", float("nan")),
        best_fit=ho["best_by_fit"]["fit"],
        reset_share=r["reset_share"],
        noop_share=r["noop_share"],
        reset_noop=r["reset_noop_share"],
        n_decisions=n_dec,
        llm_calls=r["llm_usage"]["calls"],
        gen_tokens=r["llm_usage"]["completion_tokens"],
        frac_Hmax0=sum(l["H_max"] <= 1e-9 for l in log) / n_dec,
        frac_blind=sum(l["H_max"] <= 1e-9 and l["n_unanimous_wrong"] > 0 for l in log) / n_dec,
        cand_unan_wrong=sum(l["n_unanimous_wrong"] for l in log) / max(1, sum(l["n_cands"] for l in log)),
        chosen_unan_wrong=sum(l["chosen_unanimous_wrong"] for l in log) / n_dec,
        mean_H_chosen=st.mean(l["H_chosen"] for l in log),
        ho_unanimous_wrong_of_failed=(ho["categories"].get("unanimous_wrong", 0)
                                      / max(1, ho["categories"].get("unanimous_wrong", 0) + ho["categories"].get("all_wrong_disagree", 0))),
        ho_unanimous_wrong=ho["categories"].get("unanimous_wrong", 0) / ho["n_heldout"],
        ho_all_wrong=(ho["categories"].get("unanimous_wrong", 0) + ho["categories"].get("all_wrong_disagree", 0)) / ho["n_heldout"],
        identity_acc=ho["identity_acc"],
    )


def curve(r, key="heldout_best", grid=range(0, 41, 2)):
    pts = [(0, None)] + [(l["used"], l[key]) for l in r["log"]]
    out = []
    for u in grid:
        vals = [v for (x, v) in pts if x <= u and v is not None]
        out.append(vals[-1] if vals else float("nan"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", default=res("results_v2"))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(a.res, "analysis")
    os.makedirs(out, exist_ok=True)
    rs = load(a.res)
    pols = [p for p in POL_ORDER if any(r["policy"] == p for r in rs)]
    envs = sorted({r["env"] for r in rs})
    by = collections.defaultdict(list)
    for r in rs:
        by[(r["env"], r["policy"])].append(r)
    M = {(r["env"], r["policy"], r["seed"]): metrics(r) for r in rs}
    keys = list(next(iter(M.values())).keys())
    lines = [f"# Results ({len(rs)} episodes, envs={envs}, policies={pols})\n"]

    # ---- overall table ----
    lines.append("## Overall (mean ± s.e.m. over env×seed episodes)\n")
    lines.append("| metric | " + " | ".join(POL_NAME[p] for p in pols) + " |")
    lines.append("|---|" + "---|" * len(pols))
    agg = {}
    for k in keys:
        row = []
        for p in pols:
            m, s = mean_sem(v[k] for (e, pp, sd), v in M.items() if pp == p)
            agg[(k, p)] = (m, s)
            row.append(f"{m:.3f} ± {s:.3f}")
        lines.append(f"| {k} | " + " | ".join(row) + " |")

    # ---- paired comparisons ----
    lines.append("\n## Paired differences (same env & seed)\n")
    lines.append("| metric | comparison | mean diff | 95% bootstrap CI | wins/ties/losses | sign-test p |")
    lines.append("|---|---|---|---|---|---|")
    for k in ["coverage", "ho_acc", "ho_acc_chg", "ho_oracle", "ho_oracle_chg", "reset_noop", "ho_unanimous_wrong"]:
        for p2 in [p for p in pols if p != "disagree"]:
            diffs = []
            for (e, pp, sd), v in M.items():
                if pp == "disagree" and (e, p2, sd) in M:
                    diffs.append(v[k] - M[(e, p2, sd)][k])
            if not diffs:
                continue
            lo, hi = boot_ci(diffs)
            w = sum(d > 1e-12 for d in diffs)
            l_ = sum(d < -1e-12 for d in diffs)
            lines.append(f"| {k} | disagree − {p2} | {st.mean(diffs):+.3f} | [{lo:+.3f}, {hi:+.3f}] | "
                         f"{w}/{len(diffs) - w - l_}/{l_} | {sign_test_p(diffs):.3f} |")

    # ---- per env ----
    lines.append("\n## Per environment (mean over seeds)\n")
    for k in ["coverage", "ho_acc", "ho_acc_chg", "ho_oracle_chg", "reset_noop", "ho_unanimous_wrong_of_failed"]:
        lines.append(f"\n**{k}**\n")
        lines.append("| env | " + " | ".join(POL_NAME[p] for p in pols) + " |")
        lines.append("|---|" + "---|" * len(pols))
        for e in envs:
            cells = []
            for p in pols:
                vs = [M[(e, p, r["seed"])][k] for r in by[(e, p)]]
                cells.append(f"{st.mean(vs):.2f}" if vs else "–")
            lines.append(f"| {e} | " + " | ".join(cells) + " |")

    # ---- action distribution ----
    lines.append("\n## Action distribution (share of primitive actions)\n")
    lines.append("| policy | up/down/left/right | click | noop | reset |")
    lines.append("|---|---|---|---|---|")
    for p in pols:
        c = collections.Counter()
        for r in rs:
            if r["policy"] == p:
                c.update(r["action_counts"])
        n = sum(c.values())
        mv = sum(c[m] for m in ("up", "down", "left", "right"))
        lines.append(f"| {POL_NAME[p]} | {mv / n:.3f} | {c['click'] / n:.3f} | {c['noop'] / n:.3f} | {c['reset'] / n:.3f} |")

    # ---- shared wrong assumption: held-out categories ----
    lines.append("\n## Final program pool on held-out transitions\n")
    lines.append("| policy | all correct | some correct | all wrong, disagree | all wrong, UNANIMOUS |")
    lines.append("|---|---|---|---|---|")
    for p in pols:
        c = collections.Counter()
        for r in rs:
            if r["policy"] == p:
                c.update(r["heldout"]["categories"])
        n = sum(c.values())
        lines.append(f"| {POL_NAME[p]} | " + " | ".join(f"{c[k] / n:.3f}" for k in
                     ["all_correct", "some_correct", "all_wrong_disagree", "unanimous_wrong"]) + " |")

    # ---- per-clause: which rules are unanimously mis-modelled ----
    lines.append("\n## Per rule (on-clause) on held-out: share of first-firing transitions where the final pool is unanimously wrong\n")
    lines.append("| env | clause | n | " + " | ".join(POL_NAME[p] for p in pols) + " |")
    lines.append("|---|---|---|" + "---|" * len(pols))
    for e in envs:
        clauses = sorted({int(k) for p in pols for r in by[(e, p)] for k in r["heldout"]["per_clause"]})
        for cl in clauses:
            cells, nn = [], 0
            for p in pols:
                c = collections.Counter()
                for r in by[(e, p)]:
                    c.update(r["heldout"]["per_clause"].get(str(cl), {}))
                n = sum(c.values())
                nn = max(nn, n // max(1, len(by[(e, p)])))
                cells.append(f"{c['unanimous_wrong'] / n:.2f}" if n else "–")
            lines.append(f"| {e} | {cl} | {nn} | " + " | ".join(cells) + " |")

    # ---- surprises: executed actions whose outcome the whole pool got wrong unanimously ----
    lines.append("\n## Exposure of shared wrong assumptions during exploration\n")
    lines.append("Decisions where the executed action had a unanimous-but-wrong pool prediction (the only way a shared "
                 "error gets exposed), and decisions where no candidate had any disagreement (H_max = 0).\n")
    lines.append("| policy | decisions | chosen unanimous-wrong (exposures) | H_max = 0 | H_max = 0 while some candidate unanimous-wrong (blind spot) | candidates unanimous-wrong |")
    lines.append("|---|---|---|---|---|---|")
    for p in pols:
        logs = [l for r in rs if r["policy"] == p for l in r["log"]]
        n = len(logs)
        nc = sum(l["n_cands"] for l in logs)
        lines.append(f"| {POL_NAME[p]} | {n} | {sum(l['chosen_unanimous_wrong'] for l in logs) / n:.3f} | "
                     f"{sum(l['H_max'] <= 1e-9 for l in logs) / n:.3f} | "
                     f"{sum(l['H_max'] <= 1e-9 and l['n_unanimous_wrong'] > 0 for l in logs) / n:.3f} | "
                     f"{sum(l['n_unanimous_wrong'] for l in logs) / nc:.3f} |")

    with open(os.path.join(out, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(out, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump({f"{e}|{p}|{s}": v for (e, p, s), v in M.items()}, f, indent=1)

    # ---- figures ----
    grid = list(range(0, 41, 2))
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    for ax, key, title in [(axes[0], "heldout_best", "Held-out accuracy of best-fit program"),
                           (axes[1], "coverage", "Rule (on-clause) coverage")]:
        for p in pols:
            cs = []
            for r in rs:
                if r["policy"] != p:
                    continue
                if key == "coverage":
                    pts = [(0, 0.0)] + [(l["used"], len(l["coverage"]) / r["n_clauses"]) for l in r["log"]]
                    cs.append([max([v for x, v in pts if x <= u] or [0.0]) for u in grid])
                else:
                    cs.append(curve(r, key, grid))
            ms = [st.mean([c[i] for c in cs if c[i] == c[i]] or [float("nan")]) for i in range(len(grid))]
            ax.plot(grid, ms, label=POL_NAME[p], color=COLORS[p], lw=2)
        ax.set_xlabel("actions used")
        ax.set_title(title, fontsize=10)
        ax.grid(alpha=0.3)
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "curves.png"), dpi=150)

    fig, axes = plt.subplots(1, 3, figsize=(14, 3.6))
    w = 0.8 / len(pols)
    for ax, k, title in [(axes[0], "coverage", "Rule coverage"), (axes[1], "ho_acc_chg", "Held-out acc. (changing transitions)"),
                         (axes[2], "reset_noop", "Reset + no-op share")]:
        for j, p in enumerate(pols):
            vals = [st.mean([M[(e, p, r["seed"])][k] for r in by[(e, p)]] or [float("nan")]) for e in envs]
            ax.bar([i + j * w for i in range(len(envs))], vals, w, label=POL_NAME[p], color=COLORS[p])
        ax.set_xticks([i + w * (len(pols) - 1) / 2 for i in range(len(envs))])
        ax.set_xticklabels(envs, rotation=45, fontsize=8)
        ax.set_title(title, fontsize=10)
        ax.grid(axis="y", alpha=0.3)
    axes[2].axhline(0.25, ls="--", color="k", lw=1)
    axes[2].text(0, 0.26, "humans ≈ 25%", fontsize=7)
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "per_env.png"), dpi=150)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
