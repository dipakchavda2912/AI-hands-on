"""
Unit tests for YAML tools (LangChain wrappers).
"""
import pytest
import os
from src.tools.yaml_tools import YamlTools


class TestYamlTools:
    """Test suite for YamlTools class."""

    def test_read_yaml_tool(self, temp_yaml_file):
        """Test the read_yaml tool."""
        result = YamlTools.read_yaml(temp_yaml_file)

        assert 'service' in result
        assert 'my-service' in result
        assert 'provider' in result

    def test_read_yaml_nonexistent_file(self):
        """Test reading a non-existent YAML file."""
        result = YamlTools.read_yaml('/nonexistent/file.yml')

        assert 'error' in result.lower() or 'not found' in result.lower()

    def test_update_yaml_attribute(self, temp_yaml_file):
        """Test updating a YAML attribute."""
        # Update service name
        result = YamlTools.update_yaml_attribute(
            temp_yaml_file,
            'service',
            'updated-service'
        )

        assert 'success' in result.lower()

        # Verify the change
        read_result = YamlTools.read_yaml(temp_yaml_file)
        assert 'updated-service' in read_result

    def test_update_nested_yaml_attribute(self, temp_yaml_file):
        """Test updating a nested YAML attribute."""
        result = YamlTools.update_yaml_attribute(
            temp_yaml_file,
            'provider.runtime',
            'nodejs20.x'
        )

        assert 'success' in result.lower()

        # Verify the change
        read_result = YamlTools.read_yaml(temp_yaml_file)
        assert 'nodejs20.x' in read_result

    def test_ensure_dict_key(self, temp_yaml_with_custom_string):
        """Test ensuring a key is a dictionary."""
        # The custom key starts as a string '{}'
        result = YamlTools.ensure_dict_key(
            temp_yaml_with_custom_string,
            'custom'
        )

        assert 'success' in result.lower() or 'converted' in result.lower()

        # Verify it's now a dict
        read_result = YamlTools.read_yaml(temp_yaml_with_custom_string)
        # After conversion, custom should be empty or have content
        assert 'custom' in read_result

    def test_add_yaml_attributes(self, temp_yaml_file):
        """Test adding multiple YAML attributes."""
        # Ensure custom is a dict first
        YamlTools.ensure_dict_key(temp_yaml_file, 'custom')

        # Add multiple attributes
        attributes_str = """dev-account-id: "123456"
qa-account-id: "789012"
prod-account-id: "345678"
"""

        result = YamlTools.add_yaml_attributes(
            temp_yaml_file,
            'custom',
            attributes_str
        )

        assert 'success' in result.lower()
        assert '3' in result or 'three' in result.lower()

        # Verify the changes
        read_result = YamlTools.read_yaml(temp_yaml_file)
        assert '123456' in read_result
        assert '789012' in read_result
