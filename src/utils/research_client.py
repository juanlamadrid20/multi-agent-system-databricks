import os
import time
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")


class PerplexityResearchClient:
    """Reusable client for interacting with Perplexity AI for research and reasoning"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.perplexity.ai"):
        """
        Initialize the Perplexity research client
        
        Args:
            api_key: Perplexity API key. If None, uses PERPLEXITY_API_KEY environment variable
            base_url: Perplexity API base URL
        """
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        self.base_url = base_url
        
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
    
    def research_and_reason(
        self, 
        user_query: str, 
        model: str = "sonar-reasoning-pro",
        include_date: bool = True,
        system_prompt: str = None,
        stream: bool = True
    ) -> str:
        """
        Perform research and reasoning on a user query
        
        Args:
            user_query: The user's question or request
            model: The Perplexity model to use (default: sonar-reasoning-pro)
            include_date: Whether to include current date in the query
            system_prompt: Custom system prompt (uses default if None)
            stream: Whether to use streaming responses
            
        Returns:
            The research response including reasoning process
        """
        print(f"INFO: Researching query with Perplexity AI: {user_query}")
        
        # Prepare system prompt
        if system_prompt is None:
            system_prompt = (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            )
        
        # Prepare user message
        user_content = user_query
        if include_date:
            current_date = time.strftime('%d %B %Y')
            user_content = f"today is {current_date} + {user_query}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
        
        if stream:
            return self._stream_completion(messages, model)
        else:
            return self._non_stream_completion(messages, model)
    
    def _stream_completion(self, messages: List[Dict[str, str]], model: str) -> str:
        """Handle streaming completion"""
        response_stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        
        full_response = ""
        for response in response_stream:
            if response.choices and response.choices[0].delta.content:
                content = response.choices[0].delta.content
                full_response += content
        
        return full_response
    
    def _non_stream_completion(self, messages: List[Dict[str, str]], model: str) -> str:
        """Handle non-streaming completion"""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        
        return response.choices[0].message.content
    
    def research_market_trends(self, topic: str, region: str = None) -> str:
        """
        Research market trends for a specific topic
        
        Args:
            topic: The market topic to research
            region: Optional region to focus on
            
        Returns:
            Market trends research response
        """
        query = f"What are the current market trends for {topic}"
        if region:
            query += f" in {region}"
        query += "? Include recent data and analysis."
        
        return self.research_and_reason(
            query,
            system_prompt=(
                "You are a market research analyst. Provide detailed, data-driven "
                "insights about market trends with recent statistics and analysis."
            )
        )
    
    def research_demographics(self, location: str, aspects: List[str] = None) -> str:
        """
        Research demographic information for a location
        
        Args:
            location: The location to research
            aspects: Specific demographic aspects to focus on
            
        Returns:
            Demographic research response
        """
        query = f"What are the key demographic characteristics of {location}"
        if aspects:
            query += f", specifically focusing on {', '.join(aspects)}"
        query += "? Include recent census data and trends."
        
        return self.research_and_reason(
            query,
            system_prompt=(
                "You are a demographic researcher. Provide comprehensive demographic "
                "analysis with recent census data, population statistics, and trends."
            )
        )
    
    def research_competitor_analysis(self, company: str, industry: str) -> str:
        """
        Research competitor analysis for a company
        
        Args:
            company: The company to analyze
            industry: The industry context
            
        Returns:
            Competitor analysis research response
        """
        query = (
            f"Provide a competitive analysis for {company} in the {industry} industry. "
            "Include market positioning, key competitors, strengths, and challenges."
        )
        
        return self.research_and_reason(
            query,
            system_prompt=(
                "You are a business analyst specializing in competitive intelligence. "
                "Provide thorough competitive analysis with market insights and strategic recommendations."
            )
        )