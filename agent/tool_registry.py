
from tools.calculator import calculator
from tools.web_search import web_search
from tools.wiki_lookup import wiki_lookup
from tools.code_executor import code_executor
from tools.date_utils import date_utils


TOOLS = {
    "calculator" : calculator,
    "web_search" : web_search,
    "wiki_lookup" : wiki_lookup,
    "code_executor" : code_executor,
    "date_utils" : date_utils
}

def dispatch_tool(name: str, input_text : str) -> str:
    """
        Route tool name to actual function.

        Args:
            name (str): Tool name from agent
            input_text (str): Input for tool

        Returns:
            str: Tool output
        """
    try:
        name = name.strip().lower()

        tool_func = TOOLS.get(name)

        if tool_func is None:
            return f"Error: Unkown tool '{name}'."

        result = tool_func(input_text)

        return str(result)

    except Exception as e:
        return f"Error : {str(e)}"

# Quick local tests
if __name__ == "__main__":
    tests = [
        ("calculator", "2+2"),
        ("date_utils", "today"),
        ("wiki_lookup", "India"),
        ("web_search", "capital of japan"),
        ("code_executor", "result = 5*5"),
        ("unknown_tool", "hello")
    ]

    for tool_name, tool_input in tests:
        print(f"\n--- {tool_name} ---")
        print(dispatch_tool(tool_name, tool_input))