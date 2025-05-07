# eval_humaneval.py
import os
import json
import requests
from tqdm import tqdm
from typing import List, Dict

# Configuration
MODEL_API = "http://localhost:8000/v1"
MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
TEMPERATURE = 0.2
MAX_TOKENS = 512

def load_humaneval(path: str = "HumanEval.json") -> List[Dict]:
    """Load HumanEval dataset"""
    with open(path, "r") as f:
        return json.load(f)

def generate_prompt(task: Dict) -> str:
    """Create prompt from HumanEval task"""
    prompt = f"""You are an expert Python programmer. Complete the following function:

```python
{task['prompt']}
```"""
    return prompt

def query_model(prompt: str) -> str:
    """Query the vLLM API for completion"""
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stop": ["\n```", "\nclass", "\ndef", "\n#", "\nif"]
    }
    
    response = requests.post(
        f"{MODEL_API}/completions",
        headers=headers,
        json=data
    )
    response.raise_for_status()
    return response.json()["choices"][0]["text"]

def evaluate_humaneval():
    """Run evaluation on HumanEval dataset"""
    dataset = load_humaneval()
    results = []
    
    for task in tqdm(dataset, desc="Evaluating"):
        try:
            prompt = generate_prompt(task)
            completion = query_model(prompt)
            
            # Combine prompt and completion
            full_code = task["prompt"] + completion
            
            results.append({
                "task_id": task["task_id"],
                "prompt": prompt,
                "completion": completion,
                "full_code": full_code,
                "canonical_solution": task["canonical_solution"],
                "test": task["test"]
            })
        except Exception as e:
            print(f"Error on task {task['task_id']}: {str(e)}")
            results.append({
                "task_id": task["task_id"],
                "error": str(e)
            })
    
    # Save results
    with open("humaneval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Evaluation complete. Results saved to humaneval_results.json")

if __name__ == "__main__":
    evaluate_humaneval()