# app/controllers/chatbot_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
from pydantic import BaseModel
from app.services.chatbot_service import ChatbotService
from app.db.database import get_db
from app.controllers.auth_controller import get_current_user
from app.db.models import User
from fastapi.responses import JSONResponse
from requests.exceptions import RequestException


class ChatMessage(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: str


router = APIRouter()
chatbot_service = ChatbotService()


@router.post("")
async def chat(
        chat_message: ChatMessage,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> Dict:
    try:
        # Validate message content
        if not chat_message.message.strip():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": "Message cannot be empty",
                    "error_code": "EMPTY_MESSAGE"
                }
            )

        response = await chatbot_service.get_response(
            str(current_user.id),
            chat_message.message
        )
        return response

    except HTTPException as he:
        # Handle authentication and other HTTP exceptions
        error_code = "AUTH_ERROR" if he.status_code == 401 else f"ERROR_{he.status_code}"
        return JSONResponse(
            status_code=he.status_code,
            content={
                "detail": str(he.detail),
                "error_code": error_code
            }
        )

    except RequestException as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": "The chat service is temporarily unavailable. Please try again later.",
                "error_code": "SERVICE_UNAVAILABLE",
                "additional_info": str(e)
            }
        )

    except ValueError as ve:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(ve),
                "error_code": "VALIDATION_ERROR"
            }
        )

    except Exception as e:
        # Log unexpected errors
        print(f"Unexpected error in chat endpoint: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occurred. Please try again later.",
                "error_code": "INTERNAL_SERVER_ERROR"
            }
        )