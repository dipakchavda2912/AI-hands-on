"""
Serverless provider section instructions
"""


class ServerlessProviderInstructions:
    """Instructions for serverless.yml provider section attributes"""

    @staticmethod
    def get_add_stack_tags_instruction(clone_path: str) -> str:
        """Get instruction to add stack tags in provider section"""
        return f"""
            Add the following attributes in the provider section of the {clone_path}serverless.yml file. If the provider section is not present, please add it. All the below variables should use serverless syntax for referencing custom attributes. Don't paste the actual values in the stackTags - use dynamic references instead.
            stackTags:
            service name should reference the service name from the serverless.yml file
            Name should be a combination of pOwner, pEnvironment, and service name separated by hyphens
            Vertical should reference the pVertical value from custom section
            Env should reference the pEnvironment value from custom section
            CostCenter should reference the pCostCenter value from custom section
            version should reference the version attribute from package.json file
            application should be Admin console
            fdca:team should reference the fdca-team value from custom section
            fdca:app-id should reference the fdca-app-id value from custom section
            fdca:app-name should reference the fdca-app-name value from custom section
            fdca:created-by-email should reference the fdca-created-by-email value from custom section
            fdca:git_url should reference the fdca-git-url value from custom section
            fdca:git_revision should reference the branch-name attribute from custom section by dynamically constructing the key name using the current pEnvironment value with the pattern pEnvironment-branch-name
            fdca:timestamp should reference the fdca-timestamp value from custom section
            fdca:environment should reference the env attribute from custom section by dynamically constructing the key name using the current pEnvironment value with the pattern pEnvironment-env
            fdca:blueprint_sources should reference the fdca-blueprint-sources value from custom section
            map-migrated: abc-migrate-tag-value
            """
