import os
import subprocess

from config import CONSTANTS
from utils.serverless_utils import ServerlessUtils


class NodeOpsUtils:
    @staticmethod
    def clone_repo(main):
        repo_dir = CONSTANTS["REPO_DIR"]
        # Create repo directory if it doesn't exist
        os.makedirs(repo_dir, exist_ok=True)
        # Go to that directory
        subprocess.run(f"cd ~/${repo_dir}", cwd=repo_dir, shell=True)
        # Remove any existing repo (optional, for a true reclone)
        subprocess.run(f"rm -rf base-serverless", shell=True, check=True)
        repo_url = "https://github.com/dipakchavda2912/base-serverless"
        branch = "develop"
        # Remove any existing repo (optional, for a true reclone)
        subprocess.run(
            f"rm -rf {repo_dir}base-serverless", shell=True, check=True)
        # Show the current path
        subprocess.run(f"pwd", shell=True, check=True)
        # Clone the repo
        subprocess.run(f"git clone {repo_url}",
                       cwd=repo_dir, shell=True, check=True)
        # Checkout the branch
        subprocess.run(
            f"git checkout {branch}",
            cwd=os.path.join(repo_dir, "base-serverless"),
            shell=True,
            check=True,
        )
        # List files in tree structure
        result = subprocess.run(
            "tree .",
            cwd=os.path.join(repo_dir, "base-serverless"),
            shell=True,
            capture_output=True,
            text=True,
        )
        print(f"result")

    @staticmethod
    def set_env(main):
        query = """
      Request:
      1 .Following are the environment used in the serverless.yml
      dev, qa, uat, uatdr, prod, dr
      2. For the dev, qa, uat, uatdr environment the AWS account id is 1234567890
      3. For the prod, dr environment the AWS account id is 0987654321
      4. Following is the attribute pattern used to add attribute under the custom attribute in serverless.yml
      <env>-account-id: <account-id>
      Response:
      1. Based on the above information generate the custom attributes for all the environments in yaml format compatible.
      2. I want to get the result in plain text, without any code block, markdown formatting, any explanation, serverless attribute name.
      """
        response = main.ask(query)
        # Add a comment before the LLM response
        comment = "\n\tAWS account Id Map that would be used as a map for forming urns."
        commented_response = f"{comment}\n{response.strip()}"
        ServerlessUtils.update_custom(
            "custom", response.strip(), comment=comment)
        return response

    @staticmethod
    def set_region(main):
        query = """
      Request:
      1 .Following are the region used in the serverless.yml
      us-west-2, us-east-1
      2. For the dev, qa, uat, dr environment the region is us-west-2
      3. For the uatdr, prod environment the AWS region is us-east-1
      4. Following is the attribute pattern used to add attribute under the custom attribute in serverless.yml
      <env>-region: <aws-region-name>
      Response:
      1. Based on the above information generate the custom attributes for all the environments in yaml format compatible.
      2. I want to get the result in plain text, without any code block, markdown formatting, any explanation, serverless attribute name.
      """
        response = main.ask(query)
        comment = "\n\tRegion Map for deployment of lambda functions."
        ServerlessUtils.update_custom(
            "custom", response.strip(), comment=comment)
        return response

    @staticmethod
    def set_log_level(main):
        query = """
      Request:
      1 .Following are the log level used in the serverless.yml
      info, debug, error
      2. For the dev, qa environment the log level should be info
      2. For the uat, uatdr environment the log level should be debug
      3. For the prod, dr environment the log level should be error
      4. We should create the logLevelMap attribute under custom attribute in serverless.yml
      5. logLevelMap should have all the above environment and their log level in yaml format.
      6. map in Yaml is a way to represent the structured data using key-value pairs.
      Response:
      1. Based on the above information generate the custom attributes for all the environments in yaml format compatible.
      2. I want to get the result in plain text, without any code block, markdown formatting, any explanation, serverless attribute name.
      """
        response = main.ask(query)
        comment = "\n\tLog Level Map helps to identify the log level for each environment."
        ServerlessUtils.update_custom(
            "custom", response.strip(), comment=comment)
        return response
