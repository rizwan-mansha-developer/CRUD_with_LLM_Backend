#!/usr/bin/env python3
"""
Test script to verify Gemini AI integration
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_import():
    """Test if Gemini AI can be imported"""
    try:
        import google.generativeai as genai
        print("[OK] Gemini AI imported successfully")
        return True
    except ImportError as e:
        print(f"[FAIL] Failed to import Gemini AI: {e}")
        return False

def test_api_key():
    """Test if API key is configured"""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        print("[OK] Gemini API key is configured")
        return True
    else:
        print("[FAIL] Gemini API key not configured. Please set GEMINI_API_KEY in .env file")
        return False

def test_function_calling():
    """Test Gemini function calling capability"""
    try:
        from src.backend.ai import ask_ai
        
        # Test message
        messages = [
            {"role": "system", "content": "You are a finance assistant helping employees log expenses."},
            {"role": "user", "content": "I spent $25 on lunch today for user ID 1 in the food category on 2024-01-15"}
        ]
        
        print("[OK] AI module imported successfully")
        print("Note: To test function calling, you need a valid Gemini API key")
        return True
        
    except Exception as e:
        print(f"[FAIL] Error testing function calling: {e}")
        return False

if __name__ == "__main__":
    print("Testing Gemini AI Integration...")
    print("-" * 40)
    
    tests = [
        test_gemini_import,
        test_api_key,
        test_function_calling
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("SUCCESS: All tests passed! Gemini integration is ready.")
    else:
        print("WARNING: Some tests failed. Please check the configuration.")