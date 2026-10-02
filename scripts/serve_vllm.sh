#!/usr/bin/env bash
# Start an OpenAI-compatible vLLM server.
#   scripts/serve_vllm.sh MODEL SERVED_NAME GPUS PORT [extra vllm args]
# Examples:
#   scripts/serve_vllm.sh Qwen/Qwen2.5-Coder-7B-Instruct qwen-coder-7b 0 18731
#   scripts/serve_vllm.sh Qwen/Qwen2.5-Coder-32B-Instruct-GPTQ-Int4 qwen-coder-32b 0,1 18733 \
#       --quantization gptq --tensor-parallel-size 2 --max-num-seqs 64
# Then point the agents at it:
#   export VLLM_URL=http://127.0.0.1:PORT/v1/chat/completions VLLM_MODEL=SERVED_NAME
#
# V100 notes (vLLM 0.6.6):
#  - no --enable-prefix-caching: its Triton prefill kernel asserts on Volta
#  - AWQ is refused on compute capability 7.0; GPTQ works
#  - seeded sampling builds a Triton kernel that needs Python.h; if the system has no python3-dev,
#    install a standalone Python (e.g. `uv python install 3.12`) and point C_INCLUDE_PATH at its include dir
set -euo pipefail
MODEL=$1; NAME=$2; GPUS=$3; PORT=$4; shift 4
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES=$GPUS
export VLLM_WORKER_MULTIPROC_METHOD=spawn
exec python -m vllm.entrypoints.openai.api_server --model "$MODEL" --served-model-name "$NAME" \
  --dtype half --max-model-len 16384 --gpu-memory-utilization 0.92 \
  --host 127.0.0.1 --port "$PORT" --max-num-seqs 128 --disable-log-requests --seed 0 "$@"
