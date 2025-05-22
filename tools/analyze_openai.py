import openai
import base64
import os
from dotenv import load_dotenv
from tools.prompts import SYSTEM_PROMPT_EN, SYSTEM_PROMPT_RU, USER_PROMPT_EN, USER_PROMPT_RU

load_dotenv()

def analyze_with_openai(image_path,lang):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()

    base64_image = base64.b64encode(image_bytes).decode()

    if lang == "Русский язык":
        system_prompt = SYSTEM_PROMPT_RU
        question = USER_PROMPT_RU
    else:
        system_prompt = SYSTEM_PROMPT_EN
        question = USER_PROMPT_EN

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content