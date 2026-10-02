"""Prompt construction. The shared history block comes first so vLLM prefix caching can reuse it."""
from autumn_env import legend_for
from progexec import diff

MAX_DIFF_CELLS = 30


def fmt_grid(g):
    W = len(g[0])
    head = "     x=" + "".join(str(x % 10) for x in range(W))
    rows = [f"y={y:2d}   {row}" for y, row in enumerate(g)]
    return "\n".join([head] + rows)


def fmt_changes(g0, g1):
    ch, n = diff(g0, g1, MAX_DIFF_CELLS)
    if n == 0:
        return "no change"
    s = " ".join(f"({x},{y}):{a}>{b}" for x, y, a, b in ch)
    if n > len(ch):
        s += f" ...(+{n - len(ch)} more changed cells)"
    return s


def env_description(H, W, bg):
    return (
        f"The environment is a {W}x{H} grid (x = column 0..{W - 1} from left to right, y = row 0..{H - 1} from top to bottom). "
        f"Each cell holds a one-character color code. Color legend: {legend_for(bg)}.\n"
        "Time advances in discrete steps. At every step the player performs exactly one action:\n"
        "  'up', 'down', 'left', 'right'   (arrow keys)\n"
        "  'noop'                          (do nothing; time still advances)\n"
        "  'click X Y'                     (click the cell at column X, row Y)\n"
        "Objects may also move or change on their own at every step, even on 'noop'. "
        "The player can RESET the environment, which restores the initial grid and all hidden state."
    )


def fmt_history(segments):
    """segments: list of {'init': grid, 'steps': [(action, grid_after), ...]}; the first init is the initial grid."""
    lines = ["INITIAL GRID:", fmt_grid(segments[0]["init"])]
    n = sum(len(s["steps"]) for s in segments)
    if n == 0:
        lines.append("\nNo actions have been taken yet.")
        return "\n".join(lines)
    lines.append("\nOBSERVED TRANSITIONS (changed cells are listed as (x,y):old>new; '.' = empty):")
    k = 0
    for si, seg in enumerate(segments):
        if si > 0:
            lines.append("--- RESET: the grid returned to the INITIAL GRID ---")
        g = seg["init"]
        for a, g2 in seg["steps"]:
            k += 1
            lines.append(f"[{k}] action={a} -> {fmt_changes(g, g2)}")
            g = g2
    cur = segments[-1]["steps"][-1][1] if segments[-1]["steps"] else segments[-1]["init"]
    lines.append("\nCURRENT GRID (after the last transition):")
    lines.append(fmt_grid(cur))
    return "\n".join(lines)


SYSTEM_SYNTH = ("You are an expert at inferring the hidden rules of simple grid-world games from observations "
                "and writing them as precise, general Python code.")

STEP_SPEC = """def step(grid, action, mem):
    \"\"\"grid: list of {H} rows, each a list of {W} one-char color codes (access as grid[y][x]).
    action: 'up', 'down', 'left', 'right', 'noop', or 'click X Y' (X = column, Y = row).
    mem: dict that persists across steps and is emptied on reset. Use it for hidden state that the
         grid does not show (e.g. current mode, direction of motion, counters). It is empty on the
         first step after the initial grid.
    Returns the next grid (a new list of {H} lists of {W} one-char strings).\"\"\""""


def synth_messages(H, W, bg, segments):
    user = (
        env_description(H, W, bg) + "\n\n" + fmt_history(segments) + "\n\n"
        "TASK: write a Python world model of this environment:\n\n" + STEP_SPEC.format(H=H, W=W) + "\n\n"
        "Requirements:\n"
        "- It must reproduce every observed transition exactly (the full grid after each action).\n"
        "- Model the general rules (objects, how they move, collisions, what each key and click does, what happens "
        "every step on its own) so that it also predicts actions and situations that were not observed yet. "
        "Do not hard-code step numbers or the list of observed transitions.\n"
        "- Plain Python; you may import math, copy, itertools, collections. No printing.\n"
        "First state the rules you infer in at most 2 short sentences, then give the complete code in one ```python block. "
        "Do not copy the docstring above into your code; keep the code compact."
    )
    return [{"role": "system", "content": SYSTEM_SYNTH}, {"role": "user", "content": user}]


def fmt_mismatch(k, a, g0, pred, obs, err):
    if pred is None:
        return f"[{k}] action={a}: the program raised an error: {err}"
    return (f"[{k}] action={a}\n    your prediction: {fmt_changes(g0, pred)}\n"
            f"    actually observed: {fmt_changes(g0, obs)}")


def repair_messages(H, W, bg, segments, code, mismatches, n_correct, n_total):
    user = (
        env_description(H, W, bg) + "\n\n" + fmt_history(segments) + "\n\n"
        "TASK: below is a candidate Python world model of this environment with the interface\n\n"
        + STEP_SPEC.format(H=H, W=W) + "\n\n"
        f"```python\n{code}\n```\n\n"
        f"It reproduces {n_correct} of the {n_total} observed transitions. Some mismatches "
        "(changes are relative to the grid before the action):\n" + "\n".join(mismatches) + "\n\n"
        "Fix the program so that it reproduces ALL observed transitions while still modelling general rules "
        "(no hard-coded step numbers). Explain the fix in at most 2 short sentences, then give the complete corrected "
        "code in one ```python block. Do not copy the docstring above into your code; keep the code compact."
    )
    return [{"role": "system", "content": SYSTEM_SYNTH}, {"role": "user", "content": user}]


SYSTEM_ACT = ("You are an agent exploring an unknown grid-world environment in order to learn exactly how it works. "
              "Afterwards you will be tested on predicting what happens after arbitrary actions in arbitrary situations.")


def choose_messages(H, W, bg, segments, menu, remaining):
    opts = "\n".join(f"  {i}: {m}" for i, m in enumerate(menu))
    user = (
        env_description(H, W, bg) + "\n\n" + fmt_history(segments) + "\n\n"
        f"You have {remaining} actions left in your exploration budget (a RESET costs 1 action). "
        "Choose your next action from this menu:\n" + opts + "\n\n"
        "Pick the action whose outcome will teach you the most about the rules you are still uncertain about. "
        "Reply with one or two short sentences of reasoning, then a final line of the form 'ACTION: <number>'."
    )
    return [{"role": "system", "content": SYSTEM_ACT}, {"role": "user", "content": user}]
