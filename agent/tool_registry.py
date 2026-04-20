import numexpr as ne
from streamlit import exception


def calculator(expression : str)-> str:
    """
    Safely evaluates a given mathematical expression using numexpr.
    Args:
            expression (str): Math expression like :
            "2+2" "125^3" 12312*5" "128/1.65"

    Returns:
        str: Result as string or error message
    """
    try :
        expression = expression.strip()

        if not expression:
            return "Error: Empty Expression"

        result = ne.evaluate(expression)

        if hasattr(result, "item"):
            result = result.item()

            return str(result)

    except ZeroDivisionError:
        return "Error : Division by Zero  Error"

    except Exception as e :
        return f"Error :{str(e)}"