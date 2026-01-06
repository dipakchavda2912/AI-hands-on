from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from ..utils import YamlUtils


class YamlTools:
    def __init__(self) -> None:
        """Initialize Yaml tools."""
        pass

    def read_yaml(self, yaml_file_path: str) -> str:
        """Read and return the contents of a YAML file.

        Args:
            yaml_file_path: Path to the YAML file to read
        Returns:
            String representation of the YAML file contents
        """

        try:
            # Check if file exists
            if not YamlUtils.file_exists(yaml_file_path):
                return f"Error: File '{yaml_file_path}' does not exist."

            # Parse the YAML file
            data = YamlUtils.parse_yaml(yaml_file_path)

            return f"Contents of '{yaml_file_path}':\n{data}"

        except Exception as e:
            return f"Error reading YAML file: {str(e)}"

    def update_yaml_attribute(self, yaml_file_path: str, attribute_path: str, new_value: str) -> str:
        """Update an attribute in a YAML file.

        Args:
            yaml_file_path: Path to the YAML file
            attribute_path: Dot-separated path to the attribute (e.g., 'parent.child.attr')
            new_value: New value to set for the attribute
        Returns:
            String with update status
        """
        try:
            # Check if file exists
            if not YamlUtils.file_exists(yaml_file_path):
                return f"Error: File '{yaml_file_path}' does not exist."

            # Parse the YAML file
            data = YamlUtils.parse_yaml(yaml_file_path)

            # Set the new value and get old value
            old_value, updated_value = YamlUtils.set_nested_value(
                data, attribute_path, new_value)

            # Write back to file
            YamlUtils.write_yaml(yaml_file_path, data)

            return f"Successfully updated '{attribute_path}' in '{yaml_file_path}'. Old value: {old_value}, New value: {updated_value}"

        except Exception as e:
            return f"Error updating YAML file: {str(e)}"

    def get_tools(self) -> list[StructuredTool]:
        """Get list of all available tools."""

        # Define input schema for YAML update
        class UpdateYamlInput(BaseModel):
            yaml_file_path: str = Field(
                description="Path to the YAML file to update")
            attribute_path: str = Field(
                description="Dot-separated path to the attribute (e.g., 'service.name' or 'functions.myFunction.handler')")
            new_value: str = Field(
                description="New value to set for the attribute")

        class ReadYamlInput(BaseModel):
            yaml_file_path: str = Field(
                description="Path to the YAML file to read")

        return [
            StructuredTool(
                name="update_yaml_attribute",
                func=self.update_yaml_attribute,
                description="Update an attribute in a YAML file using dot-separated path notation",
                args_schema=UpdateYamlInput
            ),
            StructuredTool(
                name="read_yaml",
                func=self.read_yaml,
                description="Read and return the contents of a YAML file",
                args_schema=ReadYamlInput
            )
        ]
