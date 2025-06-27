from agents import function_tool
from unitycatalog.ai.core.databricks import FunctionExecutionResult
from src.policies.business_conduct_policy import BusinessConductPolicy
import streamlit as st


@function_tool
def get_business_conduct_policy_info(search_query: str) -> FunctionExecutionResult:
    """
    Get business conduct policy information using Databricks function calling
    
    Args:
        search_query: The search query for policy information
        
    Returns:
        FunctionExecutionResult: The result from the Databricks function
    """
    st.write(
        "<span style='color:green;'>[🛠️TOOL-CALL]: the <a href='https://e2-demo-field-eng.cloud.databricks.com/explore/data/functions/juan_dev/genai/retail_club_conduct' target='_blank'>get_business_conduct_policy_info</a> tool was called</span>",
        unsafe_allow_html=True,
    )
    print("INFO: `get_business_conduct_policy_info` tool called")
    
    policy_handler = BusinessConductPolicy()
    return policy_handler.get_business_conduct_policy_info(search_query)