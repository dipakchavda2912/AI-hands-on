"""
Production API Server using FastAPI.

This demonstrates how to deploy your agent as a REST API service.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import asyncio
import logging
from datetime import datetime
import json

from tools.github_tools import GithubTools
from agents.github_agent import GithubAgent

# Initialize FastAPI app
app = FastAPI(
    title="CodeBaseOpsAI API",
    description="Production GitHub operations agent API",
    version="3.0.0"
)

# Initialize agent (singleton pattern)
tools = GithubTools().get_tools()
agent = GithubAgent(
    tools=tools,
    model_name="gemini-2.0-flash-exp",
    enable_checkpointing=True
)

logger = logging.getLogger(__name__)


# Request/Response Models
class AgentRequest(BaseModel):
    """Request model for agent execution."""
    request: str = Field(
        description="The user's request to the agent",
        min_length=1,
        max_length=2000
    )
    thread_id: Optional[str] = Field(
        default=None,
        description="Optional thread ID for conversation continuity"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata for tracking"
    )


class AgentResponse(BaseModel):
    """Response model for agent execution."""
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    thread_id: str
    execution_time: float
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str


# API Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for load balancers."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "3.0.0"
    }


@app.post("/agent/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    Execute agent request asynchronously.

    Example:
    ```
    POST /agent/run
    {
        "request": "Clone repo dipakchavda2912/base-serverless",
        "thread_id": "user_123_session",
        "metadata": {"user_id": "123"}
    }
    ```
    """
    try:
        result = await agent.run_async(
            user_request=request.request,
            thread_id=request.thread_id,
            metadata=request.metadata
        )

        return AgentResponse(**result)

    except Exception as e:
        logger.error(f"API error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/stream")
async def stream_agent(request: AgentRequest):
    """
    Stream agent responses in real-time using Server-Sent Events (SSE).

    Example:
    ```
    POST /agent/stream
    {
        "request": "Read repository and analyze files"
    }
    ```

    Returns SSE stream with incremental updates.
    """
    async def event_generator():
        """Generate SSE events from agent stream."""
        try:
            async for chunk in agent.stream(
                user_request=request.request,
                thread_id=request.thread_id
            ):
                # Format as SSE
                data = json.dumps(chunk)
                yield f"data: {data}\n\n"

        except Exception as e:
            error_data = json.dumps({
                "type": "error",
                "error": str(e)
            })
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@app.post("/agent/background")
async def run_agent_background(
    request: AgentRequest,
    background_tasks: BackgroundTasks
):
    """
    Execute agent in background (fire-and-forget).

    Useful for long-running operations that don't need immediate response.
    Returns immediately with a task ID.
    """
    task_id = f"task_{datetime.utcnow().timestamp()}"

    async def background_execution():
        """Execute agent in background."""
        try:
            result = await agent.run_async(
                user_request=request.request,
                thread_id=request.thread_id or task_id,
                metadata=request.metadata
            )

            # In production: Store result in database or cache
            logger.info(f"Background task {task_id} completed: {result}")

        except Exception as e:
            logger.error(
                f"Background task {task_id} failed: {e}", exc_info=True)

    background_tasks.add_task(background_execution)

    return {
        "task_id": task_id,
        "status": "queued",
        "message": "Task queued for execution"
    }


# Middleware for logging and monitoring
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests with timing."""
    start_time = datetime.utcnow()

    # Process request
    response = await call_next(request)

    # Log request details
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"time={execution_time:.3f}s"
    )

    return response


# Startup/Shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting CodeBaseOpsAI API server...")
    logger.info("Agent initialized and ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down CodeBaseOpsAI API server...")


if __name__ == "__main__":
    import uvicorn

    # Run the API server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only)
        workers=4,    # Number of worker processes
        log_level="info"
    )
