from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class SharedAgentContext:
    """Shared context class to pass data between agents"""
    store_location: Optional[str] = None
    store_id: Optional[str] = None
    demographic_data: Optional[Dict] = None
    state_code: Optional[str] = None
    current_agent: Optional[str] = None
    current_tool: Optional[str] = None
    conversation_history: List = None
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
            
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.conversation_history.append({"role": role, "content": content})
        
    def get_formatted_history(self):
        """Format conversation history for consumption by agents"""
        if not self.conversation_history:
            return "No conversation history available."
        
        formatted_history = []
        for msg in self.conversation_history:
            formatted_history.append(f"{msg['role']}: {msg['content']}")
        
        return "\n\n".join(formatted_history)