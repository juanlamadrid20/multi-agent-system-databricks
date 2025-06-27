from agents import function_tool
from src.utils.research_client import PerplexityResearchClient

# Initialize research client
research_client = PerplexityResearchClient()


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
    return research_client.research_and_reason(user_query)