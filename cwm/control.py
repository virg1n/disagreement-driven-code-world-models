"""Positive control: exploration with *good* hypotheses.

Hypothesis pool = the true Autumn program + every mutant obtained by deleting one `on` clause (run in the real
interpreter, so predictions are exact). Hypotheses are eliminated as soon as they mispredict an observation, so the
pool is an exact version space. Question: does disagreement-driven action selection identify the true program
faster than random / LLM-direct choices on the same candidate menu and budget?
"""
import argparse
import collections
import json
import multiprocessing as mp
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from autumn_env import ENV_DIR, AutumnEnv, apply_action, render  # noqa: E402
from paths import res  # noqa: E402

ENVS = ["grow", "paint", "disease", "ice", "egg", "magnets", "wind", "gravity"]
POLICIES = ["disagree", "disagree_nocost", "disagree_noreset", "random", "llm"]
BUDGET = 40


def on_clause_spans(src):
    """(start, end) spans of top-level `(on ...)` forms inside `(program ...)`."""
    spans, depth, i, start, in_str = [], 0, 0, None, False
    while i < len(src):
        ch = src[i]
        if in_str:
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == ";":
            while i < len(src) and src[i] != "\n":
                i += 1
        elif ch == "(":
            depth += 1
            if depth == 2:
                start = i
        elif ch == ")":
            if depth == 2 and src[start:start + 4] in ("(on ", "(on\n", "(on\t"):
                spans.append((start, i + 1))
            depth -= 1
        i += 1
    return spans


VALIDATE = r"""
import sys, random
sys.path.insert(0, %r)
from MARA.autumn_cpp import Interpreter, autumnstdlib
from autumn_env import apply_action
src = open(sys.argv[1]).read()
it = Interpreter(); it.set_verbose(False)
r = it.run_script(src, autumnstdlib, "", 0)
assert "successfully" in r, r
rng = random.Random(0)
for _ in range(60):
    a = rng.choice(["up", "down", "left", "right", "noop", "click %%d %%d" %% (rng.randrange(16), rng.randrange(16))])
    apply_action(it, a); it.render_all()
print("OK")
""" % HERE


def make_mutants(env_name, tmpdir):
    src = open(os.path.join(ENV_DIR, env_name + ".sexp")).read()
    out = []
    for k, (s, e) in enumerate(on_clause_spans(src)):
        m = src[:s] + src[e:]
        path = os.path.join(tmpdir, f"{env_name}_del{k}.sexp")
        with open(path, "w", encoding="utf-8") as f:
            f.write(m)
        r = subprocess.run([sys.executable, "-c", VALIDATE, path], capture_output=True, text=True, timeout=120)
        if r.returncode == 0 and "OK" in r.stdout:
            out.append((f"del{k}", m))
    return src, out


class Hyp:
    def __init__(self, name, src, seed=0):
        from MARA.autumn_cpp import Interpreter, autumnstdlib
        self.name, self.src, self.seed = name, src, seed
        self._I, self._std = Interpreter, autumnstdlib

    def _new(self):
        it = self._I()
        it.set_verbose(False)
        it.run_script(self.src, self._std, "", self.seed)
        return it

    def simulate(self, seg_actions, actions, from_reset):
        it = self._new()
        if not from_reset:
            for a in seg_actions:
                apply_action(it, a)
                it.render_all()  # keep identical to the live env, which renders after every step
        outs = []
        for a in actions:
            apply_action(it, a)
            outs.append(render(it))
        return tuple(outs)


def entropy(cnt):
    import math
    n = sum(cnt.values())
    return -sum(v / n * math.log2(v / n) for v in cnt.values() if v > 0) if n else 0.0


