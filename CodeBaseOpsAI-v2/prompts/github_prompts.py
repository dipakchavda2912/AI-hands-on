
from langchain_core.prompts import PromptTemplate


class GithubPrompt:
    chat_template: PromptTemplate = None

    def __init__(self):
        # ReAct agent requires a specific prompt format with {tools}, {tool_names}, {agent_scratchpad}, and {input}
        template = """
        You are CodeBaseOpsAI, an AI assistant that helps developers manage and operate codebases efficiently.
        You are an expert in github operations, code reviews, and codebase optimizations via github apis.
        Provide clear, concise, and accurate responses to user queries related to codebase operations.

        You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}
        """

        self.chat_template = PromptTemplate.from_template(template)

    def get_prompt_text(self, repository: str, branch: str, clone_repository_path: str) -> str:
        return """
        1. Read the repository "https://github.com/{repository}/tree/{branch}".
        2. Read all files including .js, .ts, .json, .yml, .md from the folders recursively if present.
        3. Prepare the lists of parsable array of the all the file content presents in the respository.
        4. Array should have objects with "file", "content", "sha" keys.
        4. There should be only file paths in the array with content.
        5. There should be no extra text, explanation outside of the JSON array or markdown syntax or extra characters or signs.
        6. Response should be in parsable JSON array format.
        """

    def get_chat_prompt(self, user_request: str):
        print(f"Generating chat prompt...{self.chat_template}")
        print(f"User Request: {user_request}")
        return self.chat_template.invoke({"user_request": user_request})

    def read_repository_prompt(self, repository: str, branch: str, clone_repository_path: str) -> str:
        prompt_text = self.get_prompt_text(
            repository, branch, clone_repository_path)
        formatted_prompt_text = prompt_text.format(
            repository=repository, branch=branch, clone_repository_path=clone_repository_path)
        self.chat_template = self.get_chat_prompt(formatted_prompt_text)
        return self.chat_template
