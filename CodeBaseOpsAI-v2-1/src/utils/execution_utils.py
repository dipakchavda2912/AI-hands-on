"""
Utility functions for agent execution management
"""

from typing import Dict, List, Any, Tuple


class ExecutionUtils:
    """Utilities for managing agent execution flow"""

    @staticmethod
    def get_current_datetime_string() -> str:
        """Get current date and time as a formatted string.

        Returns:
            String in format YYYYMMDD-HHMMSS
        """
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    @staticmethod
    def initialize_execution_state() -> Dict[str, int]:
        """Initialize execution state tracking dictionary.

        Returns:
            Dict with counters for total, successful, failed, and skipped operations
        """
        return {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0
        }

    @staticmethod
    def get_critical_operations() -> List[str]:
        """Get list of critical operation keywords.

        Operations containing these keywords will stop execution if they fail.

        Returns:
            List of critical operation keywords
        """
        return [
            "clone",
            "checkout",
            "load",
            "create a `custom` key"
        ]

    @staticmethod
    def extract_response_text(response: Dict[str, Any]) -> Tuple[str, bool]:
        """Extract text content from agent response.

        Args:
            response: Agent response dictionary

        Returns:
            Tuple of (extracted_text, success_flag)
        """
        try:
            if not response or "messages" not in response:
                return "No response received", False

            last_message = response["messages"][-1]
            result = last_message.content if hasattr(
                last_message, 'content') else str(last_message)

            # Extract text from result if it's a list of message parts
            if isinstance(result, list):
                # Extract text from all parts
                text_parts = [
                    part.get('text', str(part))
                    for part in result
                    if isinstance(part, dict)
                ]
                result_text = ' '.join(text_parts)
            else:
                result_text = str(result)

            return result_text, True

        except Exception as e:
            return f"Error extracting response: {str(e)}", False

    @staticmethod
    def is_critical_operation(query: str, critical_operations: List[str]) -> bool:
        """Check if a query represents a critical operation.

        Args:
            query: The query string to check
            critical_operations: List of critical operation keywords

        Returns:
            True if query contains any critical operation keyword
        """
        return any(keyword in query.lower() for keyword in critical_operations)

    @staticmethod
    def has_failure_indicators(text: str) -> bool:
        """Check if text contains failure indicators.

        Args:
            text: Text to check for failure keywords

        Returns:
            True if text contains 'error' or 'failed'
        """
        text_lower = text.lower()
        return "error" in text_lower or "failed" in text_lower

    @staticmethod
    def print_query_header(idx: int, total: int, query: str, max_length: int = 100) -> None:
        """Print formatted query header.

        Args:
            idx: Current query index (1-based)
            total: Total number of queries
            query: Query text
            max_length: Maximum length to display before truncating
        """
        print(f"\n{'=' * 60}")
        if len(query) > max_length:
            print(f"Query {idx}/{total}: {query[:max_length]}...")
        else:
            print(f"Query {idx}/{total}: {query}")
        print(f"{'=' * 60}")

    @staticmethod
    def print_execution_summary(total_queries: int, execution_state: Dict[str, int]) -> None:
        """Print execution summary with statistics.

        Args:
            total_queries: Total number of queries in the list
            execution_state: Execution state dictionary with counters
        """
        print(f"\n{'=' * 60}")
        print("Execution Summary:")
        print(f"{'=' * 60}")
        print(f"Total queries: {total_queries}")
        print(f"Executed: {execution_state['total']}")
        print(f"Successful: {execution_state['successful']}")
        print(f"Failed: {execution_state['failed']}")
        print(f"Skipped: {execution_state['skipped']}")
        print(f"{'=' * 60}")

    @staticmethod
    def should_stop_execution(
        is_critical: bool,
        result_text: str,
        execution_state: Dict[str, int]
    ) -> bool:
        """Determine if execution should stop due to critical failure.

        Args:
            is_critical: Whether the operation is critical
            result_text: Result text to check for failures
            execution_state: Execution state dictionary to update

        Returns:
            True if execution should stop
        """
        if is_critical and ExecutionUtils.has_failure_indicators(result_text):
            print(
                f"\n⚠️  CRITICAL ERROR: A critical operation failed. Stopping execution.")
            execution_state["failed"] += 1
            return True
        return False

    @staticmethod
    def handle_exception(
        exception: Exception,
        query: str,
        critical_operations: List[str],
        execution_state: Dict[str, int]
    ) -> bool:
        """Handle exception during query execution.

        Args:
            exception: The exception that occurred
            query: The query that caused the exception
            critical_operations: List of critical operation keywords
            execution_state: Execution state dictionary to update

        Returns:
            True if execution should stop
        """
        print(f"\n✗ Error: {str(exception)}")
        import traceback
        traceback.print_exc()

        execution_state["failed"] += 1

        # Check if this is a critical operation
        is_critical = ExecutionUtils.is_critical_operation(
            query, critical_operations)
        if is_critical:
            print(
                f"\n⚠️  CRITICAL ERROR: Stopping execution due to failure in critical operation.")
            return True
        return False
