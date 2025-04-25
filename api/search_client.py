import os
import requests
from api.openai_client import OpenAIClient

class SearchClient:
    def __init__(self):
        self.api_key = os.getenv("SEARCH_API_KEY")
        self.search_engine_id = os.getenv("SEARCH_ENGINE_ID")
        self.openai_client = OpenAIClient()
        
    def search(self, query, num_results=5):
        """Search the web using Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num_results
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Search API error: {response.status_code}")
            
        results = response.json()
        
        # Extract relevant information
        search_results = []
        if "items" in results:
            for item in results["items"]:
                search_results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "url": item.get("link", "")
                })
                
        return search_results
        
    def summarize(self, search_results, query):
        """Summarize search results using OpenAI"""
        # Format search results for the prompt
        formatted_results = ""
        for i, result in enumerate(search_results):
            formatted_results += f"Result {i+1}:\nTitle: {result['title']}\nSnippet: {result['snippet']}\nURL: {result['url']}\n\n"
        
        # Create a prompt for summarization
        prompt = f"I searched for '{query}' and got these results:\n\n{formatted_results}\n\nPlease provide a comprehensive summary of this information, addressing the original query."
        
        # Use OpenAI to summarize
        summary = self.openai_client.generate_response(prompt)
        
        return summary
