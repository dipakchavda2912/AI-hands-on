"""
CodeBaseOpsAI - Simple GitHub Agent Example

This demonstrates a basic ReAct agent that can perform GitHub operations.
"""

from dotenv import load_dotenv
from tools.github_tools import GithubTools
from agents.github_agent import GithubAgent

# Load environment variables
load_dotenv()


def main():
    """Main function to run the GitHub agent."""
    print("=== CodeBaseOpsAI GitHub Agent ===\n")

    # Initialize tools and agent
    github_tools = GithubTools()
    tools = github_tools.get_tools()

    agent = GithubAgent(
        tools=tools,
        model_name="gemini-2.0-flash-exp"
    )

    # Example request
    user_request = """
    Read the repository 'dipakchavda2912/base-serverless' on branch 'develop'.
    Analyze the files and provide a summary.
    """

    print("User Request:")
    print(user_request)
    print("\nAgent Response:\n")

    # Run the agent
    result = agent.run(user_request=user_request)

    print("\n" + "="*60)
    print("Result:")
    print(result)
    print("="*60)


if __name__ == "__main__":
    main()
