# app/services/chatbot_service.py
from openai import OpenAI, APIError, AuthenticationError, RateLimitError
from typing import Dict
from fastapi import HTTPException
from app.core.config import settings
import asyncio
import json
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

            # Create tourism-focused prompt
            prompt = f"""You are a knowledgeable Moroccan tourism assistant. Help users plan their trips, 
            recommend places to visit, and provide information about local customs, transportation, and accommodations.

            Previous conversation:
            {context}

            User: {message}
            Assistant:"""

            try:
                # Make request to OpenAI
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": "You are a helpful Moroccan tourism assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                )

                # Get the response
                assistant_response = response.choices[0].message.content

                if not assistant_response:
                    logger.error("Empty response from OpenAI")
                    return {
                        "response": "I apologize, but I couldn't generate a response at the moment. Please try again.",
                        "status": "error"
                    }

                # Update conversation history
                self.conversation_history[user_id].extend([
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": assistant_response}
                ])

                # Trim conversation history
                if len(self.conversation_history[user_id]) > self.max_history * 2:
                    self.conversation_history[user_id] = (
                        self.conversation_history[user_id][-self.max_history * 2:]
                    )

                return {
                    "response": assistant_response,
                    "status": "success"
                }

            except AuthenticationError as auth_error:
                logger.error(f"Authentication error: {str(auth_error)}")
                return {
                    "response": "There was an issue with the AI service authentication. Please try again later.",
                    "status": "error",
                    "error": "API_KEY_ERROR"
                }

            except RateLimitError:
                logger.error("Rate limit exceeded")
                return {
                    "response": "The service is currently experiencing high demand. Please try again in a few moments.",
                    "status": "error",
                    "error": "RATE_LIMIT_ERROR"
                }

            except APIError as api_error:
                logger.error(f"OpenAI API error: {str(api_error)}")
                return {
                    "response": "The AI service is temporarily unavailable. Please try again later.",
                    "status": "error",
                    "error": "API_ERROR"
                }

            except Exception as e:
                logger.error(f"Unexpected API error: {str(e)}")
                return {
                    "response": "An unexpected error occurred. Please try again later.",
                    "status": "error",
                    "error": "UNEXPECTED_ERROR"
                }

        except Exception as e:
            logger.error(f"Service error: {str(e)}")
            return {
                "response": "The service is currently unavailable. Please try again later.",
                "status": "error",
                "error": "SERVICE_ERROR"
            }

# Create a singleton instance
chatbot_service = ChatbotService()