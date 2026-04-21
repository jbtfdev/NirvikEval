from ddgs import DDGS


def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo.

    Args:
        query (str) : Search query

    Reuturns:
        str : top results or error message
    """

    try:
        query = query.strip()

        if not query:
            return "Error: Empty query."

        result_text = []

        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)

            for i, result in enumerate(results, start=1):
                title = result.get("title", "No title")
                body = result.get("body", "No snippet")

                result_text.append(
                    f"{i}. {title}\n{body}"
                )

        if not result_text:
            return "No result Found."

        return "\n\n".join(result_text)

    except Exception as e:
        return f"Error : {str(e)}"

