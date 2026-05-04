"""
OpenAI function calling schemas.
LLM padhke decide karta hai kab kaunsa tool use karna hai.
Description achhi likhna - yahi LLM ke liye 'documentation' hai.
"""

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": (
                "Get current weather information for a specific city. "
                "Use this when user asks about temperature, weather conditions, "
                "humidity, or climate of any city."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city, e.g., 'Mumbai', 'New York'"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Perform mathematical calculations. "
                "Use for arithmetic operations like addition, subtraction, "
                "multiplication, division, percentage, or power."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression like '25 * 4' or '(10+5)/3'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the internet for current information, news, facts, "
                "or any data that requires real-time lookup. Use when you don't "
                "know the answer or need recent information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query keywords"
                    }
                },
                "required": ["query"]
            }
        }
    }
]