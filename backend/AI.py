# Gemini/GPT/any of the other 100+ LLMs apis
# AIzaSyBbzu4VHtP5FWzLB5PApAtHHVUEVCvG1VQ
import asyncio
from random import choice

from google import genai
from constants import GeminiModels

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AIzaSyBbzu4VHtP5FWzLB5PApAtHHVUEVCvG1VQ")
# Remember to set this API in env file instead

async def gem():
    txtFile = await client.aio.files.upload(file="Rough.txt")

    response = await client.aio.models.generate_content_stream(
        model = GeminiModels.G25FlashLite,
        contents = ["Summarise this text file in 10 lines.", txtFile]
    )
    async for chunk in response:
        for letters in chunk.text:
            print(letters, end="")
            ran = choice([0.000001, 0.0001, 0.01, 0.01])
            await asyncio.sleep(ran)
        # print(end="")

    client.files.delete(name=txtFile.name)

if __name__ == '__main__':
    asyncio.run(gem())
