from typing import Self
from pyparsing import abstractmethod


class PromptUtils:
    def __init__(self, chat_template):
        self.chat_template = chat_template
        pass

    def get_chat_prompt(self, user_request: str):
        return self.chat_template.invoke({"user_request": user_request})

    def get_chat_message_for_read_repository(self, repository: str, branch: str, clone_repository_path: str):
        prompt_text = """
        1. Read the repository "https://github.com/{repository}/tree/{branch}".
        2. Read all files including .js, .ts, .json, .yml, .md from the folders recursively if present.
        3. Prepare the lists of parsable array of the all the file content presents in the respository.
        4. Array should have objects with "file", "content", "sha" keys.
        4. There should be only file paths in the array with content.
        5. There should be no extra text, explanation outside of the JSON array or markdown syntax or extra characters or signs.
        6. Response should be in parsable JSON array format.
        """
        return self.get_chat_prompt(prompt_text.format(repository=repository, branch=branch, clone_repository_path=clone_repository_path))
