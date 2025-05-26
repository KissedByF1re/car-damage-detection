import os
from dotenv import load_dotenv
import openai
from langchain_gigachat import GigaChat
from langchain.schema import HumanMessage
from tools.find_links import web_search

load_dotenv()

def find_repair_services(model: str, city: str) -> str:
    search_results = web_search(query=f"Автосервисы {city}", num_results=5)
    context = "\n".join([f"{res['title']}: {res['link']}" for res in search_results])

    prompt = f"""
                Ты — помощник по ремонту автомобилей и отбору ссылок. Выбери наиболее релевантные ссылки из результатов поиска автосервисов в городе {city}. 
                Для каждого источника укажи:
                - Название источника
                - Ссылка на источник

                Ответ должен быть структурирован как нумерованный список.

                Верни результат в формате markdown. Результаты поиска: {context}
                """

    if model == "GigaChat-2-Max":
        credentials = os.getenv("GIGACHAT_API_KEY")

        llm = GigaChat(
            credentials=credentials,
            verify_ssl_certs=False,
            scope="GIGACHAT_API_CORP",
            model="GigaChat-2-Max",
            temperature=0,
            streaming=False
        )

        msg = HumanMessage(content=prompt)
        result = llm.invoke([msg])
        answer = result.content

        return answer

    elif model == "GPT-4o":
        openai.api_key = os.getenv("OPENAI_API_KEY")

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        answer = response.choices[0].message.content

        return answer