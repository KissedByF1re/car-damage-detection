from dotenv import load_dotenv
from langchain_gigachat import GigaChat
from langchain.schema import HumanMessage
from tools.prompts import SYSTEM_PROMPT_EN, SYSTEM_PROMPT_RU, USER_PROMPT_EN, USER_PROMPT_RU
import os

load_dotenv()

def analyze_with_gigachat(image_path, lang):
    credentials = os.getenv("GIGACHAT_API_KEY")

    llm = GigaChat(
        credentials=credentials,
        verify_ssl_certs=False,
        scope="GIGACHAT_API_CORP",
        model="GigaChat-2-Max"
    )

    if lang == "Русский язык":
        system_prompt = SYSTEM_PROMPT_RU
        question = USER_PROMPT_RU
    else:
        system_prompt = SYSTEM_PROMPT_EN
        question = USER_PROMPT_EN

    with open(image_path, "rb") as f:
        file = llm.upload_file(f)

    msg = [
        HumanMessage(role="system", content=system_prompt),
        HumanMessage(role="user", content=question, additional_kwargs={"attachments": [file.id_]})
    ]
    result = llm.invoke(msg)
    return result.content