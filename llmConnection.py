import os
from google import genai

client = genai.Client(
    api_key=os.getenv("LLM_API_KEY")
)