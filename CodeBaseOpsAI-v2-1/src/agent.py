"""
CodeBaseOpsAI - Simple GitHub Agent Example

This demonstrates a basic ReAct agent that can perform GitHub operations.
"""

import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools import GithubTools, YamlTools
from .agent_prompt import AgentPropmpt


class Agent():
    tools = None
    agent_prompt = None
    agent = None
    agent_executor = None

    def __init__(self):
        self.tools = self.init_tools()
        self.agent_prompt = AgentPropmpt()
        self.llm = self.init_llm()
        self.agent_executor = self.init_react_agent()

    def init_tools(self):
        github_tools = GithubTools()
        yaml_tools = YamlTools()
        return github_tools.get_tools() + yaml_tools.get_tools()

    def init_llm(self) -> ChatGoogleGenerativeAI:
        load_dotenv()
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_output_tokens=1024,
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        return llm

    def init_react_agent(self):
        """Create an agent using the modern langchain.agents.create_agent API."""
        agent_executor = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.agent_prompt.get_prompt_text()
        )
        return agent_executor

    def set_agent_executor(self, executor):
        """Set the agent executor."""
        self.agent_executor = executor

    def get_agent_executor(self):
        return self.agent_executor
