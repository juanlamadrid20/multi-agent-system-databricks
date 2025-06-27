import os
import time
from agents import function_tool
from openai import OpenAI


@function_tool
def do_research_and_reason(user_query: str):
    """
    Get a response from sythesized intelligence from the web including the "thinking" process highligted in the <think></think> tags

    Args:
        user_query: The user's question or request
    Returns:
        The sythesized intelligence from the web including the "thinking"
        process inside <think></think> tags
    """
    print("INFO: `do_research_and_reason` tool called")
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": f"today is {time.strftime('%d %B %Y')} + " + user_query,
        },
    ]

    client = OpenAI(
        api_key=os.getenv("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai"
    )

    # chat completion with streaming
    response_stream = client.chat.completions.create(
        model="sonar-reasoning-pro",  # o3 comp
        messages=messages,
        stream=True,
    )

    full_response = ""
    for response in response_stream:
        if response.choices and response.choices[0].delta.content:
            content = response.choices[0].delta.content
            full_response += content

    return full_response