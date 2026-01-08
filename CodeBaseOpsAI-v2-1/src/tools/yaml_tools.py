from langchain_core.tools import StructuredTool
import yaml
from ..utils import YamlUtils
from ..schemas.yaml_schemas import (
    UpdateYamlInput,
    ReadYamlInput,
    EnsureDictKeyInput,
    AddAttributesInput,
    AddArrayListInput
)


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

    def ensure_dict_key(self, yaml_file_path: str, key_path: str) -> str:
        """Ensure a key exists as a dictionary in a YAML file.

        Args:
            yaml_file_path: Path to the YAML file
            key_path: Dot-separated path to the key (e.g., 'custom')

        Returns:
            String with operation status
        """
        try:
            if not YamlUtils.file_exists(yaml_file_path):
                return f"Error: File '{yaml_file_path}' does not exist."

            data = YamlUtils.parse_yaml(yaml_file_path)
            success, message = YamlUtils.ensure_key_is_dict(data, key_path)

            if success:
                YamlUtils.write_yaml(yaml_file_path, data)
                return f"Success: {message}"
            else:
                return f"Error: {message}"

        except Exception as e:
            return f"Error ensuring dictionary key: {str(e)}"

    def add_yaml_attributes(self, yaml_file_path: str, parent_key: str, attributes_yaml: str) -> str:
        """Add multiple attributes under a parent key in a YAML file.

        Args:
            yaml_file_path: Path to the YAML file
            parent_key: Parent key path (e.g., 'custom')
            attributes_yaml: YAML formatted string of attributes to add

        Returns:
            String with operation status
        """
        try:
            if not YamlUtils.file_exists(yaml_file_path):
                return f"Error: File '{yaml_file_path}' does not exist."

            # Parse the main file
            data = YamlUtils.parse_yaml(yaml_file_path)

            # Parse the attributes YAML string
            attributes = yaml.safe_load(attributes_yaml)
            if not isinstance(attributes, dict):
                return "Error: attributes_yaml must be a valid YAML dictionary"

            # Add attributes
            count, added_keys = YamlUtils.add_multiple_attributes(
                data, parent_key, attributes)

            # Write back
            YamlUtils.write_yaml(yaml_file_path, data)

            return f"Successfully added {count} attributes under '{parent_key}': {', '.join(added_keys)}"

        except yaml.YAMLError as e:
            return f"Error parsing attributes YAML: {str(e)}"
        except Exception as e:
            return f"Error adding attributes: {str(e)}"

    def add_yaml_array_list(self, yaml_file_path: str, parent_key: str, array_items_yaml: str) -> str:
        """Add an array list under a key in a YAML file.

        Args:
            yaml_file_path: Path to the YAML file
            parent_key: Key to add the array under (e.g., 'plugins')
            array_items_yaml: YAML formatted string of array items

        Returns:
            String with operation status
        """
        try:
            if not YamlUtils.file_exists(yaml_file_path):
                return f"Error: File '{yaml_file_path}' does not exist."

            # Parse the main file
            data = YamlUtils.parse_yaml(yaml_file_path)

            # Parse the array items YAML string
            array_items = yaml.safe_load(array_items_yaml)
            if not isinstance(array_items, list):
                return "Error: array_items_yaml must be a valid YAML list"

            # Add array list
            count, added_items = YamlUtils.add_yaml_formatted_array_list(
                data, parent_key, array_items)

            # Write back
            YamlUtils.write_yaml(yaml_file_path, data)

            return f"Successfully added {count} items to '{parent_key}': {', '.join(str(item) for item in added_items)}"

        except yaml.YAMLError as e:
            return f"Error parsing array YAML: {str(e)}"
        except Exception as e:
            return f"Error adding array list: {str(e)}"

    def get_tools(self) -> list[StructuredTool]:
        """Get list of all available tools."""
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
            ),
            StructuredTool(
                name="ensure_yaml_dict_key",
                func=self.ensure_dict_key,
                description="Ensure a key exists as a dictionary in a YAML file, creating or converting it if needed",
                args_schema=EnsureDictKeyInput
            ),
            StructuredTool(
                name="add_yaml_attributes",
                func=self.add_yaml_attributes,
                description="Add multiple attributes under a parent key in a YAML file. Attributes should be provided as YAML formatted string",
                args_schema=AddAttributesInput
            ),
            StructuredTool(
                name="add_yaml_array_list",
                func=self.add_yaml_array_list,
                description="Add an array list under a key in a YAML file. Array items should be provided as YAML formatted list (e.g., '[item1, item2]' or '- item1\\n- item2')",
                args_schema=AddArrayListInput
            )
        ]
