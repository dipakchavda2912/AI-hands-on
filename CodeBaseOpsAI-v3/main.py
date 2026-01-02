"""
Production-grade CodeBaseOpsAI application.

Features:
- Async support for scalability
- Proper error handling
- Structured logging
- Configuration management
- Graceful shutdown
"""

import asyncio
import json
import sys
from typing import Optional
from dotenv import load_dotenv

from tools.github_tools import GithubTools
from agents.github_agent import GithubAgent

# Load environment variables
load_dotenv()


def example_sync():
    """Example: Synchronous execution (backward compatible)."""
    print("=== Synchronous Execution Example ===\n")

    # Initialize tools and agent
    github_tools = GithubTools()
    tools = github_tools.get_tools()

    agent = GithubAgent(
        tools=tools,
        model_name="gemini-2.0-flash-exp",
        temperature=0.0,
        enable_checkpointing=True
    )

    # Execute request
    user_request = """
    Read the repository 'dipakchavda2912/base-serverless' on branch 'develop'.
    Analyze all .js, .ts, .json, .yml, and .md files.
    Return a JSON array with objects containing 'file', 'content', and 'sha' keys.
    """

    result = agent.run(user_request=user_request)

    # Display results
    print(f"\n{'='*60}")
    print(f"Success: {result['success']}")
    print(f"Execution Time: {result['execution_time']:.2f}s")
    print(f"Thread ID: {result['thread_id']}")

    if result['success']:
        print(f"\nOutput:\n{result['output']}")
    else:
        print(f"\nError: {result['error']}")

    return result


async def example_async():
    """Example: Asynchronous execution (production-grade)."""
    print("\n\n=== Asynchronous Execution Example ===\n")

    # Initialize tools and agent
    github_tools = GithubTools()
    tools = github_tools.get_tools()

    agent = GithubAgent(
        tools=tools,
        model_name="gemini-2.0-flash-exp",
        temperature=0.0,
        enable_checkpointing=True
    )

    # Execute request asynchronously
    user_request = """
    Clone the repository 'dipakchavda2912/base-serverless' to '/tmp/test-repo'.
    """

    result = await agent.run_async(
        user_request=user_request,
        metadata={"user_id": "demo_user", "session_id": "demo_session"}
    )

    # Display results
    print(f"\n{'='*60}")
    print(f"Success: {result['success']}")
    print(f"Execution Time: {result['execution_time']:.2f}s")
    print(f"Thread ID: {result['thread_id']}")

    if result['success']:
        print(f"\nOutput:\n{result['output']}")
    else:
        print(f"\nError: {result['error']}")

    return result


async def example_streaming():
    """Example: Streaming responses (real-time UX)."""
    print("\n\n=== Streaming Execution Example ===\n")

    # Initialize tools and agent
    github_tools = GithubTools()
    tools = github_tools.get_tools()

    agent = GithubAgent(
        tools=tools,
        model_name="gemini-2.0-flash-exp",
        temperature=0.0,
        enable_checkpointing=True
    )

    user_request = "Read the repository 'dipakchavda2912/base-serverless'"

    print(f"Streaming response for: {user_request}\n")
    print("Stream chunks:")
    print("-" * 60)

    chunk_count = 0
    async for chunk in agent.stream(user_request):
        chunk_count += 1
        if chunk["type"] == "chunk":
            print(f"Chunk {chunk_count}: {chunk['data']}")
        elif chunk["type"] == "error":
            print(f"Error: {chunk['error']}")

    print("-" * 60)
    print(f"Total chunks received: {chunk_count}")


async def example_conversation():
    """Example: Multi-turn conversation with state management."""
    print("\n\n=== Conversation with State Management Example ===\n")

    # Initialize tools and agent
    github_tools = GithubTools()
    tools = github_tools.get_tools()

    agent = GithubAgent(
        tools=tools,
        model_name="gemini-2.0-flash-exp",
        temperature=0.0,
        enable_checkpointing=True  # Enable state persistence
    )

    # Use same thread_id for conversation continuity
    thread_id = "conversation_demo_123"

    # First request
    result1 = await agent.run_async(
        user_request="Clone the repository 'dipakchavda2912/base-serverless'",
        thread_id=thread_id
    )
    print(f"Turn 1: {result1['output'][:200]}...")

    # Second request (maintains context)
    result2 = await agent.run_async(
        user_request="Now read all the files in that repository",
        thread_id=thread_id  # Same thread = maintains context
    )
    print(f"\nTurn 2: {result2['output'][:200]}...")


def main():
    """Main entry point with example usage patterns."""
    print("CodeBaseOpsAI v3 - Production Grade Application")
    print("=" * 60)

    # Run examples
    try:
        # Synchronous example
        example_sync()

        # Asynchronous examples
        asyncio.run(example_async())
        # asyncio.run(example_streaming())
        # asyncio.run(example_conversation())

    except KeyboardInterrupt:
        print("\n\nGraceful shutdown...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
