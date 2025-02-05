# app/controllers/chatbot_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
from pydantic import BaseModel
from app.services.chatbot_service import ChatbotService
from app.db.database import get_db
from fastapi.responses import JSONResponse
from requests.exceptions import RequestException
import uuid


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
        db: Session = Depends(get_db)
) -> Dict:
    try:
        if not chat_message.message.strip():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": "Message cannot be empty",
                    "error_code": "EMPTY_MESSAGE"
                }
            )

        # Generate a random user ID for non-authenticated users
        anonymous_user_id = str(uuid.uuid4())

        response = await chatbot_service.get_response(
            anonymous_user_id,
            chat_message.message
        )
        return response

    except HTTPException as he:
        error_code = f"ERROR_{he.status_code}"
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
        print(f"Unexpected error in chat endpoint: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occurred. Please try again later.",
                "error_code": "INTERNAL_SERVER_ERROR"
            }
        )