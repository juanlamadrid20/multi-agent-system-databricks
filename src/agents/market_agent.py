from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from src.tools.toolkit import (
    get_state_census_data,
    do_research_and_reason,
)
from src.utils.prompt_loader import load_prompt


def create_market_agent(client: AsyncOpenAI, model_name: str, enterprise_agent=None):
    """Create Market Intelligence Agent"""
    
    # Load base prompt
    market_intelligence_prompt = load_prompt('prompts/market_intelligence_agent.txt')
    
    # Create base agent
    base_agent = Agent(
        name="Market Intelligence Agent",
        handoff_description="Specialist in market research pertaining to general questions about the market, industry, news, competitors, demographics, etc.",
        instructions=market_intelligence_prompt,
        model=OpenAIChatCompletionsModel(model=model_name, openai_client=client),
        tools=[
            get_state_census_data, 
            do_research_and_reason,
        ],
    )
    
    # If enterprise agent is provided, create enhanced version with tools-for-agents pattern
    if enterprise_agent:
        enhanced_prompt = market_intelligence_prompt + """

## Additional Capabilities
You now have the Enterprise Intelligence Agent available as a tool. When a query requires store-specific information:
1. Use the get_enterprise_data tool to first obtain store location or performance information
2. Then use your demographic and market research tools to analyze that location
3. Combine both sources of information to provide a complete response

For example, if asked "Based on where store 110 is located, what are the demographics of the area?":
1. First use get_enterprise_data to find out where store 110 is located
2. Then analyze the demographics of that location using your tools
"""
        
        enhanced_agent = Agent(
            name="Market Intelligence Agent",
            handoff_description="Specialist in market research pertaining to general questions about the market, industry, news, competitors, demographics, etc.",
            instructions=enhanced_prompt,
            model=OpenAIChatCompletionsModel(model=model_name, openai_client=client),
            tools=[
                get_state_census_data, 
                do_research_and_reason,
                enterprise_agent.as_tool(
                    tool_name="get_enterprise_data",
                    tool_description="Get store location, performance data, or inventory information for specific store numbers",
                ),
            ],
        )
        return enhanced_agent
    
    return base_agent