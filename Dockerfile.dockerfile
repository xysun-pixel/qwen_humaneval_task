# vLLM serving Dockerfile for Qwen2.5-Coder-0.5B-Instruct
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install vLLM with CUDA 12.1 support
RUN pip3 install --no-cache-dir \
    vllm \
    fastapi \
    uvicorn \
    requests \
    openai \
    pandas \
    tqdm

# Create working directory
WORKDIR /app
COPY . .

# Expose the API port
EXPOSE 8000

# Command to run the server
CMD ["python3", "-m", "vllm.entrypoints.openai.api_server", \
     "--model", "Qwen/Qwen2.5-Coder-0.5B-Instruct", \
     "--trust-remote-code", \
     "--host", "0.0.0.0", \
     "--port", "8000"]