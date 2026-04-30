import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# We only initialize the client if GROQ_API_KEY is available to avoid crash if people don't use Groq
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

def generate_answer(system_prompt: str, user_prompt: str) -> str:
    if not client:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content

def generate_text(prompt: str) -> str:
    """Useful for generic prompts like query rewriting without a system prompt."""
    if not client:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=200
    )

    return response.choices[0].message.content
