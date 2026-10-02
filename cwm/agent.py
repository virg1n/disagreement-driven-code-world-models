"""One exploration episode: a pool of LLM-written world-model programs plus an action-selection policy.

Policies (everything else — model, budget, candidate menu, synthesis/repair procedure — is shared):
  disagree : pick the candidate whose predicted outcomes (across the program pool) have maximum entropy per action spent
  llm      : the same 7B LLM picks from the same menu, given the same history
  random   : uniform over menu categories (move / noop / click / reset-macro), then uniform within
"""
import collections
import json
import math
import os
import random
import re
import sys
import time
import zlib

import llm
import prompts
from autumn_env import BG, MOVES, AutumnEnv
from progexec import Program, extract_code, safe_deepcopy

CFG = dict(K=6, BUDGET=40, FRESH=2, MAX_REPAIR=4, N_CLICK_OBJ=4, N_CLICK_ANY=2,
           T_SYNTH=0.8, T_REPAIR=0.7, T_ACT=0.7, MAX_TOKENS=1000, MAX_MISMATCH_SHOWN=3,
           # v2 fixes (audit): soft version-space weighting, zero value for already-known outcomes,
           # behavioural de-duplication of the pool. Set all three off to reproduce v1.
           VS_LAMBDA=1.0, KNOWN_ZERO=True, DEDUPE_BEHAVIOUR=True)


def crc(*xs):
    return zlib.crc32("|".join(map(str, xs)).encode())


class Candidate:
    def __init__(self, label, actions, reset, kind):
        self.label, self.actions, self.reset, self.kind = label, actions, reset, kind

    @property
    def cost(self):
        return len(self.actions) + (1 if self.reset else 0)


def sample_clicks(grid, rng, n_obj, n_any):
    H, W = len(grid), len(grid[0])
    by_color = collections.defaultdict(list)
    for y in range(H):
        for x in range(W):
            if grid[y][x] != BG:
                by_color[grid[y][x]].append((x, y))
    colors = sorted(by_color)
    rng.shuffle(colors)
    picks = []
    while len(picks) < n_obj and any(by_color[c] for c in colors):
        for c in colors:  # round-robin over colors so small objects are not drowned out by large ones
            if by_color[c] and len(picks) < n_obj:
                p = rng.choice(by_color[c])
                by_color[c].remove(p)
                picks.append(p)
    picks += [(rng.randrange(W), rng.randrange(H)) for _ in range(n_any)]
    out, seen = [], set()
    for p in picks:
        if p not in seen:
            seen.add(p)
            out.append(f"click {p[0]} {p[1]}")
    return out


def make_candidates(init_grid, cur_grid, segments, rng):
    c = [Candidate(a, [a], False, "move") for a in MOVES]
    c.append(Candidate("noop", ["noop"], False, "noop"))
    c += [Candidate(a, [a], False, "click") for a in sample_clicks(cur_grid, rng, CFG["N_CLICK_OBJ"], CFG["N_CLICK_ANY"])]
    at_initial = not segments[-1]["steps"]
    if not at_initial:  # a reset macro from the initial state is a strictly more expensive primitive action
        for a in list(MOVES) + ["noop"] + sample_clicks(init_grid, rng, 2, 1):
            c.append(Candidate(f"RESET, then {a}", [a], True, "reset"))
        seg_acts = [a for a, _ in segments[-1]["steps"]]
        if len(seg_acts) >= 2:
            r = seg_acts[:2]
            c.append(Candidate(f"RESET, then replay {r[0]}; {r[1]}", r, True, "reset"))
    return c


def menu_label(c, cur_grid, init_grid):
    def desc(a, g):
        if a.startswith("click"):
            _, x, y = a.split()
            ch = g[int(y)][int(x)]
            return f"{a} (cell is '{ch}')"
        return a
    if c.reset:
        return "RESET (cost 1), then " + "; then ".join(desc(a, init_grid) for a in c.actions) + f"   [total cost {c.cost}]"
    return desc(c.actions[0], cur_grid)


def entropy(counter):
    n = sum(counter.values())
    return -sum(v / n * math.log2(v / n) for v in counter.values() if v > 0) if n > 0 else 0.0


