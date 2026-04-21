import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="NirvikEval/1.0 (Educational project)"
)

def wiki_lookup(topic : str) -> str:
    """
    Fetch a short wikipedia summary for a topic,

    Args:
        topic (str) : Example:
        "Machine Learning"
        "India"
        "Alan turing"

    Returns:
        str: Summary or text or error message

    """

    try:
       topic = topic.strip()

       if not topic:
           return "Error : Empty Topic"

       page = wiki.page(topic)

       if not page.exists():
           return "No article Found"

       summary = page.summary.strip()

       if not summary:
           return "No summary available."

       return summary[:1000]

    except Exception as e:
        return f"Error: {str(e)}"

