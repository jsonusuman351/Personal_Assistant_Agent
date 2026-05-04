"""
Web Search Tool - Tavily API se internet search.
"""
import requests
from src.config.settings import settings


def web_search(query: str, max_results: int = 3) -> str:
    """
    Search the web using Tavily API.
    
    Args:
        query: Search query
        max_results: Number of top results to return
    
    Returns:
        Formatted string with search results.
    """
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": settings.TAVILY_API_KEY,
            "query": query,
            "max_results": max_results,
            "search_depth": "basic"
        }
        
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            return f"No results found for: {query}"
        
        # Format results
        formatted = f"Search results for '{query}':\n\n"
        for i, result in enumerate(results[:max_results], 1):
            title = result.get("title", "No title")
            content = result.get("content", "")[:200]  # First 200 chars
            url_link = result.get("url", "")
            formatted += f"{i}. {title}\n   {content}...\n   Source: {url_link}\n\n"
        
        return formatted
    
    except requests.exceptions.RequestException as e:
        return f"Search failed: {e}"