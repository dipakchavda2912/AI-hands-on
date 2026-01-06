"""Quick test without GitHub API"""
from src.agent import Agent

# Test just the clone functionality (doesn't need GitHub token)
agent = Agent()
executor = agent.get_agent_executor()

query = "Clone the repository 'https://github.com/torvalds/linux.git' to /tmp/test-clone"

print(f"Query: {query}\n")
try:
    response = executor.invoke({"messages": [{"role": "user", "content": query}]})
    if response and "messages" in response:
        last_message = response["messages"][-1]
        result = last_message.content if hasattr(last_message, 'content') else str(last_message)
        print(f"✓ Result: {result}")
except Exception as e:
    print(f"✗ Error: {str(e)}")
