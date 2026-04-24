import json
from datetime import datetime

from agent.react_agent import run_agent
from eval.scorer import score_task

with open("eval/task_suite.json", "r") as f:
    task = json.load(f)

results = []

for task in task[:5]:
    print(f"Running :{task['id']}")

    trace = run_agent(task['task'])
    passed = score_task(task, trace.final_answer)

    trace_dict = trace.model_dump()
    trace_dict["passed"] = passed
    trace_dict["expected_answer"] = task["expected_answer"]
    trace_dict["category"] = task["category"]
    trace_dict["ideal_tools"] = task["ideal_tools"]

    results.append(trace_dict)

# Saving the results
date_str = datetime.now().strftime("%Y%m%d")
filename = f"results/eval_run_{date_str}.json"

with open(filename, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved results to {filename}")