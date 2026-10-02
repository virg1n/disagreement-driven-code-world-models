"""Thin wrapper around the Autumn.cpp Python bindings (MARA.autumn_cpp).

Grids are rendered as tuples of strings (one char per cell, grid[y][x]); '.' is empty background.
Resets create a fresh interpreter, so on-clause coverage is accumulated across interpreters.
"""
import json
import os

from MARA.autumn_cpp import Interpreter, autumnstdlib

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Autumn programs (.sexp); clone https://github.com/BasisResearch/Autumn.cpp into third_party/ or set AUTUMN_ENV_DIR
ENV_DIR = os.environ.get("AUTUMN_ENV_DIR", os.path.join(_ROOT, "third_party", "Autumn.cpp", "tests"))

COLOR2CH = {
    "black": "k", "white": "w", "red": "r", "blue": "b", "green": "g", "gold": "o",
    "yellow": "y", "gray": "a", "darkgreen": "d", "lightblue": "l", "skyblue": "s",
    "tan": "t", "pink": "p", "orange": "n", "purple": "u", "mediumpurple": "m",
    "sandybrown": "x", "brown": "z", "darkorange": "q",
}
BG = "."
MOVES = ("up", "down", "left", "right")
_silenced = False


def silence_cpp_stdout():
    """The interpreter prints 'On condition: ...' to fd 2 on every step. Send fd 2 to /dev/null and keep
    Python's sys.stderr on a duplicate of the original stderr."""
    import sys
    global _silenced
    if _silenced:  # already done (e.g. inherited through fork)
        return
    _silenced = True
    saved = os.dup(2)
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 2)
    sys.stderr = os.fdopen(saved, "w", buffering=1)


def apply_action(it, a):
    if a == "noop":
        pass
    elif a.startswith("click"):
        _, x, y = a.split()
        it.click(int(x), int(y))
    elif a in MOVES:
        getattr(it, a)()
    else:
        raise ValueError(f"bad action {a!r}")
    it.step()


def render(it):
    d = json.loads(it.render_all())
    gs = d.pop("GRID_SIZE")
    W, H = (gs, gs) if isinstance(gs, int) else (gs[0], gs[1])
    grid = [[BG] * W for _ in range(H)]
    for cells in d.values():
        for c in cells:
            x, y = c["position"]["x"], c["position"]["y"]
            if 0 <= x < W and 0 <= y < H:
                grid[y][x] = COLOR2CH.get(c["color"], "?")
    return tuple("".join(r) for r in grid)


class AutumnEnv:
    def __init__(self, name, seed=0):
        self.name = name
        with open(os.path.join(ENV_DIR, name + ".sexp")) as f:
            self.src = f.read()
        self.seed = seed
        self.covered = set()
        self.it = None
        self.segment_actions = []  # actions since last reset
        self.init_grid = self.reset()
        self.H, self.W = len(self.init_grid), len(self.init_grid[0])

    def _new(self):
        it = Interpreter()
        it.set_verbose(False)
        r = it.run_script(self.src, autumnstdlib, "", self.seed)
        assert "successfully" in r, r
        return it

    def reset(self):
        if self.it is not None:
            self.covered |= set(self.it.get_covered_on_clause_indices())
        self.it = self._new()
        self.n_clauses = self.it.get_on_clause_count()
        self.segment_actions = []
        return render(self.it)

    def step(self, a):
        apply_action(self.it, a)
        self.segment_actions.append(a)
        return render(self.it)

    def coverage(self):
        return self.covered | set(self.it.get_covered_on_clause_indices())

    def background(self):
        return self.it.get_background()

    def simulate(self, actions, from_reset):
        """Ground-truth outcome of `actions` from the current state (or from a reset) without touching self.it."""
        it = self._new()
        if not from_reset:
            for a in self.segment_actions:
                apply_action(it, a)
                it.render_all()  # rendering has side effects in Autumn.cpp: the live env renders after every step
        outs = []
        for a in actions:
            apply_action(it, a)
            outs.append(render(it))
        return tuple(outs)


def legend_for(env_bg):
    inv = {v: k for k, v in COLOR2CH.items()}
    items = [f"'{BG}'=empty ({env_bg} background)"] + [f"'{c}'={inv[c]}" for c in sorted(inv)]
    return ", ".join(items)