def run_episode(env_name, policy, seed, mutants, true_src):
    import llm
    import prompts
    from agent import crc, make_candidates, menu_label
    rng = random.Random(crc("control", env_name, policy, seed))
    env = AutumnEnv(env_name)
    hyps = [Hyp("TRUE", true_src)] + [Hyp(n, s) for n, s in mutants]
    alive = list(range(len(hyps)))
    segments = [{"init": env.init_grid, "steps": []}]
    used, counts, log = 0, collections.Counter(), []
    t0 = time.time()
    while used < BUDGET:
        cur = segments[-1]["steps"][-1][1] if segments[-1]["steps"] else segments[-1]["init"]
        cands = [c for c in make_candidates(env.init_grid, cur, segments, rng)
                 if c.cost <= BUDGET - used and not (c.reset and policy.endswith("_noreset"))]
        seg_acts = list(env.segment_actions)
        preds = {h: [hyps[h].simulate(seg_acts, c.actions, c.reset) for c in cands] for h in alive}
        seen_pairs = set()
        for s in segments:
            g = s["init"]
            for a, g2 in s["steps"]:
                seen_pairs.add((g, a))
                g = g2
        seen_prefixes = {tuple(a for a, _ in s["steps"][:k]) for s in segments for k in range(1, len(s["steps"]) + 1)}
        sc = []
        for ci, c in enumerate(cands):
            H = entropy(collections.Counter(preds[h][ci] for h in alive))
            known = (tuple(c.actions) in seen_prefixes) if c.reset else ((cur, c.actions[0]) in seen_pairs)
            v = 0.0 if known else H
            sc.append(dict(H=H, known=known, score=v if policy == "disagree_nocost" else v / c.cost))
        reason = None
        if policy.startswith("disagree"):
            best = max(s["score"] for s in sc)
            tied = [i for i, s in enumerate(sc) if s["score"] >= best - 1e-9]
            if any(not sc[i]["known"] for i in tied):
                tied = [i for i in tied if not sc[i]["known"]]
            mc = min(cands[i].cost for i in tied)
            ci = rng.choice([i for i in tied if cands[i].cost == mc])
        elif policy == "random":
            k = rng.choice(sorted({c.kind for c in cands}))
            ci = rng.choice([i for i, c in enumerate(cands) if c.kind == k])
        elif policy == "llm":
            import re
            menu = [menu_label(c, cur, env.init_grid) for c in cands]
            msgs = prompts.choose_messages(env.H, env.W, env.background(), segments, menu, BUDGET - used)
            text = llm.chat(msgs, n=1, temperature=0.7, max_tokens=600, seed=crc("control", env_name, seed, used))[0]
            m = re.findall(r"ACTION\W*(\d+)", text)
            ci = int(m[-1]) if m and 0 <= int(m[-1]) < len(cands) else rng.randrange(len(cands))
            reason = text[-200:]
        c = cands[ci]
        if c.reset:
            g0 = env.reset()
            segments.append({"init": g0, "steps": []})
            counts["reset"] += 1
        obs = []
        for a in c.actions:
            g = env.step(a)
            segments[-1]["steps"].append((a, g))
            obs.append(g)
            counts["click" if a.startswith("click") else a] += 1
        used += c.cost
        obs = tuple(obs)
        assert preds[0][ci] == obs if 0 in alive else True, "TRUE hypothesis mispredicted: harness bug"
        alive = [h for h in alive if preds[h][ci] == obs]
        log.append(dict(used=used, chosen=c.label, kind=c.kind, H=sc[ci]["H"], known=sc[ci]["known"],
                        H_max=max(s["H"] for s in sc), alive=[hyps[h].name for h in alive], reason=reason))
    prim = sum(counts.values())
    return dict(env=env_name, policy=policy, seed=seed, n_mutants=len(mutants),
                eliminated=[hyps[h].name for h in range(1, len(hyps)) if h not in alive],
                true_alive=0 in alive, counts=dict(counts),
                reset_share=counts["reset"] / prim, noop_share=counts["noop"] / prim,
                coverage=len(env.coverage()) / env.n_clauses, log=log, seconds=round(time.time() - t0, 1))


def job(args):
    env_name, policy, seed, out_dir = args
    from autumn_env import silence_cpp_stdout
    silence_cpp_stdout()
    path = os.path.join(out_dir, f"{env_name}__{policy}__s{seed}.json")
    if os.path.exists(path):
        return
    mut = json.load(open(os.path.join(out_dir, "mutants", f"{env_name}.json")))
    try:
        res = run_episode(env_name, policy, seed, [tuple(m) for m in mut["mutants"]], mut["true"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(res, f)
        sys.stderr.write(f"{env_name} {policy} s{seed}: eliminated {len(res['eliminated'])}/{res['n_mutants']} "
                         f"reset={res['reset_share']:.2f} {res['seconds']}s\n")
    except Exception:  # noqa: BLE001
        import traceback
        with open(path.replace(".json", ".err"), "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=res("results_control"))
    ap.add_argument("--envs", default=",".join(ENVS))
    ap.add_argument("--policies", default=",".join(POLICIES))
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--procs", type=int, default=20)
    a = ap.parse_args()
    md = os.path.join(a.out, "mutants")
    os.makedirs(md, exist_ok=True)
    for e in a.envs.split(","):
        p = os.path.join(md, f"{e}.json")
        if not os.path.exists(p):
            true_src, muts = make_mutants(e, md)
            json.dump(dict(true=true_src, mutants=muts), open(p, "w", encoding="utf-8"))
            sys.stderr.write(f"{e}: {len(muts)} valid single-rule-deletion mutants\n")
    jobs = [(e, p, int(s), a.out) for s in a.seeds.split(",") for e in a.envs.split(",") for p in a.policies.split(",")]
    with mp.get_context("fork").Pool(a.procs, maxtasksperchild=1) as pool:
        list(pool.imap_unordered(job, jobs))


if __name__ == "__main__":
    main()
