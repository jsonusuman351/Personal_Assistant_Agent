"""
FastAPI application - REST API for agent.
Run: uvicorn src.api.main:app --reload
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from src.config.settings import settings
from src.agent.agent_loop import run_agent
from src.api.models import ChatRequest, ChatResponse, HealthResponse


# Logger setup
logger.remove()
logger.add(sys.stdout, level=settings.LOG_LEVEL)
logger.add("logs/agent.log", rotation="10 MB", level="DEBUG")


# Validate settings on startup
try:
    settings.validate()
    logger.info("✅ All API keys loaded")
except ValueError as e:
    logger.error(f"❌ {e}")
    sys.exit(1)


# FastAPI app
app = FastAPI(
    title="Personal Assistant Agent API",
    description="AI agent with weather, calculator, and web search",
    version="1.0.0"
)

# CORS - browser se call karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production me specific domain do
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return HealthResponse(status="ok", message="Agent API is running")


@app.get("/health", response_model=HealthResponse)
async def health():
    """Detailed health check."""
    return HealthResponse(status="healthy", message="All systems operational")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - takes user query, returns agent response.
    """
    logger.info(f"📨 New request: {request.query}")
    
    try:
        result = run_agent(
            user_query=request.query,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            answer=result["answer"],
            tool_calls_made=result["tool_calls_made"],
            iterations=result["iterations"]
        )
    
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))