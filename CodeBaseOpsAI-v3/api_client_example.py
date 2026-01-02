"""
Example API client demonstrating how to use the CodeBaseOpsAI API.
"""

import requests
import json
from typing import Dict, Any
import sseclient  # pip install sseclient-py


class CodeBaseOpsAIClient:
    """Client for CodeBaseOpsAI API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def run_agent(
        self,
        request: str,
        thread_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute agent synchronously."""
        payload = {
            "request": request,
            "thread_id": thread_id,
            "metadata": metadata
        }

        response = requests.post(
            f"{self.base_url}/agent/run",
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def stream_agent(self, request: str):
        """Stream agent responses in real-time."""
        payload = {"request": request}

        response = requests.post(
            f"{self.base_url}/agent/stream",
            json=payload,
            stream=True
        )
        response.raise_for_status()

        client = sseclient.SSEClient(response)
        for event in client.events():
            yield json.loads(event.data)

    def run_background(
        self,
        request: str,
        thread_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Queue agent execution in background."""
        payload = {
            "request": request,
            "thread_id": thread_id,
            "metadata": metadata
        }

        response = requests.post(
            f"{self.base_url}/agent/background",
            json=payload
        )
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    client = CodeBaseOpsAIClient()

    # 1. Health check
    print("Health Check:")
    health = client.health_check()
    print(f"Status: {health['status']}\n")

    # 2. Synchronous execution
    print("Synchronous Execution:")
    result = client.run_agent(
        request="Clone repository dipakchavda2912/base-serverless",
        thread_id="demo_session_1",
        metadata={"user": "demo"}
    )
    print(f"Success: {result['success']}")
    print(f"Output: {result['output'][:200]}...")
    print(f"Execution time: {result['execution_time']:.2f}s\n")

    # 3. Streaming execution
    print("Streaming Execution:")
    for chunk in client.stream_agent("Read repository and list files"):
        print(f"Chunk: {chunk}")

    # 4. Background execution
    print("\nBackground Execution:")
    background_result = client.run_background(
        request="Analyze all files in repository"
    )
    print(f"Task ID: {background_result['task_id']}")
    print(f"Status: {background_result['status']}")
