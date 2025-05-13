# qwen_humaneval_task

（一、四）模型部署与性能优化：使用 vLLM 部署 Qwen2.5-Coder-0.5B-Instruct
相关文件：
docker-compose.yaml
定义了服务 vllm-server，会从当前目录构建镜像，映射端口 8000:8000，支持 GPU，并设置 HuggingFace 的 token。

optimized.sh
使用 vllm.entrypoints.openai.api_server 启动模型服务器，优化参数：指定模型，调参、并行设置、推理配置、量化方式（awq），以及监听端口等。

optimized_start.sh
一键调用 docker-compose up，用于启动服务（包含上面 docker-compose.yaml 中的部署逻辑）。

bulid_and_run.sh
脚本化构建镜像并运行容器，和 optimized_start.sh 类似。


（二）模型推理：运行 HumanEval 数据集生成答案
相关文件：
eval_humaneval.py
从本地读取 HumanEval.json，构造 prompt，通过 POST 请求调用 vLLM 模型 API（localhost:8000/v1/completions），生成答案。
输出写入 humaneval_results.jsonl_results.jsonl。

run.sh
只是运行上面的脚本：python eval_humaneval.py。


（三）结果评估：计算 pass@1 分数
pass@1 = 0.0122

