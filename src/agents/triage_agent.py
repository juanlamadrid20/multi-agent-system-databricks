from agents import Agent, OpenAIChatCompletionsModel, handoff
from openai import AsyncOpenAI
import streamlit as st
from src.utils.prompt_loader import load_prompt


def on_enterprise_intelligence_handoff(ctx):
    """Callback for enterprise intelligence handoff"""
    st.sidebar.success("🔄 Handing off to Enterprise Intelligence Agent")


def on_market_intelligence_handoff(ctx):
    """Callback for market intelligence handoff"""
    st.sidebar.success("🔄 Handing off to Market Intelligence Agent")


def create_triage_agent(client: AsyncOpenAI, model_name: str, enterprise_agent, market_agent):
    """Create Triage Agent with handoff capabilities"""
    
    # Load base prompt
    triage_agent_prompt = load_prompt('prompts/triage_agent.txt')
    
    # Enhanced triage prompt with conversation summarization
    enhanced_triage_prompt = triage_agent_prompt + """

## Updated Decision Logic for Compound Questions
For compound questions that require information from multiple agents:
1. Identify the primary intent/goal of the query (what information does the user ultimately want?)
2. Route to the agent that is best suited to deliver the primary information
3. The specialist agent will use other agents as tools when needed

Examples of compound questions:
- "Based on where store 110 is located, what are the demographics of the area?"
   → Route to Market Intelligence Agent (primary goal is demographics information)
   → The Market Intelligence Agent will use the Enterprise Intelligence Agent tool to get store 110's location

## Conversation Summarization 
When the user asks for a summary of the conversation (e.g., "summarize our conversation", "what have we discussed?", etc.):
1. Access the conversation_history from the shared context
2. Generate a concise, structured summary of the key points
3. Focus on key questions, insights, and decision points from the conversation
4. Highlight any important information discovered during the conversation
5. Do NOT hand off to other agents for summarization requests
"""
    
    return Agent(
        name="Triage Agent",
        instructions=enhanced_triage_prompt,
        model=OpenAIChatCompletionsModel(model=model_name, openai_client=client),
        handoffs=[
            handoff(enterprise_agent, on_handoff=on_enterprise_intelligence_handoff),
            handoff(market_agent, on_handoff=on_market_intelligence_handoff),
        ],
    )