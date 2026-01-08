"""
Pydantic schemas for JSON tool input validation.
"""
from pydantic import BaseModel, Field


class ParseJsonInput(BaseModel):
    """Schema for parsing JSON string input."""
    json_string: str = Field(
        ...,
        description="The JSON string to parse into a dictionary."
    )


class AddJsonAttributeInput(BaseModel):
    """Schema for adding a new attribute to a JSON object."""
    json_data: dict = Field(
        ...,
        description="The original JSON object as a dictionary."
    )
    key: str = Field(
        ...,
        description="The key for the new attribute to add."
    )
    value: str = Field(
        ...,
        description="The value for the new attribute to add."
    )


class SaveJsonToFileInput(BaseModel):
    """Schema for saving a JSON object to a file."""
    json_data: dict = Field(
        ...,
        description="The JSON object as a dictionary to save to a file."
    )
    file_path: str = Field(
        ...,
        description="The path to the file where the JSON should be saved."
    )
