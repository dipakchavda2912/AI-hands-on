"""
GitHub Agent using LangChain Classic ReAct Agent.

Simple agent that uses the ReAct pattern to reason and act using GitHub tools.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate


class GithubAgent:
    """
    GitHub operations agent using ReAct pattern.

    This agent uses the classic ReAct pattern to perform GitHub operations.
    """

    def __init__(self, tools: list, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the GitHub agent.

        Args:
            tools: List of LangChain tools for GitHub operations
            model_name: Name of the LLM model to use
        """
        self.tools = tools
        self.model_name = model_name

        # Initialize the language model
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.0
        )

        # Create the ReAct prompt template
        template = """Answer the following questions as best you can. You have access to the following tools:

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
Thought: {agent_scratchpad}"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
                "tool_names": ", ".join([tool.name for tool in tools])
            }
        )

        # Create the ReAct agent
        agent = create_react_agent(
            llm=self.model,
            tools=self.tools,
            prompt=prompt
        )

        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )

    def run(self, user_request: str) -> str:
        """
        Execute the agent with the given request.

        Args:
            user_request: The user's request

        Returns:
            The agent's response
        """
        result = self.agent_executor.invoke({"input": user_request})
        return result.get("output", "")