class Episode:
    def __init__(self, env_name, policy, seed, heldout, out_dir, cfg=None):
        self.cfg = dict(CFG, **(cfg or {}))
        self.env_name, self.policy, self.seed = env_name, policy, seed
        self.heldout = heldout
        self.out_dir = out_dir
        self.rng = random.Random(crc(env_name, policy, seed))
        self.env = AutumnEnv(env_name)
        self.H, self.W = self.env.H, self.env.W
        self.bg = self.env.background()
        self.segments = [{"init": self.env.init_grid, "steps": []}]
        self.pool = []
        self.used = 0
        self.decision = 0
        self.log = []
        self.counts = collections.Counter()
        self.llm_calls = collections.Counter()
        self.surprises = []  # executed transitions where the pool had been unanimous and wrong

    # ---------- history helpers ----------
    def cur_grid(self):
        s = self.segments[-1]
        return s["steps"][-1][1] if s["steps"] else s["init"]

    def transitions(self):
        """Flat list of (segment_idx, step_idx, g_before, action, g_after)."""
        out = []
        for si, s in enumerate(self.segments):
            g = s["init"]
            for ti, (a, g2) in enumerate(s["steps"]):
                out.append((si, ti, g, a, g2))
                g = g2
        return out

    # ---------- program evaluation ----------
    def evaluate(self, p):
        preds, errs, mem = [], [], {}
        for s in self.segments:
            acts = [a for a, _ in s["steps"]]
            obs = [g for _, g in s["steps"]]
            pr, er, mem = p.run_segment(s["init"], acts, self.H, self.W, observed=obs)
            preds += pr
            errs += er
        tr = self.transitions()
        p.hist_preds = preds
        p.hist_errs = errs
        p.hist_correct = [pr == t[4] for pr, t in zip(preds, tr)]
        p.acc = sum(p.hist_correct) / len(tr) if tr else 0.0
        p.n_wrong = len(tr) - sum(p.hist_correct)
        p.cur_mem = mem  # mem at the end of the current segment

    def predict(self, p, c, cur_grid):
        if c.reset:
            preds, _, _ = p.run_segment(self.env.init_grid, c.actions, self.H, self.W, observed=None)
            return tuple(preds) if all(x is not None for x in preds) else None
        g, _ = p.call(cur_grid, c.actions[0], safe_deepcopy(p.cur_mem), self.H, self.W)
        return (g,) if g is not None else None

    # ---------- synthesis ----------
    def _new_programs(self, texts, origin, parent=None):
        progs = []
        for t in texts:
            p = Program(extract_code(t), origin, self.decision, parent=parent)
            self.evaluate(p)
            progs.append(p)
        return progs

    def synthesize_initial(self):
        msgs = prompts.synth_messages(self.H, self.W, self.bg, self.segments)
        texts = llm.chat(msgs, n=self.cfg["K"], temperature=self.cfg["T_SYNTH"], max_tokens=self.cfg["MAX_TOKENS"],
                         seed=crc(self.env_name, self.seed, "init"))
        self.llm_calls["synth"] += 1
        self.pool = self._new_programs(texts, "init")

    def update_pool(self, new_idx):
        tr = self.transitions()
        for p in self.pool:
            self.evaluate(p)
        contradicted = [p for p in self.pool if p.acc < 1.0 or not p.ok]
        # repair priority: programs contradicted by the newest observation first, then the most accurate ones
        contradicted.sort(key=lambda p: (not any(not p.hist_correct[i] for i in new_idx), -p.acc))
        to_repair = contradicted[: self.cfg["MAX_REPAIR"]]
        jobs = []
        for j, p in enumerate(to_repair):
            wrong = [i for i, ok in enumerate(p.hist_correct) if not ok]
            wrong = sorted(wrong, key=lambda i: (i not in new_idx, -i))[: self.cfg["MAX_MISMATCH_SHOWN"]]
            mm = [prompts.fmt_mismatch(i + 1, tr[i][3], tr[i][2], p.hist_preds[i], tr[i][4], p.hist_errs[i]) for i in wrong]
            if not p.ok:
                mm = [f"The program failed to load: {p.err}"]
            msgs = prompts.repair_messages(self.H, self.W, self.bg, self.segments, p.code, mm, sum(p.hist_correct), len(tr))
            jobs.append(dict(messages=msgs, n=1, temperature=self.cfg["T_REPAIR"], max_tokens=self.cfg["MAX_TOKENS"],
                             seed=crc(self.env_name, self.seed, self.policy, self.decision, "rep", j)))
        if self.cfg["FRESH"] > 0:
            jobs.append(dict(messages=prompts.synth_messages(self.H, self.W, self.bg, self.segments), n=self.cfg["FRESH"],
                             temperature=self.cfg["T_SYNTH"], max_tokens=self.cfg["MAX_TOKENS"],
                             seed=crc(self.env_name, self.seed, self.policy, self.decision, "fresh")))
        results = llm.chat_many(jobs)
        new = []
        for j, p in enumerate(to_repair):
            new += self._new_programs(results[j], "repair", parent=p.pid)
        if self.cfg["FRESH"] > 0:
            new += self._new_programs(results[-1], "fresh")
        self.llm_calls["repair"] += len(to_repair)
        self.llm_calls["fresh"] += 1 if self.cfg["FRESH"] > 0 else 0
        # keep the K best by fit to the history; ties go to newer programs; drop duplicates
        # (v1: identical code; v2: identical predictions on the history and on probe actions from the current state)
        cur = self.cur_grid()
        probes = list(MOVES) + ["noop"] + sample_clicks(cur, random.Random(crc(self.seed, self.decision)), 3, 0)
        allp, seen = [], set()
        for p in sorted(self.pool + new, key=lambda p: (-p.acc if p.ok else 1, -p.birth_step, -p.pid)):
            if self.cfg["DEDUPE_BEHAVIOUR"] and p.ok:
                sig = (tuple(p.hist_preds), tuple(p.call(cur, a, safe_deepcopy(p.cur_mem), self.H, self.W)[0] for a in probes))
            else:
                sig = p.code
            if sig in seen:
                continue
            seen.add(sig)
            allp.append(p)
        self.pool = allp[: self.cfg["K"]]
        return dict(n_repair=len(to_repair), n_new=len(new), n_new_consistent=sum(p.acc == 1.0 for p in new))

    # ---------- action selection ----------
    def choose(self, cands, scores, cur_grid):
        if self.policy in ("disagree", "disagree_noreset"):
            best = max(s["score"] for s in scores)
            tied = [i for i, s in enumerate(scores) if s["score"] >= best - 1e-9]
            if any(not scores[i]["known"] for i in tied):  # at H = 0, prefer questions not yet answered
                tied = [i for i in tied if not scores[i]["known"]]
            mincost = min(cands[i].cost for i in tied)
            tied = [i for i in tied if cands[i].cost == mincost]
            return self.rng.choice(tied), None
        if self.policy == "random":
            kinds = sorted({c.kind for c in cands})
            k = self.rng.choice(kinds)
            return self.rng.choice([i for i, c in enumerate(cands) if c.kind == k]), None
        if self.policy == "llm":
            menu = [menu_label(c, cur_grid, self.env.init_grid) for c in cands]
            msgs = prompts.choose_messages(self.H, self.W, self.bg, self.segments, menu, self.cfg["BUDGET"] - self.used)
            text = llm.chat(msgs, n=1, temperature=self.cfg["T_ACT"], max_tokens=600,
                            seed=crc(self.env_name, self.seed, "act", self.decision))[0]
            self.llm_calls["act"] += 1
            m = re.findall(r"ACTION\W*(\d+)", text)
            if m and 0 <= int(m[-1]) < len(cands):
                return int(m[-1]), text
            self.llm_calls["act_parse_fail"] += 1
            return self.rng.randrange(len(cands)), "PARSE_FAIL: " + text
        raise ValueError(self.policy)

    # ---------- main loop ----------
    def run(self):
        t0 = time.time()
        self.synthesize_initial()
        while self.used < self.cfg["BUDGET"]:
            self.decision += 1
            cur = self.cur_grid()
            cands = [c for c in make_candidates(self.env.init_grid, cur, self.segments, self.rng)
                     if c.cost <= self.cfg["BUDGET"] - self.used and not (c.reset and self.policy.endswith("_noreset"))]
            truths = [self.env.simulate(c.actions, c.reset) for c in cands]
            preds = [[self.predict(p, c, cur) for c in cands] for p in self.pool]
            # soft version space: weight exp(-lambda * extra errors on the history relative to the best program)
            lam = self.cfg["VS_LAMBDA"]
            min_wrong = min((p.n_wrong for p in self.pool if p.ok), default=0)
            wts = [math.exp(-lam * (p.n_wrong - min_wrong)) if p.ok else 0.0 for p in self.pool]
            seen_pairs = {(t[2], t[3]) for t in self.transitions()}
            seen_prefixes = {tuple(a for a, _ in s["steps"][:k]) for s in self.segments for k in range(1, len(s["steps"]) + 1)}
            scores = []
            for ci, c in enumerate(cands):
                outs = [preds[pi][ci] for pi in range(len(self.pool))]
                valid = [o for o in outs if o is not None]
                cnt = collections.Counter(valid)
                H_unw = entropy(cnt) if len(valid) >= 2 else 0.0
                wcnt = collections.Counter()
                for o, w in zip(outs, wts):
                    if o is not None:
                        wcnt[o] += w
                H = entropy(wcnt) if len(valid) >= 2 and lam > 0 else H_unw
                known = (tuple(c.actions) in seen_prefixes) if c.reset else ((cur, c.actions[0]) in seen_pairs)
                value = 0.0 if (known and self.cfg["KNOWN_ZERO"]) else H
                unanimous = len(valid) == len(self.pool) and len(cnt) == 1
                n_correct = sum(o == truths[ci] for o in valid)
                scores.append(dict(label=c.label, kind=c.kind, cost=c.cost, H=H, H_unw=H_unw, known=known,
                                   score=value / c.cost,
                                   n_valid=len(valid), n_distinct=len(cnt), n_correct=n_correct,
                                   unanimous=unanimous, unanimous_wrong=unanimous and n_correct == 0))
            ci, reason = self.choose(cands, scores, cur)
            c = cands[ci]
            # execute
            start_n = len(self.transitions())
            if c.reset:
                g0 = self.env.reset()
                assert g0 == self.env.init_grid, "environment reset is not deterministic"
                self.segments.append({"init": g0, "steps": []})
                self.counts["reset"] += 1
            for a in c.actions:
                g = self.env.step(a)
                self.segments[-1]["steps"].append((a, g))
                self.counts["click" if a.startswith("click") else a] += 1
            self.used += c.cost
            new_idx = list(range(start_n, len(self.transitions())))
            if scores[ci]["unanimous_wrong"]:
                self.surprises.append(dict(decision=self.decision, label=c.label))
            upd = self.update_pool(new_idx)
            ho = self.heldout_eval(brief=True)
            self.log.append(dict(
                decision=self.decision, used=self.used, chosen=c.label, kind=c.kind, cost=c.cost,
                H_chosen=scores[ci]["H"], H_max=max(s["H"] for s in scores), score_max=max(s["score"] for s in scores),
                chosen_unanimous_wrong=scores[ci]["unanimous_wrong"], n_cands=len(cands),
                n_unanimous_wrong=sum(s["unanimous_wrong"] for s in scores),
                n_unanimous=sum(s["unanimous"] for s in scores),
                n_zeroH=sum(s["H"] == 0 for s in scores),
                chosen_known=scores[ci]["known"],
                cands=[{k: s[k] for k in ("label", "kind", "cost", "H", "H_unw", "known", "n_valid", "n_distinct", "n_correct",
                                          "unanimous_wrong")}
                       for s in scores],
                reason=reason, pool_acc=[round(p.acc, 3) for p in self.pool], coverage=sorted(self.env.coverage()),
                heldout_best=ho["best_by_fit"]["acc"], heldout_oracle=ho["oracle_best"]["acc"],
                llm_usage=dict(llm.USAGE), t=round(time.time() - t0, 1), **upd))
            sys.stderr.write(f"  [{self.env_name} {self.policy} s{self.seed}] d{self.decision} used={self.used} "
                             f"{c.label} H={scores[ci]['H']:.2f} fit={max(p.acc for p in self.pool):.2f} "
                             f"ho={ho['best_by_fit']['acc']:.2f} t={time.time() - t0:.0f}s\n")
        return self.finish(time.time() - t0)

    # ---------- evaluation ----------
    def heldout_eval(self, brief=False):
        trajs = self.heldout["trajectories"]
        res = []
        for p in self.pool:
            preds = []
            for tj in trajs:
                acts = [a for a, _ in tj["steps"]]
                obs = [g for _, g in tj["steps"]]
                pr, _, _ = p.run_segment(tuple(tj["init"]), acts, self.H, self.W, observed=[tuple(o) for o in obs])
                preds += pr
            res.append(preds)
        truth, before, tags = [], [], []
        for tj in trajs:
            g = tuple(tj["init"])
            for (a, g2), tg in zip(tj["steps"], tj["tags"]):
                truth.append(tuple(g2))
                before.append(g)
                tags.append(tg)
                g = tuple(g2)
        n = len(truth)
        changing = [i for i in range(n) if truth[i] != before[i]]

        def acc(preds, idx):
            return sum(preds[i] == truth[i] for i in idx) / max(1, len(idx))

        per = [dict(pid=p.pid, fit=p.acc, acc=acc(r, range(n)), acc_changing=acc(r, changing)) for p, r in zip(self.pool, res)]
        if not per:
            empty = dict(acc=0.0, acc_changing=0.0)
            return dict(best_by_fit=empty, oracle_best=empty)
        # agent-side choice: best fit to its own history, ties -> shorter code
        bi = min(range(len(self.pool)), key=lambda i: (-self.pool[i].acc, len(self.pool[i].code)))
        oi = max(range(len(per)), key=lambda i: per[i]["acc"])
        out = dict(best_by_fit=per[bi], oracle_best=per[oi])
        if brief:
            return out
        # shared-wrong-assumption analysis over held-out transitions
        cats = collections.Counter()
        per_clause = collections.defaultdict(collections.Counter)
        rows = []
        for i in range(n):
            outs = [r[i] for r in res]
            valid = [o for o in outs if o is not None]
            nc = sum(o == truth[i] for o in valid)
            if nc == len(outs):
                cat = "all_correct"
            elif nc > 0:
                cat = "some_correct"
            elif len(valid) == len(outs) and len(set(valid)) == 1:
                cat = "unanimous_wrong"
            else:
                cat = "all_wrong_disagree"
            cats[cat] += 1
            for cl in tags[i]:
                per_clause[cl][cat] += 1
            rows.append(dict(i=i, cat=cat, changing=i in changing, tags=tags[i]))
        out.update(per_program=per, categories=dict(cats), per_clause={str(k): dict(v) for k, v in per_clause.items()},
                   mean_pool_acc=sum(q["acc"] for q in per) / len(per), n_heldout=n, n_changing=len(changing),
                   identity_acc=sum(truth[i] == before[i] for i in range(n)) / n, rows=rows)
        return out

    def finish(self, secs):
        ho = self.heldout_eval(brief=False)
        prim = sum(self.counts.values())
        cov = sorted(self.env.coverage())
        result = dict(
            env=self.env_name, policy=self.policy, seed=self.seed, cfg=self.cfg,
            n_clauses=self.env.n_clauses, covered=cov, coverage=len(cov) / self.env.n_clauses,
            action_counts=dict(self.counts), n_primitive=prim,
            reset_share=self.counts["reset"] / prim, noop_share=self.counts["noop"] / prim,
            reset_noop_share=(self.counts["reset"] + self.counts["noop"]) / prim,
            n_decisions=self.decision, llm_calls=dict(self.llm_calls), llm_usage=dict(llm.USAGE),
            heldout=ho, surprises=self.surprises, seconds=round(secs, 1),
            final_pool=[dict(pid=p.pid, origin=p.origin, birth=p.birth_step, parent=p.parent, fit=p.acc,
                             err=p.err, code=p.code) for p in self.pool],
            history=[dict(init=s["init"], steps=s["steps"]) for s in self.segments],
            log=self.log,
        )
        return result
