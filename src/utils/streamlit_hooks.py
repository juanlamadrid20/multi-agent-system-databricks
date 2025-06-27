import time
import streamlit as st
from agents import RunContextWrapper
from src.agents.shared_context import SharedAgentContext


class StreamlitAgentHooks:
    """Custom hooks for Streamlit visualization of agent execution"""
    
    def __init__(self):
        self.start_time = None
        self.agent_status = st.empty()
        self.tool_status = st.empty()
        
    async def on_agent_start(self, context: RunContextWrapper[SharedAgentContext], agent):
        self.start_time = time.time()
        agent_name = agent.name
        context.context.current_agent = agent_name
        
        with self.agent_status.container():
            st.markdown(f"""
            <div class="agent-status agent-active">
                <div class="agent-icon">🤖</div>
                <div class="agent-name">{agent_name}</div>
                <div class="status-indicator">Active</div>
            </div>
            """, unsafe_allow_html=True)
    
    async def on_agent_end(self, context: RunContextWrapper[SharedAgentContext], agent, output):
        agent_name = agent.name
        duration = time.time() - self.start_time
        
        # Add to conversation history
        context.context.add_message(f"{agent_name}", output)
        
        with self.agent_status.container():
            st.markdown(f"""
            <div class="agent-status agent-complete">
                <div class="agent-icon">✅</div>
                <div class="agent-name">{agent_name}</div>
                <div class="status-indicator">Completed in {duration:.2f}s</div>
            </div>
            """, unsafe_allow_html=True)
        
    async def on_tool_start(self, context: RunContextWrapper[SharedAgentContext], agent, tool):
        tool_name = tool.name
        context.context.current_tool = tool_name
        
        with self.tool_status.container():
            st.markdown(f"""
            <div class="tool-status tool-active">
                <div class="tool-icon">🔧</div>
                <div class="tool-name">{tool_name}</div>
                <div class="status-indicator">Running...</div>
            </div>
            """, unsafe_allow_html=True)
        
    async def on_tool_end(self, context: RunContextWrapper[SharedAgentContext], agent, tool, result):
        tool_name = tool.name
        
        # Record tool usage in conversation history
        context.context.add_message(f"Tool ({tool_name})", str(result))
        
        with self.tool_status.container():
            st.markdown(f"""
            <div class="tool-status tool-complete">
                <div class="tool-icon">✓</div>
                <div class="tool-name">{tool_name}</div>
                <div class="status-indicator">Completed</div>
            </div>
            """, unsafe_allow_html=True)
    
    async def on_handoff(self, context: RunContextWrapper[SharedAgentContext], from_agent, to_agent):
        from_name = from_agent.name
        to_name = to_agent.name
        
        # Record handoff in conversation history
        context.context.add_message("System", f"Handoff from {from_name} to {to_name}")
        
        with self.agent_status.container():
            st.markdown(f"""
            <div class="handoff-status">
                <div class="from-agent">{from_name}</div>
                <div class="handoff-icon">↪️</div>
                <div class="to-agent">{to_name}</div>
            </div>
            """, unsafe_allow_html=True)