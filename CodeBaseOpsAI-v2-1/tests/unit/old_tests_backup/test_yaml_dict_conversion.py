"""Test new YAML tools for handling dict conversion"""
import tempfile
import os
from src.tools.yaml_tools import YamlTools

# Create test YAML with custom as a string
test_content = """service: my-service
provider:
  name: aws
custom: '{}'
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
    f.write(test_content)
    test_file = f.name

print("="*60)
print("Initial YAML content:")
print("="*60)
with open(test_file, 'r') as f:
    print(f.read())

yaml_tools = YamlTools()

# Test 1: Ensure custom is a dict
print("\n" + "="*60)
print("Test 1: Ensure 'custom' key is a dictionary")
print("="*60)
result = yaml_tools.ensure_dict_key(test_file, "custom")
print(result)

# Test 2: Add multiple attributes
print("\n" + "="*60)
print("Test 2: Add AWS account mappings")
print("="*60)
attributes = """dev-account-id: '1234567890'
qa-account-id: '1234567890'
uat-account-id: '1234567890'
prod-account-id: '0987654321'
dr-account-id: '0987654321'
"""
result = yaml_tools.add_yaml_attributes(test_file, "custom", attributes)
print(result)

# Show final result
print("\n" + "="*60)
print("Final YAML content:")
print("="*60)
with open(test_file, 'r') as f:
    print(f.read())

# Cleanup
os.unlink(test_file)
print("✓ Test completed successfully!")
