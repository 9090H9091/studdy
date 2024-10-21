import os
import aiohttp
from helpers.logger import get_logger

logger = get_logger(__name__)

OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', "llama2:13b")

async def get_ai_response(prompt: str) -> str:
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{OLLAMA_API_URL}/api/generate", json=data, headers=headers) as response:
                response.raise_for_status()
                full_response = ""
                async for line in response.content:
                    if line:
                        try:
                            line_data = await response.json()
                            chunk = line_data.get("response", "")
                            full_response += chunk
                        except Exception as e:
                            logger.error(f"Error processing AI response chunk: {e}")
                
                return full_response.strip() if full_response else "No response generated"
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return "Sorry, I encountered an error while processing your request."
