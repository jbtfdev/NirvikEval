def normalize(text):
    return text.strip().lower()

def exact_match(expected, actual):
    return normalize(expected) == normalize(actual)

def contains_match(expected, actual):
    return normalize(expected) in normalize(actual)

def numeric_match(expected, actual, tolerance=0.0):
    try:
        e = float(expected)
        a = float(actual)
        return abs(e-a) <= tolerance
    except:
        return False

def score_task(task, agent_answer):
    scoring_type = task["scoring_type"]
    expected = task["expected_answer"]
    tolerance = task["tolerance"]

    if agent_answer is None:
        return False

    if scoring_type == "exact_match":
        return exact_match(expected, agent_answer)

    elif scoring_type == "contains_match":
        return contains_match(expected, agent_answer)

    elif scoring_type == "numeric_match":
        return numeric_match(expected, agent_answer, tolerance or 0.0)

    return False