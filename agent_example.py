"""
Simple LangChain Agent Example
Demonstrates: Custom Tools, Agent Creation, and Prompt Templates
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from datetime import datetime


# ==========================================
# STEP 1: Define Custom Tool Functions
# ==========================================

def count_words(text: str) -> str:
    """Counts the number of words in the provided text."""
    word_count = len(text.split())
    return f"Word count: {word_count}"


def reverse_text(text: str) -> str:
    """Reverses the given text string."""
    reversed_result = text[::-1]
    return f"Reversed text: {reversed_result}"


def get_current_time(input_text: str) -> str:
    """Returns the current date and time. Input is ignored."""
    current = datetime.now()
    return f"Current date and time: {current.strftime('%Y-%m-%d %H:%M:%S')}"


def text_to_uppercase(text: str) -> str:
    """Converts text to uppercase."""
    return f"Uppercase: {text.upper()}"


# ==========================================
# STEP 2: Create Tool Objects
# ==========================================

agent_tools = [
    Tool(
        name="WordCounter",
        func=count_words,
        description="Counts words in a text. Input: any text string"
    ),
    Tool(
        name="TextReverser",
        func=reverse_text,
        description="Reverses the order of characters in text. Input: text to reverse"
    ),
    Tool(
        name="TimeFetcher",
        func=get_current_time,
        description="Gets current date and time. Input: anything (will be ignored)"
    ),
    Tool(
        name="UppercaseConverter",
        func=text_to_uppercase,
        description="Converts text to uppercase letters. Input: text to convert"
    )
]


# ==========================================
# STEP 3: Define Custom Prompt Template
# ==========================================

agent_prompt_text = '''You are a helpful assistant with access to specific tools.

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

agent_prompt = PromptTemplate(
    template=agent_prompt_text,
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
)


# ==========================================
# STEP 4: Initialize LLM and Create Agent
# ==========================================

def create_text_agent():
    """Creates and returns an agent executor."""

    # Initialize the language model
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Create the agent using ReAct framework
    agent = create_react_agent(
        llm=llm,
        tools=agent_tools,
        prompt=agent_prompt
    )

    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=agent_tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )

    return agent_executor


# ==========================================
# STEP 5: Use the Agent
# ==========================================

def main():
    """Main function to demonstrate agent usage."""

    print("=" * 60)
    print("LangChain Agent Example - Text Processing Agent")
    print("=" * 60)

    # Create the agent
    executor = create_text_agent()

    # Example queries
    queries = [
        "How many words are in the phrase 'Hello world from LangChain'?",
        "Convert the text 'agent example' to uppercase",
        "What is the reverse of the text 'Python'?",
        "What time is it right now?"
    ]

    # Run each query
    for idx, query in enumerate(queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Query {idx}: {query}")
        print(f"{'=' * 60}")

        try:
            response = executor.invoke({"input": query})
            print(f"\n✓ Result: {response['output']}")
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")

    print(f"\n{'=' * 60}")
    print("Example completed!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
