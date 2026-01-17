"""
Pydantic schemas for package updates tool input validation.
"""
from pydantic import BaseModel, Field
from typing import Optional


class AnalyzePackagesInput(BaseModel):
    """Schema for analyzing package dependencies."""
    package_json_path: str = Field(
        default="package.json",
        description="Path to package.json file"
    )
    lock_major: bool = Field(
        default=True,
        description="Whether to lock major version updates"
    )
    npm_lookup: bool = Field(
        default=True,
        description="Whether to lookup package versions from npm registry. If False, skips version checking."
    )


class UpdatePackagesInput(BaseModel):
    """Schema for updating package dependencies."""
    package_json_path: str = Field(
        default="package.json",
        description="Path to package.json file"
    )
    lock_major: bool = Field(
        default=True,
        description="Whether to lock major version updates"
    )
    dry_run: bool = Field(
        default=False,
        description="Whether to perform a dry run without modifying files"
    )
    apply_updates: bool = Field(
        default=False,
        description="Whether to run package manager install after updating"
    )
    manager: str = Field(
        default="npm",
        description="Package manager to use (npm, yarn, or pnpm)"
    )
    npm_lookup: bool = Field(
        default=True,
        description="Whether to lookup package versions from npm registry. If False, skips version checking."
    )


class AuditPackagesInput(BaseModel):
    """Schema for auditing package vulnerabilities."""
    package_json_path: str = Field(
        default="package.json",
        description="Path to package.json file"
    )
    min_severity: Optional[str] = Field(
        default=None,
        description="Minimum severity level (low, moderate, high, critical)"
    )


class AddPackageInput(BaseModel):
    """Schema for adding a new package."""
    package_name: str = Field(
        ...,
        description="Name of the package to add"
    )
    version: Optional[str] = Field(
        default=None,
        description="Version to install (e.g., '^1.0.0', 'latest'). If not specified, latest compatible version will be used"
    )
    package_json_path: str = Field(
        default="package.json",
        description="Path to package.json file"
    )
    dev: bool = Field(
        default=False,
        description="Whether to add as dev dependency"
    )
    install: bool = Field(
        default=False,
        description="Whether to run package manager install after adding"
    )
    manager: str = Field(
        default="npm",
        description="Package manager to use (npm, yarn, or pnpm)"
    )
    npm_lookup: bool = Field(
        default=True,
        description="Whether to lookup package versions from npm registry. If False, uses specified version or 'latest'."
    )
    node_lts_version: Optional[str] = Field(
        default=None,
        description="Node.js LTS version for package compatibility checks. If not specified, will be detected from environment."
    )


class RemovePackageInput(BaseModel):
    """Schema for removing a package."""
    package_name: str = Field(
        ...,
        description="Name of the package to remove"
    )
    package_json_path: str = Field(
        default="package.json",
        description="Path to package.json file"
    )
    uninstall: bool = Field(
        default=False,
        description="Whether to run package manager uninstall"
    )
    manager: str = Field(
        default="npm",
        description="Package manager to use (npm, yarn, or pnpm)"
    )


class UpdateSpecificPackagesInput(BaseModel):
    """Schema for updating specific packages."""
    package_names: list[str] = Field(
        ...,
        description="List of package names to update"
    )
    package_json_path: str = Field(
        default="package.json",
        description="Path to package.json file"
    )
    lock_major: bool = Field(
        default=True,
        description="Whether to lock major version updates"
    )
    apply_updates: bool = Field(
        default=False,
        description="Whether to run package manager install after updating"
    )
    manager: str = Field(
        default="npm",
        description="Package manager to use (npm, yarn, or pnpm)"
    )
    npm_lookup: bool = Field(
        default=True,
        description="Whether to lookup package versions from npm registry. If False, skips version checking."
    )


class GetPackageInfoInput(BaseModel):
    """Schema for getting package information."""
    package_name: str = Field(
        ...,
        description="Name of the package to get information about"
    )
    package_json_path: str = Field(
        default="package.json",
        description="Path to package.json file"
    )
    npm_lookup: bool = Field(
        default=True,
        description="Whether to lookup package versions from npm registry. If False, skips registry information."
    )
