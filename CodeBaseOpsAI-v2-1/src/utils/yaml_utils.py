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
