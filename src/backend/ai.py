import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import date, datetime
from sqlalchemy.orm import Session
from . import models, db

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=api_key)

# Define function schema for Gemini
add_expense_function = {
    "name": "add_expense",
    "description": "Add a new expense for the user",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "user_id": {
                "type": "INTEGER",
                "description": "The ID of the user adding the expense"
            },
            "amount": {
                "type": "NUMBER",
                "description": "The amount of the expense"
            },
            "category": {
                "type": "STRING",
                "description": "The category of the expense (e.g., food, transport, office)"
            },
            "date": {
                "type": "STRING",
                "description": "The date of the expense in YYYY-MM-DD format"
            },
        },
        "required": ["user_id", "amount", "category", "date"],
    },
}

get_expense_by_user_id_function = {
    "name": "get_expense",
    "description": "Get expanses of user by user_id",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "user_id": {
                "type": "INTEGER",
                "description": "The ID of the user adding the expense"
            },
        },
        "required": ["user_id"],
    },
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[add_expense_function, get_expense_by_user_id_function]
)

def add_expense_impl(user_id: int, amount: float, category: str, date_str: str):
    """Actual implementation of add_expense function"""
    try:
        db_session = next(db.get_db())
        expense_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        new_expense = models.Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            date=expense_date
        )
        
        db_session.add(new_expense)
        db_session.commit()
        db_session.refresh(new_expense)
        
        return f"Expense added successfully! ID: {new_expense.id}, Amount: ${amount}, Category: {category}, Date: {date_str}"
    except Exception as e:
        return f"Error adding expense: {str(e)}"
    finally:
        db_session.close()

def get_expense_impl(user_id: int):
    """Actual implementation of get_expense function"""
    try:
        db_session = next(db.get_db())
        expenses = db_session.query(models.Expense).filter(models.Expense.user_id == user_id).all()
        
        if not expenses:
            return f"No expenses found for user ID {user_id}"
        
        result = f"Expenses for user ID {user_id}:\n"
        for expense in expenses:
            result += f"- ${expense.amount} ({expense.category}) on {expense.date}\n"
        
        return result
    except Exception as e:
        return f"Error fetching expenses: {str(e)}"
    finally:
        db_session.close()

def ask_ai(messages: list):
    """Enhanced AI function with proper function calling and conversation continuity"""
    try:
        # Start a chat session for conversation continuity
        chat = model.start_chat(history=[])
        
        # Build conversation history
        conversation_text = ""
        for msg in messages:
            if msg["role"] == "system":
                conversation_text += f"System: {msg['content']}\n"
            elif msg["role"] == "user":
                conversation_text += f"User: {msg['content']}\n"
            elif msg["role"] == "assistant":
                conversation_text += f"Assistant: {msg['content']}\n"
        
        # Send the latest user message
        latest_user_msg = next((msg["content"] for msg in reversed(messages) if msg["role"] == "user"), "")
        
        response = chat.send_message(
            conversation_text + f"\nUser: {latest_user_msg}",
            generation_config=genai.types.GenerationConfig(temperature=0.7)
        )
        
        # Handle function calls
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = dict(function_call.args)
                    
                    # Execute the function
                    if function_name == "add_expense":
                        result = add_expense_impl(
                            user_id=function_args.get("user_id"),
                            amount=function_args.get("amount"),
                            category=function_args.get("category"),
                            date_str=function_args.get("date")
                        )
                    elif function_name == "get_expense":
                        result = get_expense_impl(user_id=function_args.get("user_id"))
                    else:
                        result = f"Unknown function: {function_name}"
                    
                    # Send function result back to continue conversation
                    function_response = chat.send_message(
                        f"Function {function_name} executed with result: {result}"
                    )
                    return function_response
        
        return response
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Return a mock response for testing
        class MockResponse:
            def __init__(self):
                self.text = "I'm here to help with your expenses. Please provide the details you'd like to add or ask me to retrieve your expenses."
                self.candidates = []
        return MockResponse()
