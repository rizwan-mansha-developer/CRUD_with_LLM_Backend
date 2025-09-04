#!/usr/bin/env python3
"""
Test script for enhanced AI function calling with conversation continuity
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from backend.ai import ask_ai

def test_conversation():
    """Test conversation continuity with incomplete information"""
    
    print("=== Testing Conversation Continuity ===\n")
    
    # Test 1: User provides incomplete information
    print("Test 1: User says 'I spent 25 dollars on lunch'")
    messages = [
        {
            "role": "system", 
            "content": """You are a helpful finance assistant for user ID 1. 
            
Your job is to help users add expenses and retrieve their expense history.

When adding expenses, you need ALL of these parameters:
- user_id: 1 (already provided)
- amount: The expense amount (required)
- category: The expense category like 'food', 'transport', 'office', etc. (required)
- date: Date in YYYY-MM-DD format (required)

If any required information is missing, ask the user for the specific missing details. 
Remember previous information they provided in the conversation and don't ask for it again.
Be conversational and helpful."""
        },
        {"role": "user", "content": "I spent 25 dollars on lunch"}
    ]
    
    response1 = ask_ai(messages)
    print(f"AI Response: {response1.text if hasattr(response1, 'text') else 'No text response'}")
    print()
    
    # Test 2: User provides the missing date
    print("Test 2: User provides date 'today' (2024-01-15)")
    messages.extend([
        {"role": "assistant", "content": response1.text if hasattr(response1, 'text') else "What date was this expense?"},
        {"role": "user", "content": "today, 2024-01-15"}
    ])
    
    response2 = ask_ai(messages)
    print(f"AI Response: {response2.text if hasattr(response2, 'text') else 'Function called successfully'}")
    print()
    
    # Test 3: User asks to see their expenses
    print("Test 3: User asks 'show me my expenses'")
    messages.extend([
        {"role": "assistant", "content": response2.text if hasattr(response2, 'text') else "Expense added!"},
        {"role": "user", "content": "show me my expenses"}
    ])
    
    response3 = ask_ai(messages)
    print(f"AI Response: {response3.text if hasattr(response3, 'text') else 'Function called successfully'}")

if __name__ == "__main__":
    test_conversation()