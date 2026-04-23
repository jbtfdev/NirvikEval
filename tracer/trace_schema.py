from pydantic import BaseModel
from typing import Optional
from uuid import uuid4


class ToolCall(BaseModel):
    step: int
    thought: str
    tool_name: str
    tool_input: str
    tool_output: str
    latency_ms: float

class AgentTrace(BaseModel):
    trace_id : str
    task_id : str
    task: str
    steps: list[ToolCall]
    final_answer : Optional[str]
    expected_answer : Optional[str]
    passed : bool
    total_steps : int
    total_latency_ms : float
    timed_out : bool