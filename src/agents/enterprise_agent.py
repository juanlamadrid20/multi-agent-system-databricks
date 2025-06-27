from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from src.tools.toolkit import (
    get_business_conduct_policy_info,
    get_store_performance_info,
    get_product_inventory_info,
)
from src.utils.prompt_loader import load_prompt


def create_enterprise_agent(client: AsyncOpenAI, model_name: str, market_agent=None):
    """Create Enterprise Intelligence Agent"""
    
    # Load base prompt
    enterprise_intelligence_prompt = load_prompt('prompts/enterprise_intelligence_agent.txt')
    
    # Create base agent
    base_agent = Agent(
        name="Enterprise Intelligence Agent",
        handoff_description="Specialist in enterprise analytics pertaining to the store performance, sales, store location, returns, BOPIS(buy online pick up in store), policy, inventory etc.",
        instructions=enterprise_intelligence_prompt,
        model=OpenAIChatCompletionsModel(model=model_name, openai_client=client),
        tools=[
            get_business_conduct_policy_info,
            get_store_performance_info,
            get_product_inventory_info,
        ],
    )
    
    # If market agent is provided, create enhanced version with tools-for-agents pattern
    if market_agent:
        enhanced_prompt = enterprise_intelligence_prompt + """

## Additional Capabilities
You now have the Market Intelligence Agent available as a tool. When a query requires demographic or market research data:
1. First determine the relevant location information using your store performance tools
2. Then use the get_market_intelligence tool to obtain demographic information for that location
3. Combine both sources of information to provide a complete response
"""
        
        enhanced_agent = Agent(
            name="Enterprise Intelligence Agent",
            handoff_description="Specialist in enterprise analytics pertaining to the store performance, sales, store location, returns, BOPIS(buy online pick up in store), policy, inventory etc.",
            instructions=enhanced_prompt,
            model=OpenAIChatCompletionsModel(model=model_name, openai_client=client),
            tools=[
                get_business_conduct_policy_info,
                get_store_performance_info,
                get_product_inventory_info,
                market_agent.as_tool(
                    tool_name="get_market_intelligence",
                    tool_description="Get demographic and market research information for a specific location or area",
                ),
            ],
        )
        return enhanced_agent
    
    return base_agent