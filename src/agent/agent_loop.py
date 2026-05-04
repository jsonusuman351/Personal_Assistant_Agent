"""
Core Agent Loop - LLM + Tool Execution + Iteration.
"""
import json
from loguru import logger
from openai import OpenAI

from src.config.settings import settings
from src.agent.tool_schemas import TOOLS_SCHEMA
from src.agent.tool_registry import execute_tool


# OpenAI client initialize
client = OpenAI(api_key=settings.OPENAI_API_KEY)


SYSTEM_PROMPT = """You are a helpful personal assistant.
You have access to tools for weather, calculations, and web search.

Rules:
- Use tools when needed to answer accurately
- Don't make up information - use web_search if unsure
- Be concise and friendly
- Reply in the same language user uses
"""


def run_agent(user_query: str, conversation_history: list = None) -> dict:
    """
    Main agent loop - takes user query, returns final answer.
    
    Args:
        user_query: User's question
        conversation_history: Previous messages (for multi-turn chat)
    
    Returns:
        Dict with 'answer' and 'tool_calls_made' for transparency.
    """
    logger.info(f"🚀 Agent started with query: {user_query}")
    
    # Initialize messages
    if conversation_history is None:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    else:
        messages = conversation_history.copy()
    
    messages.append({"role": "user", "content": user_query})
    
    tool_calls_made = []
    
    # AGENT LOOP - max iterations to prevent infinite loop
    for iteration in range(settings.MAX_ITERATIONS):
        logger.info(f"--- Iteration {iteration + 1} ---")
        
        # Step 1: LLM call
        try:
            response = client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                temperature=settings.TEMPERATURE,
            )
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return {"answer": f"LLM error: {e}", "tool_calls_made": tool_calls_made}
        
        response_message = response.choices[0].message
        
        # Properly format the message for next iteration
        formatted_message = {
            "role": "assistant",
            "content": response_message.content
        }
        if response_message.tool_calls:
            formatted_message["tool_calls"] = response_message.tool_calls
        
        messages.append(formatted_message)
        
        # Step 2: Check if LLM wants to use tools
        if response_message.tool_calls:
            logger.info(f"🔧 LLM requested {len(response_message.tool_calls)} tool(s)")
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"   → Calling {function_name}({function_args})")
                
                # Execute tool
                result = execute_tool(function_name, function_args)
                
                logger.info(f"   ← Result: {result[:100]}...")
                
                tool_calls_made.append({
                    "tool": function_name,
                    "args": function_args,
                    "result": result[:200]  # Truncate for logging
                })
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        
        else:
            # Step 3: Final answer ready
            logger.info("✅ Final answer generated")
            return {
                "answer": response_message.content,
                "tool_calls_made": tool_calls_made,
                "iterations": iteration + 1
            }
    
    # Max iterations reached
    logger.warning("⚠️ Max iterations reached without final answer")
    return {
        "answer": "Sorry, couldn't complete the task in time.",
        "tool_calls_made": tool_calls_made,
        "iterations": settings.MAX_ITERATIONS
    }