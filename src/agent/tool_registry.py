"""
Tool Registry - mapping tool names to actual functions.
Ye 'lookup table' hai jo agent loop use karta hai.
"""
from src.tools.weather_tool import get_weather
from src.tools.calculator_tool import calculator
from src.tools.search_tool import web_search


# Naam → Function mapping
AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "calculator": calculator,
    "web_search": web_search,
}


def execute_tool(tool_name: str, arguments: dict) -> str:
    """
    Execute a tool by name with given arguments.
    
    Args:
        tool_name: Name of the tool (must be in AVAILABLE_TOOLS)
        arguments: Dictionary of arguments to pass to the tool
    
    Returns:
        Tool execution result as string.
    """
    if tool_name not in AVAILABLE_TOOLS:
        return f"Error: Tool '{tool_name}' not found"
    
    try:
        tool_function = AVAILABLE_TOOLS[tool_name]
        result = tool_function(**arguments)
        return str(result)
    except TypeError as e:
        return f"Invalid arguments for {tool_name}: {e}"
    except Exception as e:
        return f"Tool execution failed: {e}"