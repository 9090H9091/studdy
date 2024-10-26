import aiohttp
import json
from config import OLLAMA_API_URL, OLLAMA_MODEL

async def get_ollama_response(prompt, message):
    headers = {'Content-Type': 'application/json'}
    data = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": True}
    full_response = ""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{OLLAMA_API_URL}/api/generate", json=data, headers=headers) as response:
                response.raise_for_status()
                async for line in response.content:
                    if line:
                        line_data = json.loads(line.decode('utf-8'))
                        chunk = line_data.get("response", "")
                        full_response += chunk

                        if len(full_response) <= 2000:
                            await message.edit(content=full_response)
                        else:
                            await message.edit(content=full_response[-2000:])

            return full_response.strip() if full_response else "No response"
        except aiohttp.ClientError as e:
            print(f"Error communicating with Ollama: {e}")
            return "There was an error communicating with the model."
        except ValueError as e:
            print(f"JSON decoding error: {e}")
            return "Received an invalid response from the model."
