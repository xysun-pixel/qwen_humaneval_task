python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-Coder-0.5B-Instruct \
    --trust-remote-code \
    --tensor-parallel-size 2 \
    --enforce-eager \
    --max-num-seqs 256 \
    --max-model-len 2048 \
    --quantization awq \
    --host 0.0.0.0 \
    --port 8000

# Optimization For vLLM Serving:
# Enable continuous batching: Add --enforce-eager 
# Tensor parallelism: Change --tensor-parallel-size 
# Quantization: Serve the model with AWQ 
# Optimize parameters: Adjust --max-num-seqs and --max-model-len 