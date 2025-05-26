import requests
from dotenv import load_dotenv
import os

load_dotenv()

def web_search(query, num_results=10):
    """
    Выполняет поиск в кастомном поисковике Google и возвращает список результатов.
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    cse_id = os.getenv('CSE_ID')

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": num_results
    }
    response = requests.get(url, params=params)
    results = response.json().get("items", [])
    search_results = []
    for item in results:
        title = item.get("title")
        link = item.get("link")
        snippet = item.get("snippet")
        search_results.append({
            "title": title,
            "link": link,
            "snippet": snippet
        })
    return search_results