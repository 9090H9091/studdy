import requests
from config import OLLAMA_API_URL, OLLAMA_MODEL, MAX_RESPONSES

async def get_ai_response(question: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": question,
        "max_tokens": 150  # Adjust max tokens as needed
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json().get('output', 'No response from AI.')
    except Exception as e:
        return f"Error: {str(e)}"

