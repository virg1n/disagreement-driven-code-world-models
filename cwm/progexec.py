"""Sandboxed execution of LLM-written world-model programs `step(grid, action, mem) -> grid`.

Programs run in-process with restricted builtins, an import whitelist and a SIGALRM time limit
(so this must run in a process's main thread).
"""
import builtins
import collections
import copy
import itertools
import math
import re
import signal
from contextlib import contextmanager

_ALLOWED_MODULES = {"math", "copy", "itertools", "collections", "functools", "operator", "typing"}


def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name.split(".")[0] in _ALLOWED_MODULES:
        return __import__(name, globals, locals, fromlist, level)
    raise ImportError(f"import of {name} not allowed")


_SAFE_NAMES = """abs all any bool dict enumerate filter float int isinstance issubclass len list map max min
range reversed set sorted str sum tuple zip frozenset round divmod hash iter next object super property
staticmethod classmethod type slice getattr setattr hasattr callable chr ord format repr pow id
Exception ValueError IndexError KeyError TypeError RuntimeError ZeroDivisionError AttributeError
StopIteration NotImplementedError AssertionError ArithmeticError LookupError NameError True False None""".split()
SAFE_BUILTINS = {k: getattr(builtins, k) for k in _SAFE_NAMES}
SAFE_BUILTINS["__import__"] = _safe_import
SAFE_BUILTINS["__build_class__"] = builtins.__build_class__
SAFE_BUILTINS["print"] = lambda *a, **k: None


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


signal.signal(signal.SIGALRM, _alarm)


@contextmanager
def time_limit(sec):
    signal.setitimer(signal.ITIMER_REAL, sec)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def extract_code(text):
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, re.S)
    if not blocks:
        # unterminated block (hit max_tokens) or bare code
        m = re.search(r"```(?:python|py)?\s*\n(.*)", text, re.S)
        blocks = [m.group(1)] if m else [text]
    with_step = [b for b in blocks if "def step" in b]
    return (with_step or blocks)[-1].strip()


def normalize(out, H, W):
    if not isinstance(out, (list, tuple)) or len(out) != H:
        return None
    rows = []
    for r in out:
        if isinstance(r, str):
            s = r
        elif isinstance(r, (list, tuple)) and all(isinstance(c, str) and len(c) == 1 for c in r):
            s = "".join(r)
        else:
            return None
        if len(s) != W:
            return None
        rows.append(s)
    return tuple(rows)


class Program:
    _next_id = 0

    def __init__(self, code, origin, birth_step, parent=None):
        Program._next_id += 1
        self.pid = Program._next_id
        self.code = code
        self.origin = origin  # 'init' | 'fresh' | 'repair'
        self.birth_step = birth_step
        self.parent = parent
        self.fn = None
        self.err = None
        ns = {"__builtins__": SAFE_BUILTINS, "__name__": "prog"}
        try:
            with time_limit(1.0):
                exec(compile(code, "<prog>", "exec"), ns)
            fn = ns.get("step")
            if callable(fn):
                self.fn = fn
            else:
                self.err = "no step() function defined"
        except BaseException as e:  # noqa: BLE001 - LLM code can raise anything, incl. SystemExit
            if isinstance(e, KeyboardInterrupt):
                raise
            self.err = f"{type(e).__name__}: {e}"[:300]
        # filled by evaluation
        self.hist_correct = []
        self.last_errors = {}

    @property
    def ok(self):
        return self.fn is not None

    def call(self, grid, action, mem, H, W, timeout=0.1):
        """Returns (next_grid_tuple | None, error_str | None). `mem` is mutated in place."""
        if self.fn is None:
            return None, self.err
        try:
            with time_limit(timeout):
                out = self.fn([list(r) for r in grid], action, mem)
        except BaseException as e:  # noqa: BLE001
            if isinstance(e, KeyboardInterrupt):
                raise
            return None, f"{type(e).__name__}: {e}"[:200]
        g = normalize(out, H, W)
        if g is None:
            return None, "returned value is not a HxW grid of 1-char strings"
        return g, None

    def run_segment(self, init, actions, H, W, observed=None):
        """Teacher-forced if `observed` (list of grids) is given, open-loop otherwise.
        Returns (predictions, errors, final_mem)."""
        mem = {}
        g = init
        preds, errs = [], []
        for i, a in enumerate(actions):
            p, e = self.call(g, a, mem, H, W)
            preds.append(p)
            errs.append(e)
            if observed is not None:
                g = observed[i]
            else:
                if p is None:
                    # cannot continue an open-loop rollout
                    preds.extend([None] * (len(actions) - i - 1))
                    errs.extend([e] * (len(actions) - i - 1))
                    break
                g = p
        return preds, errs, mem


def safe_deepcopy(mem):
    try:
        return copy.deepcopy(mem)
    except Exception:  # noqa: BLE001
        return dict(mem)


def diff(g0, g1, limit=None):
    ch = [(x, y, g0[y][x], g1[y][x]) for y in range(len(g0)) for x in range(len(g0[0])) if g0[y][x] != g1[y][x]]
    return ch if limit is None else ch[:limit], len(ch)


# keep stdlib modules referenced so linters don't strip imports used by programs
_ = (collections, itertools, math)
