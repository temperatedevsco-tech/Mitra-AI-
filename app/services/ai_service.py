import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

SYSTEM_PROMPT = """
You are Mitra.

A warm, intelligent and helpful AI assistant.

Keep answers friendly and concise.
"""


def generate_reply(message):

    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },

            {
                "role": "user",
                "content": message,
            },

        ],

    )

    return response.choices[0].message.content.strip()


def generate_title(first_message):

    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[

            {
                "role": "system",
                "content": """
Generate a very short chat title.

Rules:
- Maximum 5 words.
- No quotes.
- No punctuation at the end.
- Only return the title.
""",
            },

            {
                "role": "user",
                "content": first_message,
            },

        ],

    )

    return response.choices[0].message.content.strip()