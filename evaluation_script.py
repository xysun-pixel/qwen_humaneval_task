# evaluate_humaneval.py
from human_eval.data import write_jsonl, read_problems
from human_eval.evaluation import evaluate_functional_correctness
import json

def load_results():
    with open("humaneval_results.json", "r") as f:
        return json.load(f)

def prepare_for_evaluation(results):
    return [{
        "task_id": res["task_id"],
        "completion": res["full_code"]
    } for res in results if "full_code" in res]

def main():
    results = load_results()
    samples = prepare_for_evaluation(results)
    
    # Write to jsonl format expected by HumanEval
    write_jsonl("samples.jsonl", samples)
    
    # Run evaluation
    score = evaluate_functional_correctness(
        "samples.jsonl",
        problem_file="HumanEval.json",
        k=[1],
        n_workers=4,
        timeout=3.0
    )
    
    print(f"Pass@1 score: {score}")

if __name__ == "__main__":
    main()