import os
from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient
from unitycatalog.ai.core.databricks import (
    DatabricksFunctionClient,
    FunctionExecutionResult,
)

load_dotenv(".env")


class BusinessConductPolicy:
    """Class to handle business conduct policy queries using Databricks function calling"""
    
    def __init__(self):
        """Initialize the Databricks clients"""
        self.w = WorkspaceClient(
            host=os.getenv("DATABRICKS_HOST"),
            token=os.getenv("DATABRICKS_TOKEN"),
            auth_type="pat",
        )
        self.dbclient = DatabricksFunctionClient(client=self.w)
    
    def get_business_conduct_policy_info(self, search_query: str) -> FunctionExecutionResult:
        """
        Get business conduct policy information using Databricks function calling
        
        Args:
            search_query: The search query for policy information
            
        Returns:
            FunctionExecutionResult: The result from the Databricks function
        """
        if not search_query or not search_query.strip():
            raise ValueError("Search query cannot be empty")
            
        return self.dbclient.execute_function(
            function_name="juan_dev.genai.retail_club_conduct",
            parameters={"search_query": search_query},
        )