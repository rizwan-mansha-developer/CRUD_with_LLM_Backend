from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..db import get_db
from .. import models
from ..ai import ask_ai
import json
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    user_id: int
    message: str
    conversation_history: Optional[List[Dict[str, Any]]] = None

@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Build conversation with history
    messages = [
        {
            "role": "system", 
            "content": f"""You are a helpful finance assistant for user ID {request.user_id}. 
            
Your job is to help users add expenses and retrieve their expense history.
            
When adding expenses, you need ALL of these parameters:
            - user_id: {request.user_id} (already provided)
            - amount: The expense amount (required)
            - category: The expense category like 'food', 'transport', 'office', etc. (required)
            - date: Date in YYYY-MM-DD format (required)
            
If any required information is missing, ask the user for the specific missing details. 
Remember previous information they provided in the conversation and don't ask for it again.
            Be conversational and helpful."""
        }
    ]
    
    # Add conversation history if provided
    if request.conversation_history:
        messages.extend(request.conversation_history)
    
    # Add current user message
    messages.append({"role": "user", "content": request.message})

    print("Messages:", messages)

    try:
        response = ask_ai(messages)
        
        # Extract response text
        response_text = ""
        if hasattr(response, 'text') and response.text:
            response_text = response.text
        elif hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
        
        return {
            "reply": response_text or "I'm here to help with your expenses. What would you like to do?",
            "conversation_history": messages + [{"role": "assistant", "content": response_text}]
        }
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")
