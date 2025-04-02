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
Multi-Agent System with Azure OpenAI

This script implements a multi-agent system where a coordinator agent delegates tasks
to specialist agents (science and technology) based on the query topic.

Run with:
    uv run multi_agent.py --prompt "Explain quantum computing and its applications"

Test with:
    uv run pytest multi_agent.py
"""

import os
import sys
import asyncio
import argparse
from typing import List, Optional
from dataclasses import dataclass
from openai import AzureOpenAI
from rich.console import Console
from rich.panel import Panel

console = Console()

def get_client() -> AzureOpenAI:
    """Create and return an Azure OpenAI client."""
    api_base = os.getenv("AZURE_API_BASE")
    api_key = os.getenv("AZURE_API_KEY")
    api_version = os.getenv("AZURE_API_VERSION", "2024-02-01")

    if not api_base or not api_key:
        raise ValueError("AZURE_API_BASE and AZURE_API_KEY environment variables are required")

    return AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=api_base
    )

@dataclass
class Handoff:
    """Represents a handoff between agents."""
    agent: 'Agent'
    description: Optional[str] = None

class Agent:
    """Base class for all agents."""
    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = "gpt-4o",
        handoffs: List[Handoff] = None,
        handoff_description: Optional[str] = None
    ):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.handoffs = handoffs or []
        self.handoff_description = handoff_description

    async def run(self, prompt: str) -> str:
        """Process a prompt and return a response."""
        client = get_client()

        # Build full instructions including handoff options
        full_instructions = self.instructions
        if self.handoffs:
            full_instructions += "\n\nAvailable specialists:\n"
            for handoff in self.handoffs:
                full_instructions += f"- {handoff.agent.name}: {handoff.description}\n"

        messages = [
            {"role": "system", "content": full_instructions},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        content = response.choices[0].message.content

        # Check for delegation directives
        if self.handoffs:
            for handoff in self.handoffs:
                if f"DELEGATE TO {handoff.agent.name}" in content:
                    console.print(Panel(
                        f"[yellow]Coordinator delegating to {handoff.agent.name}[/yellow]"
                    ))
                    return await handoff.agent.run(prompt)

        return content

def handoff(agent: Agent, description: Optional[str] = None) -> Handoff:
    """Create a handoff to the specified agent."""
    return Handoff(agent=agent, description=description or agent.handoff_description)

def create_science_agent() -> Agent:
    """Create and return the science specialist agent."""
    instructions = """You are a science specialist with deep knowledge of physics, chemistry, biology, and related fields.
    Provide accurate, detailed scientific explanations while making complex concepts accessible.
    Use analogies and examples when helpful to illustrate scientific principles.
    Always clarify when something is theoretical or not yet proven. All replies should be in an essay format appropriate for school."""

    return Agent(
        name="Science Specialist",
        instructions=instructions,
        handoff_description="Expert in physics, chemistry, biology, and scientific principles"
    )

def create_tech_agent() -> Agent:
    """Create and return the technology specialist agent."""
    instructions = """You are a technology specialist with expertise in computer science, programming, AI, and digital technologies.
    Provide clear, accurate explanations of technical concepts and their practical applications.
    When discussing programming, focus on concepts rather than writing extensive code.
    Explain how technologies work and their real-world impact. All replies should be in JSON format."""

    return Agent(
        name="Technology Specialist",
        instructions=instructions,
        handoff_description="Expert in computer science, programming, AI, and digital technologies"
    )

def create_coordinator_agent(specialists: List[Agent]) -> Agent:
    """Create and return the coordinator agent."""
    instructions = """You are a coordinator who determines which specialist should handle a user's question.
    Analyze the user's query and decide which specialist would be best suited to respond.
    For questions that span multiple domains, choose the specialist most relevant to the core of the question.
    To delegate, include the exact text 'DELEGATE TO <specialist name>' in your response."""

    handoffs = [handoff(specialist) for specialist in specialists]

    return Agent(
        name="Coordinator",
        instructions=instructions,
        handoffs=handoffs
    )

async def run_multi_agent_system(prompt: str) -> str:
    """Run the multi-agent system with the given prompt."""
    specialists = [
        create_science_agent(),
        create_tech_agent()
    ]

    coordinator = create_coordinator_agent(specialists)

    try:
        response = await coordinator.run(prompt)
        return response
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return f"Error processing request: {str(e)}"

def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Multi-agent system using Azure OpenAI")
    parser.add_argument("--prompt", required=True, help="The prompt to process")
    args = parser.parse_args()

    try:
        response = asyncio.run(run_multi_agent_system(args.prompt))
        console.print(Panel(response, title="Response"))
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

# Tests
def test_create_specialist_agents():
    """Test specialist agent creation."""
    science_agent = create_science_agent()
    tech_agent = create_tech_agent()

    assert science_agent.name == "Science Specialist"
    assert tech_agent.name == "Technology Specialist"
    assert science_agent.model == "gpt-4o"
    assert tech_agent.model == "gpt-4o"

def test_create_coordinator_agent():
    """Test coordinator agent creation."""
    specialists = [create_science_agent(), create_tech_agent()]
    coordinator = create_coordinator_agent(specialists)

    assert coordinator.name == "Coordinator"
    assert len(coordinator.handoffs) == 2
    assert coordinator.model == "gpt-4o"

def test_handoff_function():
    """Test handoff creation."""
    agent = create_science_agent()
    handoff_obj = handoff(agent)

    assert handoff_obj.agent == agent
    assert handoff_obj.description == agent.handoff_description

def test_run_multi_agent_system():
    """Test the multi-agent system."""
    response = asyncio.run(run_multi_agent_system("What is quantum computing?"))
    assert isinstance(response, str)
    assert len(response) > 0

if __name__ == "__main__":
    main()
