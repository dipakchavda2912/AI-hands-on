"""Test YAML tools functionality"""
import os
import tempfile
from src.tools.yaml_tools import YamlTools

# Create a test YAML file
test_yaml_content = """
service: my-service
provider:
  name: aws
  runtime: python3.9
functions:
  hello:
    handler: handler.hello
    timeout: 30
  world:
    handler: handler.world
    memory: 512
"""

# Create temporary YAML file
with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
    f.write(test_yaml_content)
    test_file = f.name

print(f"Created test YAML file: {test_file}")

# Initialize tools
yaml_tools = YamlTools()

# Test 1: Update simple attribute
print("\n" + "="*60)
print("Test 1: Update service name")
print("="*60)
result = yaml_tools.update_yaml_attribute(
    test_file, "service", "updated-service")
print(result)

# Test 2: Update nested attribute
print("\n" + "="*60)
print("Test 2: Update function timeout")
print("="*60)
result = yaml_tools.update_yaml_attribute(
    test_file, "functions.hello.timeout", "60")
print(result)

# Test 3: Read the updated file
print("\n" + "="*60)
print("Updated YAML content:")
print("="*60)
with open(test_file, 'r') as f:
    print(f.read())

# Cleanup
os.unlink(test_file)
print(f"\n✓ Test completed successfully!")
