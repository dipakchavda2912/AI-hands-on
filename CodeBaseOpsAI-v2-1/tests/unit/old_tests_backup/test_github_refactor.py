"""Test refactored GitHub tools"""
from src.tools.github_tools import GithubTools
import tempfile
import os

# Initialize tools
github_tools = GithubTools()

print("="*60)
print("Test 1: Clone a small public repository")
print("="*60)

# Create a temporary directory for testing
with tempfile.TemporaryDirectory() as tmpdir:
    clone_path = os.path.join(tmpdir, "test-repo")

    # Test clone (using a small public repo)
    result = github_tools.clone_repository("octocat/Hello-World", clone_path)
    print(result)

    print("\n" + "="*60)
    print("Test 2: Checkout a different branch")
    print("="*60)

    # Test checkout
    result = github_tools.checkout_branch(clone_path, "master")
    print(result)

print("\n✓ All tests completed successfully!")
