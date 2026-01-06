"""
CodeBaseOpsAI - Simple GitHub Agent Example

This demonstrates a basic ReAct agent that can perform GitHub operations.
"""

import os
from typing import List
from dotenv import load_dotenv
from src.agent import Agent

load_dotenv()


class Main():
    tools = None
    agent_prompt = None
    agent = None
    agent_executor = None

    def __init__(self):
        self.agent_instance = Agent()
        pass

    def get_query(self) -> List[str]:
        common_queries = """dev, qa, uat, uatdr, prod, dr are the environments used in the serverless.yml. """
        return [
            "Read the repository 'dipakchavda2912/base-serverless' on branch 'develop'.",
            "Clone the repository 'dipakchavda2912/base-serverless' to local filesystem at /tmp/base-serverless-clone/",
            "Checkout the 'develop' branch in the cloned repository at /tmp/base-serverless-clone/.",
            "List all the files in the cloned repository at /tmp/base-serverless-clone/.",
            "Load the /tmp/base-serverless-clone/serverless.yml file from the local filesystem path /tmp/base-serverless-clone/ and parse it.",
            """Generate custom attributes for /tmp/base-serverless-clone/serverless.yml environments. Environments: dev, qa, uat, uatdr use AWS account ID 1234567890. Environments: prod, dr use AWS account ID 0987654321. Use pattern '<env>-account-id: <account-id>' for each environment. Update the serverless.yml file accordingly."""
        ]

    def execute(self):
        executor = self.agent_instance.get_agent_executor()
        queries = self.get_query()

        # Run each query
        for idx, query in enumerate(queries, 1):
            # Skip empty queries
            if not query or not query.strip():
                continue

            print(f"\n{'=' * 60}")
            print(f"Query {idx}: {query}")
            print(f"{'=' * 60}")

            try:
                # New create_agent API uses messages format
                response = executor.invoke(
                    {"messages": [{"role": "user", "content": query}]})

                # Extract the response from messages
                if response and "messages" in response:
                    last_message = response["messages"][-1]
                    result = last_message.content if hasattr(
                        last_message, 'content') else str(last_message)
                    print(f"\n✓ Result: {result}")
                else:
                    print(f"\n✓ Response: {response}")
            except Exception as e:
                print(f"\n✗ Error: {str(e)}")
                import traceback
                traceback.print_exc()

        print(f"\n{'=' * 60}")
        print("Example completed!")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    main = Main()
    main.execute()
