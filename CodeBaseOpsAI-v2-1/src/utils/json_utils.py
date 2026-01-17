"""
JSON utility functions for reading, writing, and manipulating JSON data.
"""
import json
from pathlib import Path
from typing import Dict, Any


class JsonUtils:
    """Utility class for common JSON operations."""

    @staticmethod
    def read_json(file_path: str | Path) -> Dict[str, Any]:
        """Read and parse a JSON file.

        Args:
            file_path: Path to the JSON file

        Returns:
            Dictionary containing the parsed JSON data
        """
        path = Path(file_path) if isinstance(file_path, str) else file_path
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def write_json(file_path: str | Path, data: Dict[str, Any], indent: int = 2) -> None:
        """Write dictionary data to a JSON file.

        Args:
            file_path: Path to the JSON file
            data: Dictionary to write to file
            indent: Number of spaces for indentation (default: 2)
        """
        path = Path(file_path) if isinstance(file_path, str) else file_path
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
            f.write("\n")

    @staticmethod
    def parse_json(json_string: str) -> Dict[str, Any]:
        """Parse a JSON string into a dictionary.

        Args:
            json_string: The JSON string to parse

        Returns:
            Dictionary representation of the JSON string
        """
        return json.loads(json_string)

    @staticmethod
    def add_attribute(json_data: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
        """Add a new attribute to a JSON object.

        Args:
            json_data: The original JSON object as a dictionary
            key: The key for the new attribute
            value: The value for the new attribute

        Returns:
            The updated JSON object with the new attribute added
        """
        json_data[key] = value
        return json_data

    @staticmethod
    def file_exists(file_path: str | Path) -> bool:
        """Check if a JSON file exists.

        Args:
            file_path: Path to check

        Returns:
            True if file exists, False otherwise
        """
        path = Path(file_path) if isinstance(file_path, str) else file_path
        return path.exists()
