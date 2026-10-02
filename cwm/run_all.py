"""Run all (env, policy, seed) episodes in parallel worker processes against the shared vLLM server.

Resumable: an episode is skipped if its result file already exists.
"""
import argparse
import json
import multiprocessing as mp
import os
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths import res  # noqa: E402

ENVS = ["grow", "paint", "disease", "ice", "egg", "magnets", "wind", "gravity"]
POLICIES = ["disagree", "llm", "random"]


def run_one(job):
    env_name, policy, seed, out_dir, cfg = job
    from autumn_env import silence_cpp_stdout
    silence_cpp_stdout()
    import heldout
    from agent import Episode
    path = os.path.join(out_dir, f"{env_name}__{policy}__s{seed}.json")
    if os.path.exists(path):
        return path, "skip"
    t0 = time.time()
    try:
        ho = heldout.load_or_make(env_name, os.path.join(out_dir, "heldout"))
        ep = Episode(env_name, policy, seed, ho, out_dir, cfg=cfg)
        res = ep.run()
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(res, f)
        os.replace(tmp, path)
        msg = (f"done cov={res['coverage']:.2f} ho_best={res['heldout']['best_by_fit']['acc']:.3f} "
               f"reset+noop={res['reset_noop_share']:.2f} {time.time() - t0:.0f}s")
    except Exception:  # noqa: BLE001
        msg = "ERROR\n" + traceback.format_exc()
        with open(path.replace(".json", ".err"), "w", encoding="utf-8") as f:
            f.write(msg)
    sys.stderr.write(f"[{time.strftime('%H:%M:%S')}] {env_name} {policy} s{seed}: {msg}\n")
    sys.stderr.flush()
    return path, msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--envs", default=",".join(ENVS))
    ap.add_argument("--policies", default=",".join(POLICIES))
    ap.add_argument("--seeds", default="0,1")
    ap.add_argument("--procs", type=int, default=10)
    ap.add_argument("--out", default=res("results_v2"))
    ap.add_argument("--cfg", default="{}", help="JSON overrides for agent.CFG")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cfg = json.loads(a.cfg)
    from autumn_env import silence_cpp_stdout
    silence_cpp_stdout()
    import heldout
    for e in a.envs.split(","):  # generate once, before workers race on the files
        heldout.load_or_make(e, os.path.join(a.out, "heldout"))
    jobs = [(e, p, int(s), a.out, cfg) for s in a.seeds.split(",") for e in a.envs.split(",") for p in a.policies.split(",")]
    sys.stderr.write(f"{len(jobs)} jobs, {a.procs} procs -> {a.out}\n")
    with mp.get_context("fork").Pool(a.procs, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(run_one, jobs):
            pass


if __name__ == "__main__":
    main()
