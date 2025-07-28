# Gemini/GPT/any of the other 100+ LLMs apis
# AIzaSyBbzu4VHtP5FWzLB5PApAtHHVUEVCvG1VQ

from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AIzaSyBbzu4VHtP5FWzLB5PApAtHHVUEVCvG1VQ")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain the beauty of the universe in a single sentence.",
)
print(response.text)
