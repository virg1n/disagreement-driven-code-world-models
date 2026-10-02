"""Offline re-synthesis: fixed synthesis budget from each agent's collected history.

Decouples the informativeness of the collected data from the online pool dynamics (which differ between
policies in the number of repair rounds). For each episode: N fresh samples from the synthesis prompt given the
full history, pick the best fit to that history, score on the held-out set.
"""
import argparse
import glob
import json
import multiprocessing as mp
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths import res  # noqa: E402

N_SAMPLES = 16


def fit_and_heldout(code, segments, ho, H, W):
    from progexec import Program
    p = Program(code, "resynth", 0)
    n = ok = 0
    for s in segments:
        acts = [a for a, _ in s["steps"]]
        obs = [tuple(g) for _, g in s["steps"]]
        pr, _, _ = p.run_segment(tuple(s["init"]), acts, H, W, observed=obs)
        n += len(obs)
        ok += sum(x == y for x, y in zip(pr, obs))
    tot = cor = tot_c = cor_c = 0
    for tj in ho["trajectories"]:
        acts = [a for a, _ in tj["steps"]]
        obs = [tuple(g) for _, g in tj["steps"]]
        pr, _, _ = p.run_segment(tuple(tj["init"]), acts, H, W, observed=obs)
        before = [tuple(tj["init"])] + obs[:-1]
        for x, y, b in zip(pr, obs, before):
            tot += 1
            cor += x == y
            if y != b:
                tot_c += 1
                cor_c += x == y
    return dict(fit=ok / max(1, n), acc=cor / tot, acc_changing=cor_c / max(1, tot_c), code_len=len(code))


def one(args):
    path, out_dir = args
    from autumn_env import AutumnEnv, silence_cpp_stdout
    silence_cpp_stdout()
    import llm
    import prompts
    from progexec import extract_code
    out = os.path.join(out_dir, os.path.basename(path))
    if os.path.exists(out):
        return
    r = json.load(open(path))
    ho = json.load(open(os.path.join(os.path.dirname(path), "heldout", f"heldout_{r['env']}.json")))
    env = AutumnEnv(r["env"])
    segs = [dict(init=tuple(s["init"]), steps=[(a, tuple(g)) for a, g in s["steps"]]) for s in r["history"]]
    msgs = prompts.synth_messages(env.H, env.W, env.background(), segs)
    texts = llm.chat(msgs, n=N_SAMPLES, temperature=0.8, max_tokens=1000)
    res = [fit_and_heldout(extract_code(t), segs, ho, env.H, env.W) for t in texts]
    best = min(res, key=lambda d: (-d["fit"], d["code_len"]))
    summary = dict(env=r["env"], policy=r["policy"], seed=r["seed"], n=len(res), samples=res, best_by_fit=best,
                   oracle=max(res, key=lambda d: d["acc"]),
                   mean_acc=sum(d["acc"] for d in res) / len(res),
                   mean_acc_changing=sum(d["acc_changing"] for d in res) / len(res))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(summary, f)
    sys.stderr.write(f"{r['env']} {r['policy']} s{r['seed']}: best fit={best['fit']:.2f} acc={best['acc']:.2f} "
                     f"chg={best['acc_changing']:.2f}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", default=res("results_v2"))
    ap.add_argument("--procs", type=int, default=12)
    a = ap.parse_args()
    out_dir = os.path.join(a.res, "resynth")
    os.makedirs(out_dir, exist_ok=True)
    jobs = [(p, out_dir) for p in sorted(glob.glob(os.path.join(a.res, "*__*__s*.json")))]
    with mp.get_context("fork").Pool(a.procs, maxtasksperchild=1) as pool:
        list(pool.imap_unordered(one, jobs))


if __name__ == "__main__":
    main()
