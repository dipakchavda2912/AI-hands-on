"""
Unit tests for YAML utilities.
"""
import pytest
import tempfile
import os
from src.utils.yaml_utils import YamlUtils


class TestYamlUtils:
    """Test suite for YamlUtils class."""

    def test_parse_yaml(self, temp_yaml_file):
        """Test parsing a YAML file."""
        data = YamlUtils.parse_yaml(temp_yaml_file)

        assert isinstance(data, dict)
        assert data['service'] == 'my-service'
        assert data['provider']['name'] == 'aws'

    def test_write_yaml(self, temp_directory):
        """Test writing a YAML file."""
        test_file = os.path.join(temp_directory, 'test.yml')
        test_data = {'key': 'value', 'nested': {'inner': 'data'}}

        YamlUtils.write_yaml(test_file, test_data)

        assert os.path.exists(test_file)

        # Read back and verify
        data = YamlUtils.parse_yaml(test_file)
        assert data == test_data

    def test_file_exists(self, temp_yaml_file):
        """Test file existence check."""
        assert YamlUtils.file_exists(temp_yaml_file) is True
        assert YamlUtils.file_exists('/nonexistent/path.yml') is False

    def test_get_nested_value(self, temp_yaml_file):
        """Test retrieving nested values."""
        data = YamlUtils.parse_yaml(temp_yaml_file)

        # Test simple key
        result = YamlUtils.get_nested_value(data, 'service')
        assert result == 'my-service'

        # Test nested key
        result = YamlUtils.get_nested_value(data, 'provider.name')
        assert result == 'aws'

        # Test deeply nested
        result = YamlUtils.get_nested_value(data, 'functions.hello.timeout')
        assert result == 30

        # Test non-existent key
        result = YamlUtils.get_nested_value(data, 'nonexistent.key')
        assert result is None

    def test_set_nested_value(self, temp_yaml_file):
        """Test setting nested values."""
        data = YamlUtils.parse_yaml(temp_yaml_file)

        # Set a simple value
        old, new = YamlUtils.set_nested_value(
            data, 'service', 'updated-service')
        assert old == 'my-service'
        assert new == 'updated-service'
        assert data['service'] == 'updated-service'

        # Set a nested value
        old, new = YamlUtils.set_nested_value(
            data, 'functions.hello.timeout', 60)
        assert old == 30
        assert new == 60
        assert data['functions']['hello']['timeout'] == 60

    def test_ensure_key_is_dict(self, temp_yaml_with_custom_string):
        """Test ensuring a key is a dictionary."""
        data = YamlUtils.parse_yaml(temp_yaml_with_custom_string)

        # Initially custom is a string
        assert isinstance(data.get('custom'), str)

        # Ensure it's a dict
        success, message = YamlUtils.ensure_key_is_dict(data, 'custom')
        assert success is True
        assert isinstance(data['custom'], dict)
        assert 'converted' in message.lower() or 'created' in message.lower()

    def test_add_multiple_attributes(self, temp_yaml_file):
        """Test adding multiple attributes."""
        data = YamlUtils.parse_yaml(temp_yaml_file)

        attributes = {
            'dev-account-id': '1234567890',
            'qa-account-id': '1234567890',
            'prod-account-id': '0987654321'
        }

        # Ensure custom key exists
        YamlUtils.ensure_key_is_dict(data, 'custom')

        # Add attributes
        count, added_keys = YamlUtils.add_multiple_attributes(
            data, 'custom', attributes)

        assert count == 3
        assert len(added_keys) == 3
        assert data['custom']['dev-account-id'] == '1234567890'
        assert data['custom']['prod-account-id'] == '0987654321'
