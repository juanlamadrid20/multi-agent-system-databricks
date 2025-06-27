#!/usr/bin/env python3
"""
Simple test runner for Research tools integration tests.
This script runs the integration tests and displays results in a user-friendly format.
"""

import os
import sys
import unittest
from dotenv import load_dotenv

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Load environment variables from .env file
load_dotenv(os.path.join(project_root, ".env"))

def run_research_tests():
    """Run Research integration tests and display results"""
    print("=" * 60)
    print("RESEARCH TOOLS INTEGRATION TESTS")
    print("=" * 60)
    
    # Check environment variables first
    required_vars = ['PERPLEXITY_API_KEY']
    
    print("\n🔍 Checking Environment Variables:")
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var}: Not set")
        else:
            print(f"✅ {var}: Set (length: {len(value)})")
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables: {missing_vars}")
        print("Please set these variables in your .env file and try again.")
        return False
    
    print("\n🚀 Running Integration Tests...")
    print("-" * 40)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.join(project_root, 'tests/integration'), pattern='test_research_tools.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if result.wasSuccessful():
        print(f"✅ All {result.testsRun} tests passed!")
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors out of {result.testsRun} tests")
        
        if result.failures:
            print("\n📋 Failures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\n')[0]}")
        
        if result.errors:
            print("\n🚨 Errors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback.split('\n')[-2]}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    try:
        success = run_research_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)