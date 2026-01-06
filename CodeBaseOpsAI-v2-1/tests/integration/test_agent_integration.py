"""
Integration tests for the complete agent workflow.
"""
import pytest
import os
import tempfile
from src.agent import Agent


class TestAgentIntegration:
    """Integration tests for the full agent workflow."""

    @pytest.fixture
    def agent(self):
        """Create an agent instance for testing."""
        return Agent()

    def test_agent_initialization(self, agent):
        """Test that agent initializes with all tools."""
        assert agent is not None
        assert agent.tools is not None
        assert len(agent.tools) > 0

    def test_agent_has_yaml_tools(self, agent):
        """Test that agent has YAML tools."""
        tool_names = [tool.name for tool in agent.tools]

        assert 'update_yaml_attribute' in tool_names
        assert 'read_yaml' in tool_names
        assert 'ensure_yaml_dict_key' in tool_names
        assert 'add_yaml_attributes' in tool_names

    def test_agent_has_github_tools(self, agent):
        """Test that agent has GitHub tools."""
        tool_names = [tool.name for tool in agent.tools]

        assert 'read_repository' in tool_names
        assert 'clone_repository' in tool_names
        assert 'checkout_branch' in tool_names
        assert 'list_files' in tool_names

    @pytest.mark.skip(reason="Requires actual GitHub token and API calls")
    def test_read_yaml_workflow(self, agent, temp_yaml_file):
        """Test reading a YAML file through the agent."""
        # This would require invoking the agent with a message
        # Skipping for now as it requires LLM calls
        pass

    @pytest.mark.skip(reason="Requires actual GitHub token and API calls")
    def test_github_workflow(self, agent):
        """Test GitHub operations through the agent."""
        # This would test the full workflow of cloning and reading a repo
        # Skipping for now as it requires API calls
        pass

    @pytest.mark.skip(reason="Requires LLM API calls")
    def test_yaml_modification_workflow(self, agent, temp_yaml_with_custom_string):
        """Test the complete YAML modification workflow."""
        # This would test:
        # 1. Ensure custom is a dict
        # 2. Add multiple attributes
        # 3. Verify changes
        # Skipping for now as it requires LLM calls
        pass
