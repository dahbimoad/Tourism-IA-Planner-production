# app/controllers/chatbot_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from pydantic import BaseModel
from app.services.chatbot_service import ChatbotService
from app.db.database import get_db
from app.controllers.auth_controller import get_current_user
from app.db.models import User

class ChatMessage(BaseModel):
    message: str

router = APIRouter()
chatbot_service = ChatbotService()

@router.post("")
async def chat(
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    try:
        response = await chatbot_service.get_response(
            str(current_user.id),
            chat_message.message
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))