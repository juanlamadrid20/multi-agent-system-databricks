import unittest
import os
from dotenv import load_dotenv
from src.policies.business_conduct_policy import BusinessConductPolicy
from unitycatalog.ai.core.databricks import FunctionExecutionResult

# Load environment variables from .env file
load_dotenv(".env")


class TestBusinessConductPolicy(unittest.TestCase):
    """Live integration tests for BusinessConductPolicy with real Databricks API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - check if required environment variables are present"""
        required_vars = ['DATABRICKS_HOST', 'DATABRICKS_TOKEN']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise unittest.SkipTest(
                f"Skipping live tests - missing environment variables: {missing_vars}"
            )
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.policy = BusinessConductPolicy()
    
    def tearDown(self):
        """Clean up after each test method"""
        self.policy = None
    
    def test_business_conduct_policy_query(self):
        """Test actual function call with real Databricks API"""
        search_query = "policy for HR leave?"
        
        try:
            result = self.policy.get_business_conduct_policy_info(search_query)
            
            # Verify result structure
            self.assertIsInstance(result, FunctionExecutionResult)
            self.assertIsNotNone(result.value)
            
            # Print result for manual verification
            print(f"\nLive test result for query '{search_query}':")
            print(f"Result type: {type(result)}")
            print(f"Result value: {result.value}")
            
        except Exception as e:
            self.fail(f"Live test failed with exception: {e}")
    
    # def test_empty_query_validation(self):
    #     """Test that empty search query raises ValueError"""
    #     with self.assertRaises(ValueError) as context:
    #         self.policy.get_business_conduct_policy_info("")
        
    #     self.assertIn("Search query cannot be empty", str(context.exception))
    
    # def test_whitespace_query_validation(self):
    #     """Test that whitespace-only search query raises ValueError"""
    #     with self.assertRaises(ValueError) as context:
    #         self.policy.get_business_conduct_policy_info("   ")
        
    #     self.assertIn("Search query cannot be empty", str(context.exception))
    
    # def test_different_policy_queries(self):
    #     """Test multiple different policy queries"""
    #     test_queries = [
    #         "harassment policy",
    #         "data privacy",
    #         "workplace safety",
    #         "ethics guidelines"
    #     ]
        
    #     for query in test_queries:
    #         with self.subTest(query=query):
    #             try:
    #                 result = self.policy.get_business_conduct_policy_info(query)
    #                 self.assertIsInstance(result, FunctionExecutionResult)
    #                 self.assertIsNotNone(result.value)
    #                 print(f"\n✓ Query '{query}' returned: {str(result.value)[:100]}...")
    #             except Exception as e:
    #                 print(f"\n✗ Query '{query}' failed: {e}")
    #                 raise


if __name__ == '__main__':
    # Run with verbose output to see print statements
    unittest.main(verbosity=2)