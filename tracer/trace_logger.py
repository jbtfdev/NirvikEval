import json
def save_trace(trace, path):
    with open(path, "w") as f:
        json.dump(trace.model_dump(), f, indent=2)