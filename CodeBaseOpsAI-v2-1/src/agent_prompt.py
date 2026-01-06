
from langchain_core.prompts import PromptTemplate


class AgentPropmpt:
    def __init__(self):
        pass

    def get_prompt_text(self) -> str:
        return '''You are a helpful assistant with access to specific tools.

        Available tools:
        {tools}

        Tool names: {tool_names}

        Follow this reasoning pattern:

        Question: {input}

        Think step by step:
        Thought: Consider what needs to be done
        Action: Choose a tool from [{tool_names}]
        Action Input: Provide input for the chosen tool
        Observation: See the tool's result
        ... repeat Thought/Action/Action Input/Observation as needed ...
        Thought: Formulate the final conclusion
        Final Answer: Provide the complete answer

        {agent_scratchpad}'''

    def get_prompt_template(self) -> PromptTemplate:
        return PromptTemplate(
            template=self.get_prompt_text(),
            input_variables=[
                "input",
                "tools",
                "tool_names",
                "agent_scratchpad"
            ]
        )
