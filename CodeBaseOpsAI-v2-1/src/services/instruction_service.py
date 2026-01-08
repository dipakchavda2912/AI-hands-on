"""
Service for managing agent instructions
"""

from typing import List
from src.instructions.github_instructions import GithubInstructions
from src.instructions.serverless_custom_instructions import ServerlessCustomInstructions
from src.instructions.serverless_provider_instructions import ServerlessProviderInstructions


class InstructionService:
    """Service class for retrieving agent instructions"""

    def __init__(self, repository: str, clone_path: str, branch: str):
        """
        Initialize instruction service

        Args:
            repository: GitHub repository identifier
            clone_path: Local path where repository will be cloned
            branch: Branch name to work with
        """
        self.repository = repository
        self.clone_path = clone_path
        self.branch = branch

    def get_all_instructions(self) -> List[str]:
        """
        Get all agent instructions in sequence

        Returns:
            List of instruction strings
        """
        instruction_groups = [
            self.get_repository_operations_instructions(),
            self.get_serverless_yml_preparation_instructions(),
            self.get_aws_configuration_instructions(),
            self.get_custom_attributes_instructions(),
            self.get_bucket_and_datadog_instructions(),
            self.get_fdca_and_environment_mappings_instructions(),
            self.get_provider_stack_tags_instructions(),
        ]

        # Flatten the list of instruction groups
        instructions = [
            instruction
            for group in instruction_groups
            for instruction in group
        ]

        return instructions

    def get_repository_operations_instructions(self) -> List[str]:
        """Get only repository operation instructions"""
        return [
            GithubInstructions.get_read_repository_instruction(
                self.repository, self.branch),
            GithubInstructions.get_clone_repository_instruction(
                self.repository, self.clone_path),
            GithubInstructions.get_checkout_branch_instruction(
                self.clone_path, self.branch),
            GithubInstructions.get_list_files_instruction(
                self.clone_path, self.branch),
        ]

    def get_serverless_yml_preparation_instructions(self) -> List[str]:
        """Get serverless.yml preparation instructions"""
        return [
            ServerlessCustomInstructions.get_load_serverless_yml_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_create_custom_key_instruction(
                self.clone_path),
        ]

    def get_aws_configuration_instructions(self) -> List[str]:
        """Get AWS configuration instructions"""
        return [
            ServerlessCustomInstructions.get_aws_account_id_mappings_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_aws_region_mappings_instruction(
                self.clone_path),
        ]

    def get_custom_attributes_instructions(self) -> List[str]:
        """Get custom attributes instructions"""
        return [
            ServerlessCustomInstructions.get_add_powner_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_pvertical_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_paccountid_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_pappname_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_pcostcenter_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_penvironment_instruction(
                self.clone_path),
        ]

    def get_bucket_and_datadog_instructions(self) -> List[str]:
        """Get bucket and Datadog configuration instructions"""
        return [
            ServerlessCustomInstructions.get_add_bucket_mappings_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_datadog_arn_mappings_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_datadog_config_instruction(
                self.clone_path),
        ]

    def get_fdca_and_environment_mappings_instructions(self) -> List[str]:
        """Get FDCA tags and environment mapping instructions"""
        return [
            ServerlessCustomInstructions.get_add_fdca_tags_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_branch_name_mappings_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_environment_name_mappings_instruction(
                self.clone_path),
        ]

    def get_provider_stack_tags_instructions(self) -> List[str]:
        """Get provider stack tags instructions"""
        return [
            ServerlessProviderInstructions.get_add_stack_tags_instruction(
                self.clone_path),
        ]

    def get_serverless_config_instructions(self) -> List[str]:
        """Get serverless configuration instructions (legacy method for backward compatibility)"""
        return [
            ServerlessCustomInstructions.get_load_serverless_yml_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_create_custom_key_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_aws_account_id_mappings_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_aws_region_mappings_instruction(
                self.clone_path),
        ]

    def get_tagging_instructions(self) -> List[str]:
        """Get tagging and environment mapping instructions (legacy method for backward compatibility)"""
        return [
            ServerlessCustomInstructions.get_add_fdca_tags_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_branch_name_mappings_instruction(
                self.clone_path),
            ServerlessCustomInstructions.get_add_environment_name_mappings_instruction(
                self.clone_path),
            ServerlessProviderInstructions.get_add_stack_tags_instruction(
                self.clone_path),
        ]
