from openai import AsyncOpenAI
from .enterprise_agent import create_enterprise_agent
from .market_agent import create_market_agent
from .triage_agent import create_triage_agent


def create_agent_system(client: AsyncOpenAI, model_name: str):
    """Create the complete multi-agent system with tools-for-agents pattern"""
    
    # Create base agents first
    base_enterprise_agent = create_enterprise_agent(client, model_name)
    base_market_agent = create_market_agent(client, model_name)
    
    # Create enhanced agents with cross-agent tools
    enhanced_enterprise_agent = create_enterprise_agent(client, model_name, base_market_agent)
    enhanced_market_agent = create_market_agent(client, model_name, base_enterprise_agent)
    
    # Create triage agent with handoffs to enhanced agents
    triage_agent = create_triage_agent(client, model_name, enhanced_enterprise_agent, enhanced_market_agent)
    
    return {
        'triage_agent': triage_agent,
        'enterprise_agent': enhanced_enterprise_agent,
        'market_agent': enhanced_market_agent,
        'base_enterprise_agent': base_enterprise_agent,
        'base_market_agent': base_market_agent
    }