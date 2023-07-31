import requests
import os
import json

class WebSearch:
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        self.cx = os.environ.get('SEARCH_ENGINE_ID')   
        self.url_base = "https://www.googleapis.com/customsearch/v1"

    def search(self, query):
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "sort": "date",
            "num": 5
        }
    
        results = []
        response = requests.get(self.url_base, params=params)
        response.raise_for_status()
        items = response.json()["items"]
        for item in items:
            results.append({"title": item['title'], "text": item["snippet"], "link": item['link']})

        return json.dumps(results)
    
    def export_function_search(self):
        return {
            "name": "search",
            "description": "Searches the web using Google's Custom Search API, can be used to search for news, articles, updated information etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "query (str): The search query",
                    }
                },
                "required": ["query"],
            },
        }