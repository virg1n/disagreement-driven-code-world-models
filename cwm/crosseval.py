"""Cross-evaluation: each agent's best program tested on the histories collected by the other agents
(same env, different seed), plus held-out accuracy by action kind and trajectory depth.
Usage: python crosseval.py [results_dir]   (default: results/results_v2)"""
import json,glob,os,sys,collections,statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import res
from autumn_env import silence_cpp_stdout; silence_cpp_stdout()
from progexec import Program
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # tables contain non-ASCII; Windows consoles default to cp125x
R=sys.argv[1] if len(sys.argv)>1 else res("results_v2")
eps=[json.load(open(f)) for f in sorted(glob.glob(R+"/*__*__s*.json"))]
POL=["disagree","llm","random"]
def kind(a): return "click" if a.startswith("click") else ("noop" if a=="noop" else "move")
def run(prog, segs, H, W):
    out=[]
    for init,steps in segs:
        acts=[a for a,_ in steps]; obs=[tuple(g) for _,g in steps]
        pr,_,_=prog.run_segment(tuple(init),acts,H,W,observed=obs)
        prev=[tuple(init)]+obs[:-1]
        out+= [(a, p==o, o!=b) for a,p,o,b in zip(acts,pr,obs,prev)]
    return out
cross=collections.defaultdict(list); crossall=collections.defaultdict(list); bykind=collections.defaultdict(list)
depth=collections.defaultdict(list); hist_stats=collections.defaultdict(list)
for e in eps:
    env=e["env"]; ho=json.load(open(f"{R}/heldout/heldout_{env}.json"))
    H=len(e["history"][0]["init"]); W=len(e["history"][0]["init"][0])
    best=min(e["final_pool"], key=lambda p:(-p["fit"],len(p["code"])))
    prog=Program(best["code"],"x",0)
    # held-out by action kind and by step index within trajectory
    for tj in ho["trajectories"]:
        r=run(prog,[(tj["init"],tj["steps"])],H,W)
        for i,(a,ok,chg) in enumerate(r):
            if chg: bykind[(e["policy"],kind(a))].append(ok); depth[(e["policy"], "steps 1-8" if i<8 else "steps 9-25")].append(ok)
    # cross-eval on other episodes' histories (different seed, same env)
    for o in eps:
        if o["env"]!=env or o["seed"]==e["seed"]: continue
        r=run(prog,[(s["init"],s["steps"]) for s in o["history"]],H,W)
        ch=[ok for a,ok,chg in r if chg]
        if ch: cross[(e["policy"],o["policy"])].append(sum(ch)/len(ch))
        crossall[(e["policy"],o["policy"])].append(sum(ok for a,ok,c in r)/len(r))
    # what the agent's own history looks like
    segs=e["history"]; n=sum(len(s["steps"]) for s in segs)
    chg=0; grids=set()
    for s in segs:
        g=tuple(s["init"])
        for a,g2 in s["steps"]:
            chg+= tuple(g2)!=g; grids.add(tuple(g2)); g=tuple(g2)
    hist_stats[(e["policy"],"changing share")].append(chg/n); hist_stats[(e["policy"],"distinct grids")].append(len(grids))
    hist_stats[(e["policy"],"mean segment length")].append(n/len([s for s in segs if s["steps"]]))
print("Best-fit program of ROW policy tested on histories collected by COLUMN policy (other seeds), changing transitions")
print("| trained on \ tested on | "+" | ".join(POL)+" |"); print("|---|---|---|---|")
for p in POL: print(f"| {p} | "+" | ".join(f"{st.mean(cross[(p,q)]):.3f}" for q in POL)+" |")
print("\nSame, all transitions"); 
for p in POL: print(f"| {p} | "+" | ".join(f"{st.mean(crossall[(p,q)]):.3f}" for q in POL)+" |")
print("\nHeld-out accuracy on changing transitions by action kind (n pooled)")
for p in POL: print(p, {k: (round(st.mean(bykind[(p,k)]),3), len(bykind[(p,k)])) for k in ("move","click","noop")}, {d: round(st.mean(depth[(p,d)]),3) for d in ("steps 1-8","steps 9-25")})
print("\nAgent history properties")
for p in POL: print(p, {k: round(st.mean(hist_stats[(p,k)]),2) for k in ("changing share","distinct grids","mean segment length")})
