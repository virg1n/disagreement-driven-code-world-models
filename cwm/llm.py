"""Minimal client for the vLLM OpenAI-compatible server (Qwen2.5-Coder-7B-Instruct)."""
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests

URL = os.environ.get("VLLM_URL", "http://127.0.0.1:18731/v1/chat/completions")
MODEL = os.environ.get("VLLM_MODEL", "qwen-coder-7b")

_lock = threading.Lock()
USAGE = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0, "seconds": 0.0}


def chat(messages, n=1, temperature=0.8, top_p=0.95, max_tokens=1400, seed=None):
    payload = {"model": MODEL, "messages": messages, "n": n, "temperature": temperature,
               "top_p": top_p, "max_tokens": max_tokens}
    # vLLM 0.6.6 returns n identical samples when a per-request seed is set, so only seed n=1 calls
    if seed is not None and n == 1:
        payload["seed"] = int(seed) % (2**31)
    t0 = time.time()
    last = None
    for attempt in range(6):
        try:
            r = requests.post(URL, json=payload, timeout=900)
            r.raise_for_status()
            j = r.json()
            u = j.get("usage", {})
            with _lock:
                USAGE["calls"] += 1
                USAGE["prompt_tokens"] += u.get("prompt_tokens", 0)
                USAGE["completion_tokens"] += u.get("completion_tokens", 0)
                USAGE["seconds"] += time.time() - t0
            return [c["message"]["content"] or "" for c in j["choices"]]
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"LLM call failed after retries: {last}")


_pool = None


def chat_many(jobs):
    """jobs: list of kwargs dicts for chat(); returns list of results (list of strings each) in order."""
    global _pool
    if _pool is None:  # created lazily so forked worker processes get their own threads
        _pool = ThreadPoolExecutor(max_workers=8)
    futs = [_pool.submit(chat, **j) for j in jobs]
    return [f.result() for f in futs]
