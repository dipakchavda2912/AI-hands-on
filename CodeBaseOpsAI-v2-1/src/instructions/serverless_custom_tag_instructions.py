"""
Serverless custom attributes instructions
"""

from typing import List, Optional


class ServerlessCustomTagInstructions:
    """Instructions for serverless.yml custom section attributes"""

    def __init__(self, *, clone_path: Optional[str] = None, package_name: Optional[str] = None, is_dev: bool = False):
        """Initialize with configuration"""
        self.clone_path = clone_path
        self.package_name = package_name
        self.is_dev = is_dev

    def get_instructions(self) -> List[str]:
        """Get all serverless custom section instructions

        Returns:
            List of serverless custom configuration instruction strings
        """
        return [
            self.get_load_serverless_yml_instruction(),
            self.get_create_custom_key_instruction(),
            self.get_aws_account_id_mappings_instruction(),
            self.get_aws_region_mappings_instruction(),
            self.get_add_powner_instruction(),
            self.get_add_pvertical_instruction(),
            self.get_add_paccountid_instruction(),
            self.get_add_pappname_instruction(),
            self.get_add_pcostcenter_instruction(),
            self.get_add_penvironment_instruction(),
            self.get_add_bucket_mappings_instruction(),
            self.get_add_datadog_arn_mappings_instruction(),
            self.get_add_datadog_config_instruction(),
            self.get_add_fdca_tags_instruction(),
            self.get_add_branch_name_mappings_instruction(),
            self.get_add_environment_name_mappings_instruction(),
        ]

    def get_load_serverless_yml_instruction(self) -> str:
        """Get instruction to load and parse serverless.yml"""
        return f"Load the {self.clone_path}serverless.yml file from the local filesystem path {self.clone_path} and parse it."

    def get_create_custom_key_instruction(self) -> str:
        """Get instruction to create custom key in serverless.yml"""
        return f"Create a `custom` key in the {self.clone_path}serverless.yml file if it does not already exist."

    def get_aws_account_id_mappings_instruction(self) -> str:
        """Get instruction to add AWS account ID mappings"""
        return f"""Add AWS account ID mappings under the 'custom' key.
            beginning: '# AWS account Id Map that would be used as a map for forming urns.'
            For environments dev, qa, uat, uatdr: use AWS account ID 1234567890
            For environments prod, dr: use AWS account ID 0987654321
            Use the pattern '<env>-account-id: <account-id>' for each environment (e.g., dev-account-id: 1234567890).
            Value should not use quotes.
            Update the {self.clone_path}serverless.yml file with these mappings."""

    def get_aws_region_mappings_instruction(self) -> str:
        """Get instruction to add AWS region mappings"""
        return f"""Add AWS region mappings under the 'custom' key.
            beginning: '# AWS Region Map for deployment of lambda functions.'
            For environments dev, qa, uat, dr: use AWS region us-west-2
            For environments uatdr, prod: use AWS region us-east-1
            Use the pattern '<env>-region: <aws-region-name>' for each environment (e.g., dev-region: us-west-2).
            Value should not use quotes.
            Update the {self.clone_path}serverless.yml file with these mappings."""

    def get_add_powner_instruction(self) -> str:
        """Get instruction to add pOwner attribute"""
        return f"""Add pOwner: abcd attribute under the `custom` key in the {self.clone_path}serverless.yml file."""

    def get_add_pvertical_instruction(self) -> str:
        """Get instruction to add pVertical attribute"""
        return f"""Add pVertical: abcd attribute under the `custom` key in the {self.clone_path}serverless.yml file."""

    def get_add_paccountid_instruction(self) -> str:
        """Get instruction to add pAccountId attribute"""
        return f"""Add pAccountId: which is referring the dynamic account id based on the environment from the AWS account ID mappings under the `custom` key in the {self.clone_path}serverless.yml file."""

    def get_add_pappname_instruction(self) -> str:
        """Get instruction to add pAppName attribute"""
        return f"""Add pAppName: abcd attribute under the `custom` key in the {self.clone_path}serverless.yml file."""

    def get_add_pcostcenter_instruction(self) -> str:
        """Get instruction to add pCostCenter attribute"""
        return f"""Add pCostCenter: 1010011:1111111 attribute under the `custom` key in the {self.clone_path}serverless.yml file."""

    def get_add_penvironment_instruction(self) -> str:
        """Get instruction to add pEnvironment attribute"""
        return f"""Add pEnvironment attribute under the `custom` key in the {self.clone_path}serverless.yml file.
            The value should be a serverless framework variable reference: ${{opt:stage, self:provider.stage}}
            This dynamically resolves to either the --stage CLI option or the provider.stage value from the serverless.yml file.
            The value should NOT use quotes."""

    def get_add_bucket_mappings_instruction(self) -> str:
        """Get instruction to add bucket name mappings"""
        return f"""Add bucket name as per enviroment under the `custom` key in the {self.clone_path}serverless.yml file.
            beginning: '# S3 Bucket names for different environments.'
            For environments dev, qa use the bucket name as per environment.
            For environments uat, uatdr use the bucket name uat.
            For environments prod, dr use bucket name prod.
            Use the pattern '<env>-bucket: <bucket-name>' for each environment (e.g., dev-bucket: dev).
            Value should not use quotes."""

    def get_add_datadog_arn_mappings_instruction(self) -> str:
        """Get instruction to add Datadog ARN mappings"""
        return f"""Add Datadog API Key Secret Manager ARN mappings under the 'custom' key in the {self.clone_path}serverless.yml file.
            beginning: '# Datadog API Key Secret Manager ARN per environment.'
            For each environment (dev, qa, uat, uatdr, prod, dr), add a literal AWS Secrets Manager ARN string.

            Use the pattern: <env>-datadog-api-arn: arn:aws:secretsmanager:<region>:<account-id>:secret:<env>-datadog-api-key

            Examples:
            - dev-datadog-api-arn: arn:aws:secretsmanager:us-west-2:1234567890:secret:dev-datadog-api-key
            - prod-datadog-api-arn: arn:aws:secretsmanager:us-east-1:0987654321:secret:prod-datadog-api-key

            Use the appropriate region and account ID for each environment based on the previously defined mappings.
            Values should be literal ARN strings WITHOUT quotes.
            Update the {self.clone_path}serverless.yml file with these mappings."""

    def get_add_datadog_config_instruction(self) -> str:
        """Get instruction to add Datadog configuration"""
        return f"""
            Add a nested attribute 'datadog' under the `custom` key in the {self.clone_path}serverless.yml file.
            The datadog attribute should contain two sub-attributes:
            1. site: datadoghq.com (plain string value without quotes)
            2. apiKeySecretArn: should use a serverless framework variable reference to dynamically reference the environment-specific datadog ARN.

            The apiKeySecretArn value should be: ${{self:custom.${{self:custom.pEnvironment}}-datadog-api-arn}}
            This dynamically resolves to the correct environment's datadog ARN by:
            - First resolving pEnvironment to get current environment (dev/prod/etc)
            - Then using that to reference the corresponding <env>-datadog-api-arn attribute.
            Values should NOT use quotes.
            """

    def get_add_fdca_tags_instruction(self) -> str:
        """Get instruction to add FDCA tags"""
        return f"""
            Add FDCA tags under the `custom` key in the {self.clone_path}serverless.yml file.
            All tags start with `fdca-`. The following attributes to be added:
            team should be NAQP
            app-id should be APM0005284
            app-name should be Admin console
            created-by-email should be my email
            git-url should be full repository url with .git extension
            timestamp should be utc timestamp of the modification
            blueprint-sources should be NA
            """

    def get_add_branch_name_mappings_instruction(self) -> str:
        """Get instruction to add branch name mappings"""
        return f"""
            Add branch name mappings under the 'custom' key in the {self.clone_path}serverless.yml file.
            beginning: '# Tagging branch name'
            For environment dev: use branch name develop
            For environments qa, uat, uatdr, prod, dr: use a dynamic release branch reference from package.json version field
            Use the pattern '<env>-branch-name: <branch-name>' for each environment.
            The release branch should dynamically reference the version from package.json in the format release/version.
            Values should not use quotes.
            Update the {self.clone_path}serverless.yml file with these mappings.
            """

    def get_add_environment_name_mappings_instruction(self) -> str:
        """Get instruction to add environment name mappings"""
        return f"""
            Add environment name mappings under the 'custom' key in the {self.clone_path}serverless.yml file.
            For environments dev, qa, uat: use the same environment name
            For environment uatdr: use uat
            For environments prod, dr: use prod
            Use the pattern '<env>-env: <environment-name>' for each environment (e.g., dev-env: dev).
            Values should not use quotes.
            Update the {self.clone_path}serverless.yml file with these mappings.
            """
