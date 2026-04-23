from datetime import datetime


def date_utils(query: str) ->str:
    """
    Simple Date utility tool

    supported queries:
    -today
    -days since YYYY-MM-DD
    -days until YYYY-MM-DD
    """

    try:
        query = query.strip().lower()

        if not query:
            return "Error : Empty Query"

        today = datetime.now().date()

        if query == "today" or "today's date" or "what is the current date?":
            return str(today)

        elif query.startswith("days since"):
            date_str = query.replace("days since", "").strip()
            past_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            diff = (today - past_date).days
            return f"{diff} days"

        elif query.startswith("days until"):
            date_str = query.replace("days until", "").strip()
            future_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            diff = (future_date - today).days

            return f"{diff} days"

        else :
            return "Error : Unsupported query"

    except ValueError:
        return "Error : Invalid date format. Use YYYY-MM-DD."

    except Exception as e:
        return f"Error : {str(e)}"


# Quick local test
if __name__ == "__main__":
    tests = [
        "today",
        "days since 2024-01-01",
        "days until 2027-01-01",
        "days since banana",
        "",
        "hello"
    ]

    for t in tests:
        print(f"{t} -> {date_utils(t)}")