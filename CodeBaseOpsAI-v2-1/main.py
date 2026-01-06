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
        source_repository = "dipakchavda2912/base-serverless"
        clone_path = "/tmp/base-serverless-clone/"
        branch = "develop"
        return [
            f"Read the repository '{source_repository}' on branch '{branch}'.",

            f"Clone the repository '{source_repository}' to local filesystem at {clone_path}",

            f"Checkout the '{branch}' branch in the cloned repository at {clone_path}.",

            f"List all the files in the cloned repository at {clone_path} on branch {branch}",

            f"Load the {clone_path}serverless.yml file from the local filesystem path {clone_path} and parse it.",

            f"Create a `custom` key in the {clone_path}serverless.yml file if it does not already exist.",

            f"""Add AWS account ID mappings under the 'custom' key.
            beginning: '# AWS account Id Map that would be used as a map for forming urns.'
            For environments dev, qa, uat, uatdr: use AWS account ID 1234567890
            For environments prod, dr: use AWS account ID 0987654321
            Use the pattern '<env>-account-id: <account-id>' for each environment (e.g., dev-account-id: 1234567890).
            Update the {clone_path}serverless.yml file with these mappings.""",

            f"""Add AWS region mappings under the 'custom' key.
            beginning: '# AWS Region Map for deployment of lambda functions.'
            For environments dev, qa, uat, dr: use AWS region us-west-2
            For environments uatdr, prod: use AWS region us-east-1
            Use the pattern '<env>-region: <aws-region-name>' for each environment (e.g., dev-region: us-west-2).
            Update the {clone_path}serverless.yml file with these mappings."""
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
