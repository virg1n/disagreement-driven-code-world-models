#!/usr/bin/env bash
# Environment used for the experiments (Linux, Python 3.12, CUDA driver >= 12.1, V100 GPUs).
# Run from the repository root.
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install -q uv
export UV_HTTP_TIMEOUT=600

# torch 2.5.1+cu121 still ships sm_70 kernels (V100); newer cu128 builds do not
uv pip install "torch==2.5.1" --index-url https://download.pytorch.org/whl/cu121
uv pip install -r requirements.txt

# Autumn.cpp Python bindings: the wheel is published on the GitHub release, not on PyPI
uv pip install "https://github.com/BasisResearch/Autumn.cpp/releases/download/v1/mara_autumn_cpp-1.0.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl"

# Autumn programs (.sexp) used as environments
mkdir -p third_party
[ -d third_party/Autumn.cpp ] || git clone --depth 1 https://github.com/BasisResearch/Autumn.cpp third_party/Autumn.cpp

python -c "from MARA.autumn_cpp import Interpreter; import vllm, torch; print('ok', vllm.__version__, torch.cuda.get_arch_list())"
