import os
import re

from ruamel.yaml import YAML

from config import CONSTANTS

yaml = YAML()
yaml.preserve_quotes = True


class ServerlessUtils:
  serverless_path = os.path.join(
    CONSTANTS["REPO_DIR"], "base-serverless", "serverless.yml"
  )

  @staticmethod
  def update_custom(sl_attribute: str, llm_response, comment=None):
    # Remove markdown code block markers and comments
    lines = llm_response.strip().splitlines()
    yaml_lines = [
      line
      for line in lines
      if not line.strip().startswith("```")
         and not line.strip().startswith("#")
         and line.strip()
    ]
    yaml_str = "\n".join(yaml_lines)

    # If the response is nested under 'custom:', extract only the mapping
    if yaml_str.startswith("custom:"):
      yaml_str = re.sub(r"^custom:\s*", "", yaml_str)
      yaml_str = re.sub(r"^\s+", "", yaml_str, flags=re.MULTILINE)

    # Parse the new attributes
    try:
      from io import StringIO

      custom_attrs = yaml.load(StringIO(yaml_str))
      if custom_attrs is None:
        custom_attrs = {}
    except Exception as e:
      print("Failed to parse LLM response as YAML:", e)
      return

    # Ensure the file exists
    if not os.path.exists(ServerlessUtils.serverless_path):
      with open(ServerlessUtils.serverless_path, "w") as f:
        f.write("custom: {}\n")

    # Load the existing serverless.yml
    with open(ServerlessUtils.serverless_path, "r") as f:
      data = yaml.load(f)
    if data is None:
      data = {}

    # Ensure 'custom' exists
    if sl_attribute not in data or data[sl_attribute] is None:
      data[sl_attribute] = {}

    # Add comment before new attributes if provided
    if comment:
      for k in custom_attrs:
        data[sl_attribute].yaml_set_comment_before_after_key(k, before=comment)
        break  # Only add before the first new key

    # Merge new attributes into existing custom section
    for k, v in custom_attrs.items():
      data[sl_attribute][k] = v

    # Write back to serverless.yml
    with open(ServerlessUtils.serverless_path, "w") as f:
      yaml.dump(data, f)
    print(f"serverless.yml updated with new {sl_attribute} attributes.")
    return llm_response
