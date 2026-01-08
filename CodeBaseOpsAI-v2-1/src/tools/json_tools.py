import json
import os
from langchain_core.tools import StructuredTool
from ..schemas.json_schemas import (
    ParseJsonInput,
    AddJsonAttributeInput,
    SaveJsonToFileInput
)


class JsonTools:
    pass
    """A collection of JSON-related tools for the agent to use."""

    def parse_json(self, json_string: str) -> dict:
        """Parse a JSON string into a dictionary.

        Args:
            json_string: The JSON string to parse.

        Returns:
            A dictionary representation of the JSON string.
        """
        return json.loads(json_string)

    def add_new_attribute(self, json_data: dict, key: str, value) -> dict:
        """Add a new attribute to a JSON object.

        Args:
            json_data: The original JSON object as a dictionary.
            key: The key for the new attribute.
            value: The value for the new attribute.

        Returns:
            The updated JSON object with the new attribute added.
        """
        json_data[key] = value
        return json_data

    def save_json_to_file(self, json_data: dict, file_path: str) -> None:
        """Save a JSON object to a file.

        Args:
            json_data: The JSON object as a dictionary.
            file_path: The path to the file where the JSON should be saved.
        """
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

    def get_tools(self) -> list[StructuredTool]:
        """Get list of all available tools."""
        return [
            StructuredTool(
                name="parse_json",
                func=self.parse_json,
                description="Parse a JSON string into a dictionary",
                args_schema=ParseJsonInput
            ),
            StructuredTool(
                name="add_new_attribute",
                func=self.add_new_attribute,
                description="Add a new attribute to a JSON object",
                args_schema=AddJsonAttributeInput
            ),
            StructuredTool(
                name="save_json_to_file",
                args_schema=SaveJsonToFileInput,
                func=self.save_json_to_file,
                description="Save a JSON object to a file"
            )
        ]
