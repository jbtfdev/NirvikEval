import subprocess
import re


def ollama_call(system_prompt : str, messages : list[dict]) -> str:
    prompt = system_prompt + "\n\n"


    for m in messages:
        role = m["role"].upper()
        prompt += f"{role} : {m["content"]}\n"

    result = subprocess.run(
            ["ollama", "run", "llama3.1:8b"],
            input = prompt,
            text = True,
            capture_output= True
        )

    return result.stdout.strip()

def parse_response(text: str):
    thought_match = re.search(r"thought:\s*(.*?)\s*Action:", text, re.IGNORECASE | re.DOTALL)
    action_match = re.search(r"action:\s*(.*?)\s*Action input:", text, re.IGNORECASE | re.DOTALL)
    input_match = re.search(r"action input:\s*(.*?)\s*Final Answer:", text, re.IGNORECASE | re.DOTALL)
    final_match = re.search(r"final answer:\s*(.*)", text, re.IGNORECASE | re.DOTALL)

    thought = thought_match.group(1).strip() if thought_match else ""

    if final_match:
        return thought, "Final Answer", final_match.group(1).strip()

    action = action_match.group(1).strip() if action_match else "Final Answer"
    action_input = input_match.group(1).strip() if input_match else ""

    return thought, action, action_input

def dispatch_tool(name: str, input: str )-> str:
    return "42"

def run_agent(task: str, max_steps: int = 6):
    system_prompt = """You are an agent.
Use format:

Thought: ...
Action: ...
Action Input: ...

OR

Thought: ...
Final Answer: ...
"""
    messages = [{"role": "user", "content" : task}]

    for step in range(max_steps):
        response = ollama_call(system_prompt, messages)

        thought, action, action_input = parse_response(response)

        if action =="Final Answer":
            return action_input

        observation = dispatch_tool(action, action_input)

        messages.append({"role" : "assistant", "content" : response})
        messages.append({"role" : "user", "content" : f"Observation :{observation}"})

    return "Max Steps Reached"


if __name__ == "__main__":
    result = run_agent("what is 6 * 7?")
    print(result)