"""
CodeBaseOpsAI - Simple GitHub Agent Example

This demonstrates a basic ReAct agent that can perform GitHub operations.
"""

import os
from typing import List
from dotenv import load_dotenv
from src.agent import Agent
from src.services.instruction_service import InstructionService
from src.utils.execution_utils import ExecutionUtils

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
        parent_folder_name = f"base-serverless-{ExecutionUtils.get_current_datetime_string()}"
        clone_path = f"/tmp/{parent_folder_name}/base-serverless-clone/"
        branch = "develop"
        node_lts_version = '22.11.0'

        # Use instruction service to get all instructions
        instruction_service = InstructionService(
            repository=source_repository,
            clone_path=clone_path,
            branch=branch,
            node_lts_version=node_lts_version
        )

        return instruction_service.get_all_instructions()

    def execute(self):
        """Execute all agent queries with error handling and progress tracking."""
        executor = self.agent_instance.get_agent_executor()

        # Safety check
        if executor is None:
            print("\n❌ Error: Agent executor is not initialized.")
            return

        queries = self.get_query()

        # Initialize execution tracking
        execution_state = ExecutionUtils.initialize_execution_state()
        critical_operations = ExecutionUtils.get_critical_operations()

        # Run each query
        for idx, query in enumerate(queries, 1):
            # Skip empty queries
            if not query or not query.strip():
                execution_state["skipped"] += 1
                continue

            execution_state["total"] += 1
            ExecutionUtils.print_query_header(idx, len(queries), query)

            try:
                # Execute query
                response = executor.invoke(
                    {"messages": [{"role": "user", "content": query}]})

                # Process response
                if self._process_query_response(
                    response, query, critical_operations, execution_state
                ):
                    break  # Stop execution on critical failure

            except Exception as e:
                # Handle exception
                if ExecutionUtils.handle_exception(
                    e, query, critical_operations, execution_state
                ):
                    break  # Stop execution on critical exception

        # Print final summary
        ExecutionUtils.print_execution_summary(len(queries), execution_state)

    def _process_query_response(
        self,
        response: dict,
        query: str,
        critical_operations: List[str],
        execution_state: dict
    ) -> bool:
        """Process query response and check for critical failures.

        Args:
            response: Agent response dictionary
            query: Original query string
            critical_operations: List of critical operation keywords
            execution_state: Execution state dictionary

        Returns:
            True if execution should stop, False otherwise
        """
        # Extract response text
        result_text, success = ExecutionUtils.extract_response_text(response)

        if success:
            print(f"\n✓ Result: {result_text}")

            # Check if critical operation failed
            is_critical = ExecutionUtils.is_critical_operation(
                query, critical_operations)

            if ExecutionUtils.should_stop_execution(
                is_critical, result_text, execution_state
            ):
                return True  # Stop execution

            execution_state["successful"] += 1
        else:
            print(f"\n✓ Response: {response}")
            execution_state["successful"] += 1

        return False  # Continue execution


if __name__ == "__main__":
    main = Main()
    main.execute()
