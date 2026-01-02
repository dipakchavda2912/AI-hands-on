"""
Unit tests for GitHub Agent.

Run with: pytest tests/test_github_agent.py -v
"""

import pytest
from agents.github_agent import GithubAgent
from tools.github_tools import GithubTools


@pytest.fixture
def agent():
    """Create agent fixture."""
    tools = GithubTools().get_tools()
    return GithubAgent(
        tools=tools,
        model_name="gemini-2.0-flash-exp",
        enable_checkpointing=False  # Disable for testing
    )


def test_agent_initialization(agent):
    """Test agent initializes correctly."""
    assert agent is not None
    assert agent.model_name == "gemini-2.0-flash-exp"
    assert len(agent.tools) > 0


def test_agent_run_returns_dict(agent):
    """Test agent.run returns proper dictionary."""
    result = agent.run("Hello")

    assert isinstance(result, dict)
    assert "success" in result
    assert "thread_id" in result
    assert "execution_time" in result


@pytest.mark.asyncio
async def test_agent_async_run(agent):
    """Test async execution."""
    result = await agent.run_async("Test request")

    assert isinstance(result, dict)
    assert "success" in result
    assert "output" in result or "error" in result


def test_conversation_state(agent):
    """Test conversation maintains state."""
    thread_id = "test_thread_123"

    result1 = agent.run("First message", thread_id=thread_id)
    result2 = agent.run("Second message", thread_id=thread_id)

    assert result1["thread_id"] == result2["thread_id"]
