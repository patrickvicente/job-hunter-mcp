from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def call_llm(prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 600, temperature: float = 0.2) -> str:
    """
    Generic async function to call the OpenAI ChatGPT API with a prompt.
    Returns the raw response as a string.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM call failed: {e}" 