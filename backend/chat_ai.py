import os
from openai import OpenAI
import dotenv
dotenv.load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_reply(prompt):
    """Genereer een tekst-antwoord via ChatGPT"""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a friendly digital human that speaks naturally."},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content
