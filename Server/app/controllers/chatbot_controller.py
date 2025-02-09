# app/controllers/chatbot_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
from pydantic import BaseModel
from app.services.chatbot_service import ChatbotService
from app.db.database import get_db
from fastapi.responses import JSONResponse
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
        # Validate input
        if not chat_message.message.strip():
            return {
                "response": "Message cannot be empty",
                "status": "error",
                "error": "EMPTY_MESSAGE"
            }

        # Get response from chatbot service
        response = await chatbot_service.get_response("user", chat_message.message)

        # If the response indicates an error
        if response.get("status") == "error":
            return JSONResponse(
                status_code=status.HTTP_200_OK,  # Keep 200 to maintain frontend compatibility
                content={
                    "response": response.get("response"),
                    "status": "error",
                    "error": response.get("error", "UNKNOWN_ERROR")
                }
            )

        # Return successful response
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response
        )

    except Exception as e:
        logger.error(f"Controller error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,  # Keep 200 to maintain frontend compatibility
            content={
                "response": "An unexpected error occurred. Please try again later.",
                "status": "error",
                "error": "INTERNAL_SERVER_ERROR"
            }
        )