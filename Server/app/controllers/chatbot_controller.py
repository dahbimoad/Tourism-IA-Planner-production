# app/controllers/chatbot_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
from pydantic import BaseModel
from app.services.chatbot_service import ChatbotService
from app.db.database import get_db
from fastapi.responses import JSONResponse
import uuid
import logging

logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    message: str

router = APIRouter()
chatbot_service = ChatbotService()

@router.post("")
async def chat(
        chat_message: ChatMessage,
        db: Session = Depends(get_db)
) -> Dict:
    try:
        if not chat_message.message.strip():
            return JSONResponse(
                status_code=status.HTTP_200_OK,  # Keep 200 for frontend compatibility
                content={
                    "response": "Please enter a message",
                    "status": "error",
                    "error": "EMPTY_MESSAGE"
                }
            )

        # Generate a random user ID for non-authenticated users
        anonymous_user_id = str(uuid.uuid4())

        response = await chatbot_service.get_response(
            anonymous_user_id,
            chat_message.message
        )

        # Always return 200 status code for frontend compatibility
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response
        )

    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,  # Keep 200 for frontend compatibility
            content={
                "response": "⚠️ The chat service is currently unavailable. Please try again later.",
                "status": "error",
                "error": "SERVICE_ERROR"
            }
        )