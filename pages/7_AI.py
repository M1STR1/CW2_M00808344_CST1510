# Simple OpenAI wrapper - requires OPENAI_API_KEY env var
import os
import openai


OPENAI_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY


def summarise_text(prompt: str):
    if not OPENAI_KEY:
        return "OpenAI API key not set. Set OPENAI_API_KEY to use AI features."
    resp = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return resp['choices'][0]['message']['content'].strip()