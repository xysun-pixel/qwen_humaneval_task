# Evaluation Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install pandas pytest numpy

# Copy evaluation scripts
COPY humaneval_results.json .
COPY HumanEval.json .
COPY evaluate_humaneval.py .

# Official HumanEval evaluation script
RUN git clone https://github.com/openai/human-eval.git
WORKDIR /app/human-eval
RUN pip install -e .

WORKDIR /app
CMD ["python", "evaluate_humaneval.py"]