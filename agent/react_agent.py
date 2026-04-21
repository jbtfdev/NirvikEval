import subprocess
import re
from agent.tool_registry import dispatch_tool


def ollama_call(system_prompt : str, messages : list[dict]) -> str:
    prompt = system_prompt + "\n\n"


    for m in messages:
        role = m["role"].upper()
        prompt += f"{role} : {m['content']}\n"

    process = subprocess.run(
            ["ollama", "run", "llama3.1:8b"],
            input = prompt,
            text = True,
            capture_output= True
        )

    return process.stdout.strip()

def parse_response(text: str):
    thought_match = re.search(
        r"thought:\s*(.*?)\s*(Action:|Final Answer:)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    action_match = re.search(
        r"action:\s*(.*?)\s*Action input:",
        text,
        re.IGNORECASE | re.DOTALL
    )

    input_match = re.search(
        r"action input:\s*(.*?)\s*(Observation:|Final Answer:|$)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    final_match = re.search(
        r"final answer:\s*(.*)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    thought = thought_match.group(1).strip() if thought_match else ""

    if final_match:
        return thought, "Final Answer", final_match.group(1).strip()

    action = action_match.group(1).strip() if action_match else "Final Answer"
    action_input = input_match.group(1).strip() if input_match else ""
    action_input = action_input.strip().strip('"').strip("'")
    # print("PARSED:", thought, action, action_input)

    return thought, action, action_input



def run_agent(task: str, max_steps: int = 10):
    system_prompt = """
    You are a ReAct agent.

    You MUST use exactly one format.

    Format 1:
    Thought: reasoning
    Action: tool_name
    Action Input: tool input

    Format 2:
    Thought: reasoning
    Final Answer: answer

    Available tools:
    - calculator(expression): Input must be only raw math expression. Example: 6 * 7
    - web_search(query): Input must be only search query.
    - wiki_lookup(topic): Input must be only topic name.
    - code_executor(code): Input must be only Python code. Must store answer in result variable.
    - date_utils(query): Input must be direct date query.

    IMPORTANT:
    After receiving an Observation from a tool, if it answers the question, respond with Final Answer.
    IMPORTANT:
    If Observation contains the answer, immediately respond with:
    
    Thought: I now know the answer.
    Final Answer: <answer>

    Do not call another tool after a successful observation.

    Do not repeat the same tool call if the answer is already known.
    Do not speak normally.
    """
    messages = [{"role": "user", "content" : task}]

    for step in range(max_steps):
        response = ollama_call(system_prompt, messages)

        thought, action, action_input = parse_response(response)

        if action =="Final Answer":
            return action_input

        observation = dispatch_tool(action, action_input)

        messages.append({"role" : "assistant", "content" : response})
        messages.append({"role" : "user", "content" : f"Observation : {observation}"})
        # print(f"\nSTEP {step + 1}")
        # print("RAW RESPONSE:", repr(response))

    return "Max Steps Reached"




if __name__ == "__main__":
    tests = [
        "What is 25 * 8 + 13?",
        "Tell me about Alan Turing.",
        "What is the capital of Japan?",
        "How many days since 2024-01-01?",
        "Use Python code to find the sum of squares from 1 to 5."
    ]

    for i, task in enumerate(tests, start=1):
        print(f"\n========== TEST {i} ==========")
        print("TASK:", task)

        result = run_agent(task)

        print("RESULT:", repr(result))