"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatRequest(BaseModel):
    """User input to the agent."""
    query: str = Field(..., min_length=1, max_length=1000, description="User question")
    conversation_history: Optional[List[Dict[str, Any]]] = None


class ToolCallInfo(BaseModel):
    """Info about each tool call made."""
    tool: str
    args: Dict[str, Any]
    result: str


class ChatResponse(BaseModel):
    """Agent's response."""
    answer: str
    tool_calls_made: List[ToolCallInfo]
    iterations: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str