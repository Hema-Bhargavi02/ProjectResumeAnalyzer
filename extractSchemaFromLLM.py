from google.genai import types
import os
from google import genai

client = genai.Client(
    api_key=os.getenv("LLM_API_KEY")
)


def extract_structured_data(content, schema):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=content,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema
        )
    )

    return response.parsed