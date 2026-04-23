import subprocess
import re
import time
import uuid

from agent.tool_registry import dispatch_tool
from tracer.trace_schema import ToolCall, AgentTrace
from tracer.trace_logger import  save_trace

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
    trace_steps = []
    final_answer = None
    timed_out = True


    for step in range(max_steps):
        response = ollama_call(system_prompt, messages)

        thought, action, action_input = parse_response(response)

        if action == "Final Answer":
            final_answer = action_input
            timed_out = False
            break

        start = time.time()
        observation = dispatch_tool(action, action_input)
        latency_ms = (time.time() - start) * 1000

        tool_call = ToolCall(
            step = step + 1,
            thought = thought,
            tool_name = action,
            tool_input = action_input,
            tool_output = str(observation),
            latency_ms = round(latency_ms, 2)
        )
        trace_steps.append(tool_call)


        messages.append({"role" : "assistant", "content" : response})
        messages.append({"role" : "user", "content" : f"Observation: {observation}"})
        # print(f"\nSTEP {step + 1}")
        # print("RAW RESPONSE:", repr(response))

    total_latency = sum(step.latency_ms for step in trace_steps)

    trace = AgentTrace(
        trace_id = str(uuid.uuid4()),
        task_id = "manual_test",
        task = task,
        steps = trace_steps,
        final_answer = final_answer,
        expected_answer = None,
        passed = False,
        total_steps = len(trace_steps),
        total_latency_ms = round(total_latency, 2),
        timed_out = timed_out
        )

    return trace





if __name__ == "__main__":
    trace = run_agent("What is 25 * 8 + 13?")

    save_trace(trace, "../results/manual_test_1.json")

    print("Trace saved successfully.")
    print("Final Answer:", trace.final_answer)