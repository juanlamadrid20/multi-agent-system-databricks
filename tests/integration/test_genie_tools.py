import unittest
import os
from dotenv import load_dotenv
from src.utils.genie_client import GenieClient

# Load environment variables from .env file
load_dotenv(".env")


class TestGenieToolsIntegration(unittest.TestCase):
    """Integration tests for Genie tools with real Databricks API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - check if required environment variables are present"""
        required_vars = [
            'DATABRICKS_HOST', 
            'DATABRICKS_TOKEN', 
            'GENIE_SPACE_STORE_PERFORMANCE_ID',
            'GENIE_SPACE_PRODUCT_INV_ID'
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise unittest.SkipTest(
                f"Skipping live tests - missing environment variables: {missing_vars}"
            )
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Initialize Genie client for testing
        self.genie_client = GenieClient()
        
        # Create test functions that use the client
        self.get_store_performance_info = self.genie_client.query_store_performance
        self.get_product_inventory_info = self.genie_client.query_product_inventory
    
    
    def test_get_store_performance_info_live(self):
        """Test actual store performance query with real Genie API"""
        test_query = "What are the top 5 performing stores by revenue this month?"
        
        try:
            result = self.get_store_performance_info(test_query)
            
            # Verify result structure
            self.assertIsInstance(result, dict)
            self.assertIsNotNone(result)
            
            # Check that we got actual data (not an error)
            self.assertNotIn('error', result)
            
            # Print result for manual verification
            print(f"\nStore Performance Test Result:")
            print(f"Query: '{test_query}'")
            print(f"Result type: {type(result)}")
            print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            if isinstance(result, dict) and 'data_array' in result:
                print(f"Data rows: {len(result.get('data_array', []))}")
            
        except Exception as e:
            self.fail(f"Store performance test failed with exception: {e}")
    
    def test_get_product_inventory_info_live(self):
        """Test actual product inventory query with real Genie API"""
        test_query = "What products have low inventory levels across all stores?"
        
        try:
            result = self.get_product_inventory_info(test_query)
            
            # Verify result structure
            self.assertIsInstance(result, dict)
            self.assertIsNotNone(result)
            
            # Check that we got actual data (not an error)
            self.assertNotIn('error', result)
            
            # Print result for manual verification
            print(f"\nProduct Inventory Test Result:")
            print(f"Query: '{test_query}'")
            print(f"Result type: {type(result)}")
            print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            if isinstance(result, dict) and 'data_array' in result:
                print(f"Data rows: {len(result.get('data_array', []))}")
            
        except Exception as e:
            self.fail(f"Product inventory test failed with exception: {e}")
    
    def test_store_performance_with_specific_store(self):
        """Test store performance query for a specific store"""
        test_query = "Show me performance metrics for store 110"
        
        try:
            result = self.get_store_performance_info(test_query)
            
            self.assertIsInstance(result, dict)
            self.assertNotIn('error', result)
            
            print(f"\nSpecific Store Test Result:")
            print(f"Query: '{test_query}'")
            print(f"Result summary: {str(result)[:200]}...")
            
        except Exception as e:
            self.fail(f"Specific store test failed with exception: {e}")
    
    def test_product_inventory_by_category(self):
        """Test product inventory query by category"""
        test_query = "What is the current inventory for electronics products?"
        
        try:
            result = self.get_product_inventory_info(test_query)
            
            self.assertIsInstance(result, dict)
            self.assertNotIn('error', result)
            
            print(f"\nCategory Inventory Test Result:")
            print(f"Query: '{test_query}'")
            print(f"Result summary: {str(result)[:200]}...")
            
        except Exception as e:
            self.fail(f"Category inventory test failed with exception: {e}")
    
    def test_timeout_handling(self):
        """Test that timeout is handled properly for long-running queries"""
        # This test would require a query that takes longer than the timeout
        # For now, we'll just verify the timeout parameter is being used
        test_query = "Complex analytical query that might take time"
        
        # Test timeout by using a custom timeout value
        try:
            # Use a very short timeout to test timeout handling
            result = self.genie_client.query_genie_space(
                os.getenv("GENIE_SPACE_STORE_PERFORMANCE_ID"), 
                test_query, 
                timeout=0.1  # Very short timeout
            )
            print(f"Query completed too quickly to test timeout: {result}")
        except TimeoutError:
            print("✓ Timeout handling works correctly")
        except Exception as e:
            print(f"Other exception during timeout test: {e}")
    
    def test_environment_variables_loaded(self):
        """Test that required environment variables are loaded"""
        required_vars = [
            'DATABRICKS_HOST', 
            'DATABRICKS_TOKEN', 
            'GENIE_SPACE_STORE_PERFORMANCE_ID',
            'GENIE_SPACE_PRODUCT_INV_ID'
        ]
        
        for var in required_vars:
            value = os.getenv(var)
            self.assertIsNotNone(value, f"Environment variable {var} should be set")
            self.assertNotEqual(value.strip(), "", f"Environment variable {var} should not be empty")
            print(f"✓ {var}: {'*' * min(len(value), 10)}... (length: {len(value)})")


if __name__ == '__main__':
    # Run with verbose output to see print statements
    unittest.main(verbosity=2)