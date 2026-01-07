
from langchain_core.prompts import PromptTemplate


class AgentPropmpt:
    """Agent prompt for ReAct pattern reasoning.

    Provides prompts in two formats:
    - get_prompt_text(): String format for modern create_agent() API (recommended)
    - get_prompt_template(): PromptTemplate for legacy agent implementations
    """

    def __init__(self):
        pass

    def get_prompt_text(self) -> str:
        """Get the system prompt as a string.

        Used by modern create_agent() API. LangChain automatically handles
        variable substitution for {tools}, {tool_names}, {input}, {agent_scratchpad}.

        Returns:
            str: The system prompt with placeholders
        """
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
        """Get the system prompt as a PromptTemplate.

        Used for legacy agent implementations or when you need explicit
        control over prompt variable formatting.

        Returns:
            PromptTemplate: Template with defined input variables
        """
        return PromptTemplate(
            template=self.get_prompt_text(),
            input_variables=[
                "input",
                "tools",
                "tool_names",
                "agent_scratchpad"
            ]
        )
