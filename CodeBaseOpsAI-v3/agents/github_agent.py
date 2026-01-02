"""
Production-grade GitHub Agent using LangGraph.

Features:
- State management with checkpointing
- Streaming responses
- Error handling and retries
- Observability and logging
- Async support for scalability
"""

import logging
from typing import Any, Dict, Optional, AsyncIterator
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GithubAgent:
    """
    Production-grade GitHub operations agent.

    Uses LangGraph for state management and modern agent orchestration.
    Supports streaming, checkpointing, and graceful error handling.
    """

    def __init__(
        self,
        tools: list,
        model_name: str = "gemini-2.0-flash-exp",
        temperature: float = 0.0,
        enable_checkpointing: bool = True
    ):
        """
        Initialize the GitHub agent.

        Args:
            tools: List of LangChain tools for GitHub operations
            model_name: Name of the LLM model to use
            temperature: Temperature for model responses (0.0 = deterministic)
            enable_checkpointing: Enable state persistence for resume capability
        """
        self.tools = tools
        self.model_name = model_name

        # Initialize the language model with production settings
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            max_retries=3,  # Auto-retry on failures
            timeout=60.0,   # 60 second timeout
        )

        # Initialize checkpointer for state management
        self.checkpointer = MemorySaver() if enable_checkpointing else None

        # Create the LangGraph agent
        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            checkpointer=self.checkpointer,
        )

        logger.info(
            f"Initialized GithubAgent with model={model_name}, checkpointing={enable_checkpointing}")

    async def run_async(
        self,
        user_request: str,
        thread_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute agent asynchronously (production-grade for concurrent requests).

        Args:
            user_request: The user's request
            thread_id: Optional thread ID for conversation continuity
            metadata: Additional metadata for tracking

        Returns:
            Dict containing the result and metadata
        """
        start_time = datetime.utcnow()
        thread_id = thread_id or f"thread_{start_time.timestamp()}"

        try:
            logger.info(
                f"[{thread_id}] Starting async execution: {user_request[:100]}...")

            config = RunnableConfig(
                configurable={"thread_id": thread_id},
                metadata=metadata or {}
            )

            # Execute the agent
            result = await self.agent.ainvoke(
                {"messages": [HumanMessage(content=user_request)]},
                config=config
            )

            # Extract the final response
            final_message = result["messages"][-1]
            output = final_message.content if hasattr(
                final_message, 'content') else str(final_message)

            execution_time = (datetime.utcnow() - start_time).total_seconds()

            logger.info(f"[{thread_id}] Completed in {execution_time:.2f}s")

            return {
                "success": True,
                "output": output,
                "thread_id": thread_id,
                "execution_time": execution_time,
                "timestamp": start_time.isoformat(),
                "messages": result["messages"]
            }

        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            logger.error(
                f"[{thread_id}] Failed after {execution_time:.2f}s: {str(e)}", exc_info=True)

            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "thread_id": thread_id,
                "execution_time": execution_time,
                "timestamp": start_time.isoformat()
            }

    def run(
        self,
        user_request: str,
        thread_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute agent synchronously (backward compatible).

        Args:
            user_request: The user's request
            thread_id: Optional thread ID for conversation continuity
            metadata: Additional metadata for tracking

        Returns:
            Dict containing the result and metadata
        """
        start_time = datetime.utcnow()
        thread_id = thread_id or f"thread_{start_time.timestamp()}"

        try:
            logger.info(
                f"[{thread_id}] Starting execution: {user_request[:100]}...")

            config = RunnableConfig(
                configurable={"thread_id": thread_id},
                metadata=metadata or {}
            )

            # Execute the agent
            result = self.agent.invoke(
                {"messages": [HumanMessage(content=user_request)]},
                config=config
            )

            # Extract the final response
            final_message = result["messages"][-1]
            output = final_message.content if hasattr(
                final_message, 'content') else str(final_message)

            execution_time = (datetime.utcnow() - start_time).total_seconds()

            logger.info(f"[{thread_id}] Completed in {execution_time:.2f}s")

            return {
                "success": True,
                "output": output,
                "thread_id": thread_id,
                "execution_time": execution_time,
                "timestamp": start_time.isoformat(),
                "messages": result["messages"]
            }

        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            logger.error(
                f"[{thread_id}] Failed after {execution_time:.2f}s: {str(e)}", exc_info=True)

            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "thread_id": thread_id,
                "execution_time": execution_time,
                "timestamp": start_time.isoformat()
            }

    async def stream(
        self,
        user_request: str,
        thread_id: Optional[str] = None
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Stream agent responses in real-time (production UX).

        Args:
            user_request: The user's request
            thread_id: Optional thread ID for conversation continuity

        Yields:
            Dict chunks containing incremental responses
        """
        thread_id = thread_id or f"thread_{datetime.utcnow().timestamp()}"

        try:
            logger.info(
                f"[{thread_id}] Starting stream: {user_request[:100]}...")

            config = RunnableConfig(
                configurable={"thread_id": thread_id}
            )

            async for chunk in self.agent.astream(
                {"messages": [HumanMessage(content=user_request)]},
                config=config
            ):
                yield {
                    "type": "chunk",
                    "data": chunk,
                    "thread_id": thread_id
                }

        except Exception as e:
            logger.error(
                f"[{thread_id}] Stream error: {str(e)}", exc_info=True)
            yield {
                "type": "error",
                "error": str(e),
                "thread_id": thread_id
            }
