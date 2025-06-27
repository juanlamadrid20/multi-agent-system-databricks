import os
import time
from typing import Dict, Any
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")


class GenieClient:
    """Reusable client for interacting with Databricks Genie API"""
    
    def __init__(self, workspace_client: WorkspaceClient = None):
        """
        Initialize the Genie client
        
        Args:
            workspace_client: Optional pre-configured WorkspaceClient. 
                            If None, creates a new one from environment variables.
        """
        if workspace_client:
            self.w = workspace_client
        else:
            self.w = WorkspaceClient(
                host=os.getenv("DATABRICKS_HOST"),
                token=os.getenv("DATABRICKS_TOKEN"),
                auth_type="pat",
            )
    
    def query_genie_space(
        self, 
        space_id: str, 
        user_query: str, 
        timeout: float = 60.0, 
        poll_interval: float = 2.0
    ) -> Dict[str, Any]:
        """
        Execute a query against a Genie space and return the results
        
        Args:
            space_id: The Genie space ID to query
            user_query: The natural language query to execute
            timeout: Maximum time to wait for query completion (seconds)
            poll_interval: How often to poll for completion (seconds)
            
        Returns:
            Dict containing the query results or error information
            
        Raises:
            TimeoutError: If the query doesn't complete within the timeout period
        """
        print(f"INFO: Querying Genie space {space_id} with query: {user_query}")
        
        # Step 1: Start a new conversation using the SDK
        message = self.w.genie.start_conversation_and_wait(space_id, user_query)
        conversation_id = message.conversation_id
        message_id = message.id
        
        # Step 2: Poll for completion using the SDK
        start_time = time.time()
        while True:
            msg = self.w.genie.get_message(space_id, conversation_id, message_id)
            status = msg.status.value if msg.status else None
            
            if status == "COMPLETED":
                if msg.attachments and len(msg.attachments) > 0:
                    attachment_id = msg.attachments[0].attachment_id
                    result = self.w.genie.get_message_attachment_query_result(
                        space_id, conversation_id, message_id, attachment_id
                    )
                    return result.statement_response.as_dict()
                else:
                    return {"error": "No attachments found in message."}
            
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Genie API query timed out after {timeout} seconds.")
            
            time.sleep(poll_interval)
    
    def query_store_performance(self, user_query: str) -> Dict[str, Any]:
        """
        Query the store performance Genie space
        
        Args:
            user_query: The natural language query about store performance
            
        Returns:
            Dict containing the query results
        """
        space_id = os.getenv("GENIE_SPACE_STORE_PERFORMANCE_ID")
        if not space_id:
            raise ValueError("GENIE_SPACE_STORE_PERFORMANCE_ID environment variable is not set")
        
        return self.query_genie_space(space_id, user_query)
    
    def query_product_inventory(self, user_query: str) -> Dict[str, Any]:
        """
        Query the product inventory Genie space
        
        Args:
            user_query: The natural language query about product inventory
            
        Returns:
            Dict containing the query results
        """
        space_id = os.getenv("GENIE_SPACE_PRODUCT_INV_ID")
        if not space_id:
            raise ValueError("GENIE_SPACE_PRODUCT_INV_ID environment variable is not set")
        
        return self.query_genie_space(space_id, user_query)