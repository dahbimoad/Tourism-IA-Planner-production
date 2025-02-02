import requests
from typing import Dict, List
from fastapi import HTTPException


class ChatbotService:
    def __init__(self):
        self.base_url = "http://localhost:11434/api"
        self.model = "llama3.2:1b"
        self.conversation_history = {}

    async def get_response(self, user_id: str, message: str) -> Dict:
        try:
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []

            # Build context from conversation history
            context = "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in self.conversation_history[user_id][-5:]
            ])

            # Create a tourism-focused prompt
            prompt = f"""You are a knowledgeable Moroccan tourism assistant. Help users plan their trips, 
            recommend places to visit, and provide information about local customs, transportation, and accommodations.

            Previous conversation:
            {context}

            User: {message}
            Assistant:"""

            try:
                # Make request to Ollama
                response = requests.post(
                    f"{self.base_url}/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=120
                )

                # Print response for debugging
                print(f"Ollama response status: {response.status_code}")
                print(f"Ollama response: {response.text}")

                if response.status_code != 200:
                    error_msg = f"Ollama API error: {response.text}"
                    print(error_msg)
                    raise HTTPException(status_code=500, detail=error_msg)

                # Get the response
                response_json = response.json()
                assistant_response = response_json.get('response', '')

                if not assistant_response:
                    print("Empty response from Ollama")
                    raise HTTPException(status_code=500, detail="Empty response from Ollama")

                # Update conversation history
                self.conversation_history[user_id].extend([
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": assistant_response}
                ])

                return {
                    "response": assistant_response,
                    "status": "success"
                }

            except requests.exceptions.ConnectionError:
                error_msg = "Could not connect to Ollama. Make sure Ollama is running with: ollama run llama3.2"
                print(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)

            except requests.exceptions.Timeout:
                error_msg = "Request to Ollama timed out"
                print(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)

        except Exception as e:
            error_msg = f"Error in chatbot service: {str(e)}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)


# Create a singleton instance
chatbot_service = ChatbotService()