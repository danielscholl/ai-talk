#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "pytest>=7.4.0",
#   "rich>=13.7.0",
#   "azure-identity>=1.15.0",
#   "python-dotenv>=1.0.0",
#   "openai>=1.65.0,<1.66.0"
# ]
# ///

"""
Basic Agent Example with Azure OpenAI

This example demonstrates how to create a simple agent using the OpenAI API
with Azure OpenAI service. The agent can respond to user queries with helpful information.

Run with:
    uv run basic_agent.py --prompt x

Test with:
    uv run pytest basic_agent.py
"""

import os
import sys
import argparse
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
import asyncio

from openai import AzureOpenAI
from openai.types.chat import ChatCompletion

# Initialize console and load environment variables
console = Console()
load_dotenv()

# Constants
MODEL = os.environ.get("AZURE_MODEL", "gpt-4o")  # Use environment variable or default to "gpt-4o"

class Agent:
    """Simple Agent implementation"""
    def __init__(self, name: str, instructions: str, model: str):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.client = None

    async def run(self, prompt: str) -> str:
        """Run the agent with a prompt"""
        if not self.client:
            self.client = get_azure_openai_client()

        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message.content

def get_azure_openai_client():
    """
    Create and return an Azure OpenAI client.

    Returns:
        An AzureOpenAI client instance.
    """
    if not os.environ.get("AZURE_API_KEY"):
        raise ValueError("Azure OpenAI API key not found. Set AZURE_API_KEY environment variable.")

    if not os.environ.get("AZURE_API_BASE"):
        raise ValueError("Azure OpenAI endpoint not found. Set AZURE_API_BASE environment variable.")

    return AzureOpenAI(
        api_key=os.environ.get("AZURE_API_KEY"),
        api_version=os.environ.get("AZURE_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.environ.get("AZURE_API_BASE")
    )

def create_basic_agent(instructions: str = None) -> Agent:
    """
    Create a basic agent with the given instructions.

    Args:
        instructions: Custom instructions for the agent. If None, default instructions are used.

    Returns:
        An Agent instance configured with the provided instructions.
    """
    default_instructions = """
    You are a helpful assistant that provides accurate and concise information.
    Always be respectful and provide factual responses based on the latest available information.
    If you don't know something, admit it rather than making up information.
    """

    return Agent(
        name="BasicAssistant",
        instructions=instructions or default_instructions,
        model=MODEL
    )

async def run_basic_agent(prompt: str, agent: Optional[Agent] = None) -> str:
    """
    Run the basic agent with the given prompt.

    Args:
        prompt: The user's query or prompt
        agent: Optional pre-configured agent. If None, a default agent is created.

    Returns:
        The agent's response as a string
    """
    # Create agent if not provided
    if agent is None:
        agent = create_basic_agent()

    # Run the agent with the prompt
    return await agent.run(prompt)

def main():
    """Main function to parse arguments and run the agent."""
    parser = argparse.ArgumentParser(description="Basic Agent Example with Azure OpenAI")
    parser.add_argument("--prompt", "-p", type=str, required=True,
                        help="The prompt to send to the agent")

    args = parser.parse_args()

    try:
        # Run the agent and get response
        response = asyncio.run(run_basic_agent(args.prompt))

        # Display the response
        console.print(Panel(response, title="Agent Response", border_style="green"))

    except ValueError as e:
        console.print(Panel(f"[bold red]Error: {str(e)}[/bold red]"))
        sys.exit(1)
    except Exception as e:
        console.print(Panel(f"[bold red]Error: {str(e)}[/bold red]"))
        sys.exit(1)

# Test functions
def test_create_basic_agent():
    """Test that the agent is created with the correct configuration."""
    import pytest
    if not os.environ.get("AZURE_API_KEY"):
        pytest.skip("Azure OpenAI API key not set")

    agent = create_basic_agent("Test instructions")
    assert agent.name == "BasicAssistant"
    assert agent.instructions == "Test instructions"
    assert agent.model == MODEL

def test_run_basic_agent():
    """Test that the agent can run and produce a response."""
    import pytest

    # Skip this test if no Azure OpenAI credentials are available
    if not os.environ.get("AZURE_API_KEY"):
        pytest.skip("Azure OpenAI API key not set")

    # Run a simple test query
    response = asyncio.run(run_basic_agent("What is 2+2?"))

    # Verify we got a non-empty response
    assert response
    assert len(response) > 0
    # The response should contain "4" somewhere
    assert "4" in response

if __name__ == "__main__":
    main()