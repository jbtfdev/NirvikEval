from RestrictedPython import compile_restricted
from RestrictedPython import safe_globals

def code_executor(code : str) -> str:
    try:
        code = code.strip()

        if not code:
            return " Error :  Empty Code."

        byte_code = compile_restricted(code, "<string>", "exec")

        env = safe_globals.copy()
        env["sum"] = sum
        env["range"] = range
        env["len"] = len
        env["min"] = min
        env["max"] = max
        env["abs"] = abs


        local_vars = {}

        exec(byte_code, env, local_vars)

        if "result" not in local_vars:
            return "Error : No result variable set."

        return str(local_vars["result"])

    except Exception as e:
        return f"Error : {str(e)}"