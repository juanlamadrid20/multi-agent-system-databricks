import unittest
import os
from dotenv import load_dotenv
from src.utils.research_client import PerplexityResearchClient

# Load environment variables from .env file
load_dotenv(".env")


class TestResearchToolsIntegration(unittest.TestCase):
    """Integration tests for research tools with real Perplexity AI API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class - check if required environment variables are present"""
        required_vars = ['PERPLEXITY_API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise unittest.SkipTest(
                f"Skipping live tests - missing environment variables: {missing_vars}"
            )
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Initialize research client for testing
        self.research_client = PerplexityResearchClient()
        
        # Create test function that uses the client
        self.do_research_and_reason = self.research_client.research_and_reason
    
    def test_basic_research_query_live(self):
        """Test basic research functionality with real Perplexity API"""
        test_query = "What are the latest trends in artificial intelligence for 2024?"
        
        try:
            result = self.do_research_and_reason(test_query)
            
            # Verify result structure
            self.assertIsInstance(result, str)
            self.assertIsNotNone(result)
            self.assertGreater(len(result), 100)  # Should be a substantial response
            
            # Print result for manual verification
            print(f"\nBasic Research Test Result:")
            print(f"Query: '{test_query}'")
            print(f"Response length: {len(result)} characters")
            print(f"Response preview: {result[:200]}...")
            
            # Check for reasoning indicators (Perplexity often uses these)
            reasoning_indicators = ["<think>", "analysis", "research", "data", "recent"]
            has_reasoning = any(indicator.lower() in result.lower() for indicator in reasoning_indicators)
            if has_reasoning:
                print("✓ Response contains reasoning/research indicators")
            
        except Exception as e:
            self.fail(f"Basic research test failed with exception: {e}")
    
    def test_market_trends_research_live(self):
        """Test market trends research functionality"""
        topic = "electric vehicles"
        region = "United States"
        
        try:
            result = self.research_client.research_market_trends(topic, region)
            
            # Verify result structure
            self.assertIsInstance(result, str)
            self.assertIsNotNone(result)
            self.assertGreater(len(result), 100)
            
            # Print result for manual verification
            print(f"\nMarket Trends Research Test Result:")
            print(f"Topic: '{topic}', Region: '{region}'")
            print(f"Response length: {len(result)} characters")
            print(f"Response preview: {result[:200]}...")
            
            # Check for market-related content
            market_indicators = ["market", "trend", "growth", "data", "statistics", "analysis"]
            has_market_content = any(indicator.lower() in result.lower() for indicator in market_indicators)
            self.assertTrue(has_market_content, "Response should contain market-related content")
            
        except Exception as e:
            self.fail(f"Market trends research test failed with exception: {e}")
    
    def test_demographics_research_live(self):
        """Test demographics research functionality"""
        location = "California"
        aspects = ["age distribution", "income levels", "education"]
        
        try:
            result = self.research_client.research_demographics(location, aspects)
            
            # Verify result structure
            self.assertIsInstance(result, str)
            self.assertIsNotNone(result)
            self.assertGreater(len(result), 100)
            
            # Print result for manual verification
            print(f"\nDemographics Research Test Result:")
            print(f"Location: '{location}', Aspects: {aspects}")
            print(f"Response length: {len(result)} characters")
            print(f"Response preview: {result[:200]}...")
            
            # Check for demographic-related content
            demo_indicators = ["demographic", "population", "census", "age", "income", "education"]
            has_demo_content = any(indicator.lower() in result.lower() for indicator in demo_indicators)
            self.assertTrue(has_demo_content, "Response should contain demographic-related content")
            
        except Exception as e:
            self.fail(f"Demographics research test failed with exception: {e}")
    
    def test_competitor_analysis_live(self):
        """Test competitor analysis research functionality"""
        company = "Tesla"
        industry = "automotive"
        
        try:
            result = self.research_client.research_competitor_analysis(company, industry)
            
            # Verify result structure
            self.assertIsInstance(result, str)
            self.assertIsNotNone(result)
            self.assertGreater(len(result), 100)
            
            # Print result for manual verification
            print(f"\nCompetitor Analysis Test Result:")
            print(f"Company: '{company}', Industry: '{industry}'")
            print(f"Response length: {len(result)} characters")
            print(f"Response preview: {result[:200]}...")
            
            # Check for competitor analysis content
            analysis_indicators = ["competitor", "competition", "market", "analysis", "strength", "challenge"]
            has_analysis_content = any(indicator.lower() in result.lower() for indicator in analysis_indicators)
            self.assertTrue(has_analysis_content, "Response should contain competitor analysis content")
            
        except Exception as e:
            self.fail(f"Competitor analysis test failed with exception: {e}")
    
    def test_non_streaming_mode(self):
        """Test research functionality without streaming"""
        test_query = "What are the benefits of renewable energy?"
        
        try:
            result = self.research_client.research_and_reason(test_query, stream=False)
            
            # Verify result structure
            self.assertIsInstance(result, str)
            self.assertIsNotNone(result)
            self.assertGreater(len(result), 50)
            
            print(f"\nNon-streaming Test Result:")
            print(f"Query: '{test_query}'")
            print(f"Response length: {len(result)} characters")
            print(f"Response preview: {result[:150]}...")
            
        except Exception as e:
            self.fail(f"Non-streaming research test failed with exception: {e}")
    
    def test_custom_system_prompt(self):
        """Test research with custom system prompt"""
        test_query = "Explain quantum computing"
        custom_prompt = "You are a technical expert. Provide detailed, technical explanations."
        
        try:
            result = self.research_client.research_and_reason(
                test_query, 
                system_prompt=custom_prompt
            )
            
            # Verify result structure
            self.assertIsInstance(result, str)
            self.assertIsNotNone(result)
            self.assertGreater(len(result), 50)
            
            print(f"\nCustom System Prompt Test Result:")
            print(f"Query: '{test_query}'")
            print(f"Custom prompt: '{custom_prompt[:50]}...'")
            print(f"Response length: {len(result)} characters")
            print(f"Response preview: {result[:150]}...")
            
        except Exception as e:
            self.fail(f"Custom system prompt test failed with exception: {e}")
    
    def test_without_date_inclusion(self):
        """Test research without including current date"""
        test_query = "What is machine learning?"
        
        try:
            result = self.research_client.research_and_reason(test_query, include_date=False)
            
            # Verify result structure
            self.assertIsInstance(result, str)
            self.assertIsNotNone(result)
            self.assertGreater(len(result), 50)
            
            print(f"\nNo Date Inclusion Test Result:")
            print(f"Query: '{test_query}'")
            print(f"Response length: {len(result)} characters")
            print(f"Response preview: {result[:150]}...")
            
        except Exception as e:
            self.fail(f"No date inclusion test failed with exception: {e}")
    
    def test_environment_variables_loaded(self):
        """Test that required environment variables are loaded"""
        required_vars = ['PERPLEXITY_API_KEY']
        
        for var in required_vars:
            value = os.getenv(var)
            self.assertIsNotNone(value, f"Environment variable {var} should be set")
            self.assertNotEqual(value.strip(), "", f"Environment variable {var} should not be empty")
            print(f"✓ {var}: {'*' * min(len(value), 10)}... (length: {len(value)})")
    
    def test_client_initialization_with_invalid_api_key(self):
        """Test client initialization with invalid API key"""
        with self.assertRaises(ValueError) as context:
            # Try to create client without API key
            with unittest.mock.patch.dict(os.environ, {}, clear=True):
                PerplexityResearchClient()
        
        self.assertIn("PERPLEXITY_API_KEY", str(context.exception))


if __name__ == '__main__':
    # Run with verbose output to see print statements
    unittest.main(verbosity=2)