"""
CodeBaseOpsAI - Simple GitHub Agent Example

This demonstrates a basic ReAct agent that can perform GitHub operations.
"""

import os
from typing import List, Any
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import StructuredTool
from .tools import GithubTools, YamlTools, JsonTools, PackageUpdatesTools
from .agent_prompt import AgentPropmpt


class Agent():
    tools: List[StructuredTool]
    agent_prompt: AgentPropmpt
    llm: ChatGoogleGenerativeAI
    agent: Any  # CompiledGraph from LangChain
    node_lts_version: str

    def __init__(self, node_lts_version: str):
        self.node_lts_version = node_lts_version
        self.tools = self.init_tools()
        self.agent_prompt = AgentPropmpt()
        self.llm = self.init_llm()
        self.agent = self.init_react_agent()

    def init_tools(self) -> List[StructuredTool]:
        github_tools = GithubTools()
        yaml_tools = YamlTools()
        json_tools = JsonTools()
        package_updates_tools = PackageUpdatesTools(
            node_lts_version=self.node_lts_version)
        return github_tools.get_tools() + yaml_tools.get_tools() + json_tools.get_tools() + package_updates_tools.get_tools()

    def init_llm(self) -> ChatGoogleGenerativeAI:
        load_dotenv()
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_output_tokens=1024,
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        return llm

    def init_react_agent(self) -> Any:
        """Create an agent using the modern langchain.agents.create_agent API.

        Returns:
            CompiledGraph: The agent that acts as both agent and executor.
            LangChain automatically handles prompt variable substitution.
        """
        agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.agent_prompt.get_prompt_text()
        )
        return agent

    def get_agent(self) -> Any:
        """Get the agent instance."""
        return self.agent

    def get_agent_executor(self) -> Any:
        """Get the agent executor (alias for get_agent for backward compatibility)."""
        return self.agent
