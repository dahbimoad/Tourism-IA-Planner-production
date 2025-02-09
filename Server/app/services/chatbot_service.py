# app/services/chatbot_service.py
from openai import OpenAI, APIError, AuthenticationError, RateLimitError
from typing import Dict
from fastapi import HTTPException
from app.core.config import settings
import asyncio
import logging

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.AI_API_KEY)
        self.model = settings.AI_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT
        self.max_history = settings.MAX_CONVERSATION_HISTORY
        self.conversation_history = {}

    async def get_response(self, user_id: str, message: str) -> Dict:
        try:
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []

            # Build context from conversation history
            context = "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in self.conversation_history[user_id][-self.max_history:]
            ])

            try:
                # Make request to OpenAI
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": "You are a helpful Moroccan tourism assistant."},
                            {"role": "user", "content": message}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                )

                assistant_response = response.choices[0].message.content
                return {
                    "response": assistant_response,
                    "status": "success"
                }

            except AuthenticationError as auth_error:
                logger.error(f"Authentication error: {str(auth_error)}")
                return {
                    "response": "⚠️ The chat service is currently unavailable. Our team is working on it. Please try again later.",
                    "status": "error",
                    "error": "SERVICE_UNAVAILABLE"
                }

            except RateLimitError:
                return {
                    "response": "The service is experiencing high demand. Please try again in a few moments.",
                    "status": "error",
                    "error": "RATE_LIMIT"
                }

            except Exception as e:
                logger.error(f"OpenAI API error: {str(e)}")
                return {
                    "response": "⚠️ Service temporarily unavailable. Please try again later.",
                    "status": "error",
                    "error": "API_ERROR"
                }

        except Exception as e:
            logger.error(f"Service error: {str(e)}")
            return {
                "response": "⚠️ Service temporarily unavailable. Please try again later.",
                "status": "error",
                "error": "SERVICE_ERROR"
            }

# Create a singleton instance
chatbot_service = ChatbotService()