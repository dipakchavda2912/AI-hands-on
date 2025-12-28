import os

CONSTANTS = {
  "GITHUB": {
    "REPO": "dipakchavda2912/base-serverless",
    "BRANCH": "develop",
    "ALLOWED_EXTENSIONS": [".ts", ".yml"]
  },
  "ALLOWED_CHARS_FOR_AGENT_NAME": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_",
  "CHUNK_SIZE": 1500,
  "CHUNK_OVERLAP": 200,
  "SYSTEM_INSTRUCTIONS": "You are a helpful assistant for answering questions about the given GitHub repository. You can reply an answers of the questions by reading the codes from the repository files and give the answers in details by referring the mentioned github repository.",
  "REPO_DIR": os.path.expanduser(
    "~/repo-to-be-created/"
  )

}
