
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

        if "(" in name:
            name = name.split("(")[0].strip()

        tool_func = TOOLS.get(name)
        cleaned = input_text.strip()

        if tool_func is None:
            return f"Error: Unknown tool '{name}'."

        prefixes = ["topic =", "query =", "expression =", "code =", "input ="]

        for prefix in prefixes:
            if cleaned.lower().startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()

        cleaned = cleaned.strip('"').strip("'").strip("`").strip()
        cleaned = cleaned.split("\n")[0].strip()

        result = tool_func(cleaned)

        return str(result)

    except Exception as e:
        return f"Error : {str(e)}"

