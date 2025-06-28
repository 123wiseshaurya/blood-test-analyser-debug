#!/usr/bin/env python3
"""
Test script for Blood Test Report Analyser
This script tests the core functionality without requiring a full server setup.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all modules can be imported successfully."""
    print("🔍 Testing imports...")
    
    try:
        from tools import llm, blood_test_tool
        print("✅ Tools imported successfully")
    except Exception as e:
        print(f"❌ Tools import failed: {e}")
        return False
    
    try:
        from agents import doctor
        print("✅ Agents imported successfully")
    except Exception as e:
        print(f"❌ Agents import failed: {e}")
        return False
    
    try:
        from task import help_patients
        print("✅ Tasks imported successfully")
    except Exception as e:
        print(f"❌ Tasks import failed: {e}")
        return False
    
    try:
        from main import app
        print("✅ FastAPI app imported successfully")
    except Exception as e:
        print(f"❌ FastAPI app import failed: {e}")
        return False
    
    return True

def test_llm_configuration():
    """Test if LLM is properly configured."""
    print("\n🤖 Testing LLM configuration...")
    
    try:
        from tools import llm
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key or api_key == "your_openai_api_key_here":
            print("⚠️  OpenAI API key not configured. Set OPENAI_API_KEY in .env file")
            return False
        else:
            print("✅ LLM configured with API key")
            return True
    except Exception as e:
        print(f"❌ LLM configuration failed: {e}")
        return False

def test_pdf_tool():
    """Test PDF reading tool functionality."""
    print("\n📄 Testing PDF tool...")
    
    try:
        from tools import blood_test_tool
        
        # Test with a non-existent file
        result = blood_test_tool.func("non_existent_file.pdf")
        if "Error: File not found" in result:
            print("✅ PDF tool error handling works correctly")
            return True
        else:
            print("❌ PDF tool error handling failed")
            return False
    except Exception as e:
        print(f"❌ PDF tool test failed: {e}")
        return False

def test_crew_setup():
    """Test CrewAI setup and configuration."""
    print("\n👥 Testing CrewAI setup...")
    
    try:
        from crewai import Crew, Process
        from agents import doctor
        from task import help_patients
        
        # Create a test crew
        test_crew = Crew(
            agents=[doctor],
            tasks=[help_patients],
            process=Process.sequential,
        )
        
        print("✅ CrewAI setup successful")
        return True
    except Exception as e:
        print(f"❌ CrewAI setup failed: {e}")
        return False

def test_file_structure():
    """Test if required directories exist."""
    print("\n📁 Testing file structure...")
    
    required_dirs = ["data", "outputs"]
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"⚠️  Creating missing directory: {dir_name}")
            os.makedirs(dir_name, exist_ok=True)
        else:
            print(f"✅ Directory exists: {dir_name}")
    
    return True

def main():
    """Run all tests."""
    print("🧪 Blood Test Report Analyser - System Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_llm_configuration,
        test_pdf_tool,
        test_crew_setup,
        test_file_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("\n🚀 To start the server, run:")
        print("   python main.py")
        print("\n🌐 Then visit:")
        print("   http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 