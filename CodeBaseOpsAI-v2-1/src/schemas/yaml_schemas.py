"""
Pydantic schemas for YAML tool input validation.
"""

from pydantic import BaseModel, Field


class UpdateYamlInput(BaseModel):
    """Input schema for updating a YAML attribute."""
    yaml_file_path: str = Field(
        description="Path to the YAML file to update")
    attribute_path: str = Field(
        description="Dot-separated path to the attribute (e.g., 'service.name' or 'functions.myFunction.handler')")
    new_value: str = Field(
        description="New value to set for the attribute")


class ReadYamlInput(BaseModel):
    """Input schema for reading a YAML file."""
    yaml_file_path: str = Field(
        description="Path to the YAML file to read")


class EnsureDictKeyInput(BaseModel):
    """Input schema for ensuring a key exists as a dictionary."""
    yaml_file_path: str = Field(
        description="Path to the YAML file")
    key_path: str = Field(
        description="Key path to ensure exists as a dictionary (e.g., 'custom')")


class AddAttributesInput(BaseModel):
    """Input schema for adding multiple attributes to a YAML file."""
    yaml_file_path: str = Field(
        description="Path to the YAML file")
    parent_key: str = Field(
        description="Parent key to add attributes under (e.g., 'custom')")
    attributes_yaml: str = Field(
        description="YAML formatted string of attributes to add")


class AddArrayListInput(BaseModel):
    """Input schema for adding an array list to a YAML file."""
    yaml_file_path: str = Field(
        description="Path to the YAML file")
    parent_key: str = Field(
        description="Key to add the array list under (e.g., 'plugins')")
    array_items_yaml: str = Field(
        description="YAML formatted string of array items (e.g., '- item1\\n- item2' or '[item1, item2]')")
