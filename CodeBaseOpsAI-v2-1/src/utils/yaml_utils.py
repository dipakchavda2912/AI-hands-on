import os
import yaml
from typing import Any, Tuple


class YamlUtils:

    @staticmethod
    def parse_yaml(yaml_file_path: str) -> dict:
        """Parse a YAML file and return its contents as a dictionary.

        Args:
            yaml_file_path: Path to the YAML file

        Returns:
            Dictionary containing the parsed YAML data
        """
        with open(yaml_file_path, 'r') as f:
            data = yaml.safe_load(f)
        return data

    @staticmethod
    def write_yaml(yaml_file_path: str, data: dict) -> None:
        """Write dictionary data to a YAML file.

        Args:
            yaml_file_path: Path to the YAML file
            data: Dictionary to write to file
        """
        with open(yaml_file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists.

        Args:
            file_path: Path to check

        Returns:
            True if file exists, False otherwise
        """
        return os.path.exists(file_path)

    @staticmethod
    def navigate_to_nested_key(data: dict, key_path: str) -> Tuple[dict, str, Any]:
        """Navigate to a nested key in a dictionary using dot notation.

        Args:
            data: The dictionary to navigate
            key_path: Dot-separated path (e.g., 'parent.child.attr')

        Returns:
            Tuple of (parent_dict, final_key, old_value)
        """
        keys = key_path.split('.')
        d = data

        # Navigate to parent of target key
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]

        # Get old value
        final_key = keys[-1]
        old_value = d.get(final_key, 'not set')

        return d, final_key, old_value

    @staticmethod
    def set_nested_value(data: dict, key_path: str, new_value: Any) -> Tuple[Any, Any]:
        """Set a value in a nested dictionary using dot notation.

        Args:
            data: The dictionary to modify
            key_path: Dot-separated path (e.g., 'parent.child.attr')
            new_value: The value to set

        Returns:
            Tuple of (old_value, new_value)
        """
        parent_dict, final_key, old_value = YamlUtils.navigate_to_nested_key(
            data, key_path)
        parent_dict[final_key] = new_value
        return old_value, new_value

    @staticmethod
    def get_nested_value(data: dict, key_path: str) -> Any:
        """Get a value from a nested dictionary using dot notation.

        Args:
            data: The dictionary to read
            key_path: Dot-separated path (e.g., 'parent.child.attr')

        Returns:
            The value at the specified path, or None if not found
        """
        keys = key_path.split('.')
        d = data

        for key in keys:
            if not isinstance(d, dict) or key not in d:
                return None
            d = d[key]

        return d

    @staticmethod
    def ensure_key_is_dict(data: dict, key_path: str) -> Tuple[bool, str]:
        """Ensure a key exists and is a dictionary, creating or converting it if needed.

        Args:
            data: The dictionary to modify
            key_path: Dot-separated path (e.g., 'custom' or 'parent.custom')

        Returns:
            Tuple of (success, message)
        """
        keys = key_path.split('.')
        d = data

        # Navigate to parent of target key
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            elif not isinstance(d[key], dict):
                return False, f"Key '{key}' in path exists but is not a dictionary"
            d = d[key]

        final_key = keys[-1]

        # Check if key exists and what type it is
        if final_key not in d:
            d[final_key] = {}
            return True, f"Created new dictionary at '{key_path}'"
        elif isinstance(d[final_key], dict):
            return True, f"Key '{key_path}' already exists as a dictionary"
        else:
            # Convert to dict (e.g., from string "{}" or empty value)
            d[final_key] = {}
            return True, f"Converted '{key_path}' from {type(d[final_key]).__name__} to dictionary"

    @staticmethod
    def add_multiple_attributes(data: dict, parent_key: str, attributes: dict) -> Tuple[int, list]:
        """Add multiple attributes under a parent key.

        Args:
            data: The dictionary to modify
            parent_key: The parent key path (e.g., 'custom')
            attributes: Dictionary of attributes to add

        Returns:
            Tuple of (count_added, list_of_added_keys)
        """
        # Ensure parent key is a dictionary
        success, msg = YamlUtils.ensure_key_is_dict(data, parent_key)
        if not success:
            return 0, []

        # Get the parent dict
        parent_dict = YamlUtils.get_nested_value(data, parent_key)
        if parent_dict is None:
            parent_dict = {}
            YamlUtils.set_nested_value(data, parent_key, parent_dict)

        # Add all attributes
        added_keys = []
        for key, value in attributes.items():
            parent_dict[key] = value
            added_keys.append(key)

        return len(added_keys), added_keys

    @staticmethod
    def add_yaml_formatted_array_list(data: dict, parent_key: str, array_list: list) -> Tuple[int, list]:
        """Add a YAML-formatted array list under a parent key.

        Args:
            data: The dictionary to modify
            parent_key: The parent key path (e.g., 'plugins')
            array_list: List of items to add
        Returns:
            Tuple of (count_added, list_of_added_items)
        """
        # Set the parent key to the array list directly
        old_value, new_value = YamlUtils.set_nested_value(
            data, parent_key, array_list)

        return len(array_list), array_list
