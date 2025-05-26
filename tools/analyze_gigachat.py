from dotenv import load_dotenv
from langchain_gigachat import GigaChat
from langchain.schema import HumanMessage
from tools.prompts import GIGA_CHAT_PROMPT_RU, GIGA_CHAT_PROMPT_EN
import os

load_dotenv()

def analyze_with_gigachat(image_path, lang):
    credentials = os.getenv("GIGACHAT_API_KEY")

    llm = GigaChat(
        credentials=credentials,
        verify_ssl_certs=False,
        scope="GIGACHAT_API_CORP",
        model="GigaChat-2-Max",
        temperature=0.1,
        streaming=False
    )

    if lang == "Русский язык":
        prompt = GIGA_CHAT_PROMPT_RU

    else:
        prompt = GIGA_CHAT_PROMPT_EN

    with open(image_path, "rb") as f:
        file = llm.upload_file(f)

    msg = HumanMessage(content=prompt,
                       additional_kwargs={"attachments": [file.id_]})

    result = llm.invoke([msg])
    answer = result.content

    return answer